# THIS FILE IS PART OF THE ECHO-SYNC PROJECT.
# Visit :

"""
Echo-Sync Landmark Schema & Topology Definitions.

Standardizes the multi-modal keypoint representation across data ingestion,
spatial normalization, model training, and edge inference.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Tuple
import numpy as np


# ---------------------------------------------------------------------------
# MediaPipe Holistic Topology Indices
# ---------------------------------------------------------------------------

# Upper body pose subset: skip legs/feet (indices 25-32) to eliminate noise
# 0-10: Face/head pose anchors, 11-12: Shoulders, 13-14: Elbows, 15-16: Wrists,
# 17-22: Hands/pinky/index/thumb bounds, 23-24: Hips
POSE_UPPER_BODY_INDICES: Final[Tuple[int, ...]] = tuple(range(25))

# 8 facial anchors for head orientation, mouth movements, and gaze
# (Nose, inner/outer eye corners, mouth corners, chin anchor)
FACE_CORE_INDICES: Final[Tuple[int, ...]] = (
    1,    # Nose tip
    33,   # Left eye outer corner
    133,  # Left eye inner corner
    263,  # Right eye inner corner
    362,  # Right eye outer corner
    61,   # Mouth left corner
    291,  # Mouth right corner
    152,  # Chin
)

# Hand topologies: Full 21 keypoints per hand
HAND_LANDMARK_COUNT: Final[int] = 21


@dataclass(frozen=True)
class LandmarkTopology:
    """Canonical landmark counts and index offsets."""

    num_pose: int = len(POSE_UPPER_BODY_INDICES)  # 25
    num_left_hand: int = HAND_LANDMARK_COUNT      # 21
    num_right_hand: int = HAND_LANDMARK_COUNT     # 21
    num_face: int = len(FACE_CORE_INDICES)        # 8

    # Channels: (x, y, z, confidence/visibility)
    channels: int = 4

    # Default temporal frame padding/resampling target for model batching
    target_sequence_length: int = 90

    @property
    def total_vertices(self) -> int:
        """Returns total joint count V (default: 75)."""
        return self.num_pose + self.num_left_hand + self.num_right_hand + self.num_face

    @property
    def frame_shape(self) -> Tuple[int, int]:
        """Expected shape for a single frame: (V, C) -> (75, 4)."""
        return (self.total_vertices, self.channels)

    @property
    def sequence_shape(self) -> Tuple[int, int, int]:
        """Expected shape for a model batch item: (T, V, C) -> (90, 75, 4)."""
        return (self.target_sequence_length, self.total_vertices, self.channels)

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


# Global singleton instance for project-wide use
SCHEMA = LandmarkTopology()


# ---------------------------------------------------------------------------
# Skeletal Graph Topology (Bones / Edges for ST-GCN & GNN Modeling)
# ---------------------------------------------------------------------------

# Spatial adjacency edges connecting joints within the 75-vertex space
POSE_EDGES = [
    (11, 12), (11, 13), (13, 15), (12, 14), (14, 16),  # Arms & shoulders
    (11, 23), (12, 24), (23, 24)                       # Torso
]

# Standard 21-point hand skeleton connections (0-indexed per hand)
HAND_EDGES_LOCAL = [
    (0, 1), (1, 2), (2, 3), (3, 4),        # Thumb
    (0, 5), (5, 6), (6, 7), (7, 8),        # Index
    (0, 9), (9, 10), (10, 11), (11, 12),   # Middle
    (0, 13), (13, 14), (14, 15), (15, 16), # Ring
    (0, 17), (17, 18), (18, 19), (19, 20), # Pinky
    (5, 9), (9, 13), (13, 17)              # Palm base
]

LEFT_HAND_EDGES = [(u + 25, v + 25) for u, v in HAND_EDGES_LOCAL]
RIGHT_HAND_EDGES = [(u + 46, v + 46) for u, v in HAND_EDGES_LOCAL]

# Body-to-hand connections (Pose Wrists to Hand Roots)
CROSS_EDGES = [
    (15, 25),  # Pose Left Wrist (15) -> Left Hand Root (25)
    (16, 46),  # Pose Right Wrist (16) -> Right Hand Root (46)
]

ALL_GRAPH_EDGES = POSE_EDGES + LEFT_HAND_EDGES + RIGHT_HAND_EDGES + CROSS_EDGES


def create_empty_frame() -> np.ndarray:
    """Helper returning a zero-initialized array matching the schema shape (75, 4)."""
    return np.zeros(SCHEMA.frame_shape, dtype=np.float32)