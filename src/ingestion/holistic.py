# src/ingestion/holistic.py
"""MediaPipe Holistic raw ingestion engine outputting canonical (75, 4) packets."""

from dataclasses import dataclass
from typing import Iterator, Optional
import cv2
import mediapipe as mp
import numpy as np

from src.schema import (
    SCHEMA,
    POSE_UPPER_BODY_INDICES,
    FACE_CORE_INDICES,
    HAND_LANDMARK_COUNT,
)
from src.ingestion.camera import EdgeCameraStream


@dataclass
class FramePacket:
    """Standardized multi-purpose payload produced by Stage 1."""
    frame_idx: int
    timestamp_ms: float
    landmarks: np.ndarray             # Shape: (75, 4) -> [x, y, z, conf]
    bgr_image: Optional[np.ndarray]   # Raw frame for visualization / WebUI


class RawHolisticIngestor:
    def __init__(
        self,
        camera_id: int | str = 0,
        width: int = 640,
        height: int = 480,
        model_complexity: int = 0,
        include_image: bool = True,
    ):
        self.camera = EdgeCameraStream(source=camera_id, width=width, height=height)
        self.include_image = include_image
        self.frame_idx = 0
        self._closed = False

        self.mp_holistic = mp.solutions.holistic
        self.holistic = self.mp_holistic.Holistic(
            static_image_mode=False,
            model_complexity=model_complexity,
            smooth_landmarks=True,
            refine_face_landmarks=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )

    def __enter__(self) -> "RawHolisticIngestor":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    def _extract_canonical_landmarks(self, results) -> np.ndarray:
        tensor = SCHEMA.create_empty_frame()

        # 1. Pose Upper Body (indices 0..24)
        if results.pose_landmarks:
            for out_idx, mp_idx in enumerate(POSE_UPPER_BODY_INDICES):
                lm = results.pose_landmarks.landmark[mp_idx]
                tensor[out_idx] = [lm.x, lm.y, lm.z, lm.visibility]

        # 2. Left Hand (indices 25..45)
        if results.left_hand_landmarks:
            for out_idx in range(HAND_LANDMARK_COUNT):
                lm = results.left_hand_landmarks.landmark[out_idx]
                tensor[25 + out_idx] = [lm.x, lm.y, lm.z, 1.0]

        # 3. Right Hand (indices 46..66)
        if results.right_hand_landmarks:
            for out_idx in range(HAND_LANDMARK_COUNT):
                lm = results.right_hand_landmarks.landmark[out_idx]
                tensor[46 + out_idx] = [lm.x, lm.y, lm.z, 1.0]

        # 4. Face Core Anchors (indices 67..74)
        if results.face_landmarks:
            for out_idx, mp_idx in enumerate(FACE_CORE_INDICES):
                lm = results.face_landmarks.landmark[mp_idx]
                tensor[67 + out_idx] = [lm.x, lm.y, lm.z, 1.0]

        return tensor

    def stream(self) -> Iterator[FramePacket]:
        """Continuous generator yielding canonical FramePackets."""
        self.camera.start()
        try:
            while True:
                success, frame = self.camera.read_latest()
                if not success or frame is None:
                    continue

                self.frame_idx += 1
                t_start = cv2.getTickCount()

                # RGB conversion for MediaPipe
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                rgb_frame.flags.writeable = False
                results = self.holistic.process(rgb_frame)

                # Extract into canonical (75, 4) array
                landmarks = self._extract_canonical_landmarks(results)
                
                t_end = cv2.getTickCount()
                latency_ms = ((t_end - t_start) / cv2.getTickFrequency()) * 1000.0

                yield FramePacket(
                    frame_idx=self.frame_idx,
                    timestamp_ms=latency_ms,
                    landmarks=landmarks,
                    bgr_image=frame if self.include_image else None,
                )
        finally:
            self.close()

    def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        self.camera.release()
        if self.holistic is not None:
            self.holistic.close()