# src/ingestion/broadcaster.py
"""Dual-endpoint Stage 1 broadcaster: zero-copy internal queue + WebSocket UI stream."""

from __future__ import annotations

import numpy as np
import asyncio
import base64
import json
import queue
import threading
from typing import Optional, Set
import cv2
import websockets
from websockets.asyncio.server import ServerConnection

from src.schema import ALL_GRAPH_EDGES
from src.ingestion.holistic import FramePacket, RawHolisticIngestor


class IngestionBroadcaster:
    """
    Runs Stage 1 ingestion once and fans out packets to:
      1. Internal ML pipeline (Stage 2 DynaPrune) via bounded in-memory queue.
      2. External UI (Tauri / browser) via lightweight local WebSocket.
    """

    def __init__(
        self,
        ingestor: RawHolisticIngestor,
        ws_host: str = "127.0.0.1",
        ws_port: int = 8765,
        jpeg_quality: int = 75,
    ):
        self.ingestor = ingestor
        self.ws_host = ws_host
        self.ws_port = ws_port
        self.jpeg_quality = jpeg_quality

        # Endpoint 1: Single-slot ring queue for Stage 2 ML consumer
        self._ml_queue: queue.Queue[FramePacket] = queue.Queue(maxsize=1)

        # Endpoint 2: WebSocket state
        self._ws_clients: Set[ServerConnection] = set()
        self._ws_loop: Optional[asyncio.AbstractEventLoop] = None
        self._ws_thread: Optional[threading.Thread] = None

        self._producer_thread: Optional[threading.Thread] = None
        self._running = False

    def _serialize_for_ui(self, packet: FramePacket) -> str:
        """Encodes landmarks and optional JPEG frame into a single synced payload."""
        img_b64: Optional[str] = None
        if packet.bgr_image is not None:
            ok, buf = cv2.imencode(
                ".jpg", packet.bgr_image, [cv2.IMWRITE_JPEG_QUALITY, self.jpeg_quality]
            )
            if ok:
                img_b64 = base64.b64encode(buf.tobytes()).decode("ascii")

        payload = {
            "type": "frame",
            "frame_idx": packet.frame_idx,
            "latency_ms": round(packet.timestamp_ms, 2),
            "landmarks": np.round(packet.landmarks, 4).tolist(),
            "image_jpeg_b64": img_b64,
        }
        return json.dumps(payload)

    async def _ws_handler(self, websocket: ServerConnection) -> None:
        self._ws_clients.add(websocket)
        try:
            # Send static graph topology once on connection so UI knows which dots to connect
            handshake = json.dumps({
                "type": "topology",
                "num_vertices": 75,
                "edges": ALL_GRAPH_EDGES,
            })
            await websocket.send(handshake)
            await websocket.wait_closed()
        finally:
            self._ws_clients.discard(websocket)

    async def _broadcast_ws(self, message: str) -> None:
        if not self._ws_clients:
            return
        websockets.broadcast(self._ws_clients, message)

    def _run_ws_server(self) -> None:
        self._ws_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._ws_loop)

        async def serve() -> None:
            async with websockets.serve(self._ws_handler, self.ws_host, self.ws_port):
                while self._running:
                    await asyncio.sleep(0.1)

        self._ws_loop.run_until_complete(serve())

    def _producer_loop(self) -> None:
        for packet in self.ingestor.stream():
            if not self._running:
                break

            # 1. Push to Internal ML Endpoint (drop stale frame if consumer is busy)
            if self._ml_queue.full():
                try:
                    self._ml_queue.get_nowait()
                except queue.Empty:
                    pass
            self._ml_queue.put_nowait(packet)

            # 2. Push to WebSocket UI Endpoint ONLY if a UI client is connected
            if self._ws_clients and self._ws_loop is not None:
                msg = self._serialize_for_ui(packet)
                asyncio.run_coroutine_threadsafe(self._broadcast_ws(msg), self._ws_loop)

    def start(self, enable_ws: bool = True) -> "IngestionBroadcaster":
        if self._running:
            return self
        self._running = True

        if enable_ws:
            self._ws_thread = threading.Thread(target=self._run_ws_server, daemon=True)
            self._ws_thread.start()

        self._producer_thread = threading.Thread(target=self._producer_loop, daemon=True)
        self._producer_thread.start()
        return self

    def get_latest_packet(self, timeout: float = 1.0) -> Optional[FramePacket]:
        """Endpoint 1 consumer method: used by Stage 2 (DynaPrune)."""
        try:
            return self._ml_queue.get(timeout=timeout)
        except queue.Empty:
            return None

    def stop(self) -> None:
        self._running = False
        self.ingestor.close()
        if self._producer_thread:
            self._producer_thread.join(timeout=1.0)
        if self._ws_thread:
            self._ws_thread.join(timeout=1.0)