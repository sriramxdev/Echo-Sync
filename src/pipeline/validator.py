"""Dataset integrity, extraction, and spatial-temporal normalization module."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import cv2
import mediapipe as mp
import numpy as np

from src.pipeline.schema import (
    FACE_CORE_INDICES,
    HAND_LANDMARK_COUNT,
    POSE_UPPER_BODY_INDICES,
    SCHEMA,
    create_empty_frame,
)


class LandmarkProcessor:
    """Processes raw MediaPipe landmarks into canonical, normalized tensors."""

    @staticmethod
    def extract_canonical_frame(results: Any) -> np.ndarray:
        """
        Extracts exactly 75 canonical landmarks from MediaPipe Holistic output.
        Output layout: (75, 4) -> [x, y, z, confidence]
        """
        frame = create_empty_frame()

        # 1. Pose: indices 0..24
        if results.pose_landmarks:
            for out_idx, mp_idx in enumerate(POSE_UPPER_BODY_INDICES):
                lm = results.pose_landmarks.landmark[mp_idx]
                frame[out_idx] = [lm.x, lm.y, lm.z, lm.visibility]

        # 2. Left Hand: indices 25..45
        if results.left_hand_landmarks:
            for out_idx in range(HAND_LANDMARK_COUNT):
                lm = results.left_hand_landmarks.landmark[out_idx]
                frame[25 + out_idx] = [lm.x, lm.y, lm.z, 1.0]

        # 3. Right Hand: indices 46..66
        if results.right_hand_landmarks:
            for out_idx in range(HAND_LANDMARK_COUNT):
                lm = results.right_hand_landmarks.landmark[out_idx]
                frame[46 + out_idx] = [lm.x, lm.y, lm.z, 1.0]

        # 4. Face Core: indices 67..74
        if results.face_landmarks:
            for out_idx, mp_idx in enumerate(FACE_CORE_INDICES):
                lm = results.face_landmarks.landmark[mp_idx]
                frame[67 + out_idx] = [lm.x, lm.y, lm.z, 1.0]

        return frame

    @staticmethod
    def normalize_spatial_invariance(frame: np.ndarray) -> np.ndarray:
        """
        Centers coordinate plane at the mid-shoulder and normalizes scale
        by inter-shoulder Euclidean distance.
        """
        norm_frame = frame.copy()

        # Anchors: 11 = Left Shoulder, 12 = Right Shoulder
        left_shoulder = norm_frame[11, :3]
        right_shoulder = norm_frame[12, :3]

        # Visibility threshold for shoulders
        if norm_frame[11, 3] > 0.3 and norm_frame[12, 3] > 0.3:
            mid_shoulder = (left_shoulder + right_shoulder) / 2.0
            shoulder_dist = float(np.linalg.norm(left_shoulder - right_shoulder))

            # Apply translation
            norm_frame[:, :3] -= mid_shoulder

            # Apply scaling
            if shoulder_dist > 1e-3:
                norm_frame[:, :3] /= shoulder_dist
        else:
            # Fallback anchor: Nose tip (index 0)
            if norm_frame[0, 3] > 0.3:
                norm_frame[:, :3] -= norm_frame[0, :3]

        return norm_frame

    @staticmethod
    def temporal_resample(sequence: np.ndarray, target_length: int = 90) -> np.ndarray:
        """
        Interpolates sequence length along axis 0 from T_raw to target_length.
        Shape: (T, 75, 4) -> (90, 75, 4)
        """
        current_length = sequence.shape[0]
        if current_length == target_length:
            return sequence

        if current_length == 0:
            return np.zeros((target_length, SCHEMA.total_vertices, SCHEMA.channels), dtype=np.float32)

        # Generate sample points
        source_indices = np.linspace(0, current_length - 1, num=current_length)
        target_indices = np.linspace(0, current_length - 1, num=target_length)

        resampled = np.zeros(
            (target_length, SCHEMA.total_vertices, SCHEMA.channels), dtype=np.float32
        )

        # Resample channels across time
        for v in range(SCHEMA.total_vertices):
            for c in range(SCHEMA.channels):
                resampled[:, v, c] = np.interp(
                    target_indices, source_indices, sequence[:, v, c]
                )

        return resampled