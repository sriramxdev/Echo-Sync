# src/ingestion/camera.py
"""Threaded OpenCV camera capture to prevent buffer lag on edge hardware."""

import threading
import time
from typing import Optional, Tuple
import cv2
import numpy as np


class EdgeCameraStream:
    """Threaded camera wrapper ensuring zero buffer accumulation."""

    def __init__(self, source: int | str = 0, width: int = 640, height: int = 480):
        self.source = source
        self.width = width
        self.height = height

        self.cap = cv2.VideoCapture(self.source)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.cap.set(cv2.CAP_PROP_FPS, 30)

        self.grabbed, self.frame = self.cap.read()
        self.running = False
        self.lock = threading.Lock()
        self.thread: Optional[threading.Thread] = None

    def start(self) -> "EdgeCameraStream":
        if self.running:
            return self
        self.running = True
        self.thread = threading.Thread(target=self._update, daemon=True)
        self.thread.start()
        return self

    def _update(self) -> None:
        while self.running:
            grabbed, frame = self.cap.read()
            if not grabbed:
                time.sleep(0.005)
                continue
            with self.lock:
                self.grabbed = grabbed
                self.frame = frame  # Overwrites immediately; no queue lag

    def read_latest(self) -> Tuple[bool, Optional[np.ndarray]]:
        with self.lock:
            if not self.grabbed or self.frame is None:
                return False, None
            return True, self.frame.copy()

    def release(self) -> None:
        self.running = False
        if self.thread is not None:
            self.thread.join(timeout=1.0)
        self.cap.release()