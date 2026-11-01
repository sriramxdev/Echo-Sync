# src/schema/topology.py
"""
Echo-Sync Canonical Landmark Schema & Topology Definitions.

Standardizes the multi-modal keypoint representation across data ingestion,
spatial normalization, edge decimation, model training, and live inference.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Final, Tuple
import numpy as np


# ---------------------------------------------------------
# 1. MediaPipe Holistic Topology Indices
# ---------------------------------------------------------

# Upper body pose subset (indices 0..24):
# 0-10: Face/head pose anchors, 11-12: Shoulders, 13-14: Elbows, 15-16: Wrists,
# 17-22: Hands/pinky/index/thumb bounds, 23-24: Hips
POSE_UPPER_BODY_INDICES: Final[Tuple[int, ...]] = tuple(range(25))

# 8 facial anchors for head orientation, mouth movements, and gaze
# (Nose tip, L/R inner/outer eye corners, mouth corners, chin anchor)
FACE_CORE_INDICES: Final[Tuple[int, ...]] = (1, 33, 133, 263, 362, 61, 291, 152)

# Full 21 keypoints per hand
HAND_LANDMARK_COUNT: Final[int] = 21


# ---------------------------------------------------------
# 2. Canonical Topology Contract (V = 75, C = 4)
# ---------------------------------------------------------

@dataclass(frozen=True)
class LandmarkTopology:
    """Canonical landmark counts, channel specs, and offset slices."""

    num_pose: int = len(POSE_UPPER_BODY_INDICES)  # 25
    num_left_hand: int = HAND_LANDMARK_COUNT        # 21
    num_right_hand: int = HAND_LANDMARK_COUNT       # 21
    num_face: int = len(FACE_CORE_INDICES)          # 8

    # Channels: (x, y, z, confidence/visibility)
    channels: int = 4

    # Default temporal frame target for model inference
    target_sequence_length: int = 90

    @property
    def total_vertices(self) -> int:
        """Returns total joint count V (default: 75)."""
        return self.num_pose + self.num_left_hand + self.num_right_hand + self.num_face

    @property
    def frame_shape(self) -> Tuple[int, int]:
        """Expected shape for a single raw frame: (V, C) -> (75, 4)."""
        return (self.total_vertices, self.channels)

    # Offset ranges in the unified (75, 4) tensor
    @property
    def pose_slice(self) -> slice:
        return slice(0, 25)

    @property
    def left_hand_slice(self) -> slice:
        return slice(25, 46)

    @property
    def right_hand_slice(self) -> slice:
        return slice(46, 67)

    @property
    def face_slice(self) -> slice:
        return slice(67, 75)

    def create_empty_frame(self) -> np.ndarray:
        """Helper returning a zero-initialized array matching (75, 4)."""
        return np.zeros(self.frame_shape, dtype=np.float32)


# Global singleton instance for project-wide use
SCHEMA = LandmarkTopology()