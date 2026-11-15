# THIS FILE IS PART OF THE ECHO-SYNC PROJECT.
# Visit :
# src/schema/topology.py
"""
Echo-Sync Canonical Landmark Schema & Topology Definitions.

Standardizes the multi-modal keypoint representation and skeletal edges across
data ingestion, spatial normalization, edge decimation, ST-GCN training, and UI rendering.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Final, List, Tuple
import numpy as np


# ---------------------------------------------------------
# 1. MediaPipe Holistic Topology Indices
# ---------------------------------------------------------

POSE_UPPER_BODY_INDICES: Final[Tuple[int, ...]] = tuple(range(25))
FACE_CORE_INDICES: Final[Tuple[int, ...]] = (1, 33, 133, 263, 362, 61, 291, 152)
HAND_LANDMARK_COUNT: Final[int] = 21


# ---------------------------------------------------------
# 2. Skeletal Graph Topology (Bones / Edges in 75-Vertex Space)
# ---------------------------------------------------------

POSE_EDGES: Final[List[Tuple[int, int]]] = [
    (11, 12), (11, 13), (13, 15), (12, 14), (14, 16),  # Arms & shoulders
    (11, 23), (12, 24), (23, 24),                      # Torso
]

HAND_EDGES_LOCAL: Final[List[Tuple[int, int]]] = [
    (0, 1), (1, 2), (2, 3), (3, 4),        # Thumb
    (0, 5), (5, 6), (6, 7), (7, 8),        # Index
    (0, 9), (9, 10), (10, 11), (11, 12),   # Middle
    (0, 13), (13, 14), (14, 15), (15, 16), # Ring
    (0, 17), (17, 18), (18, 19), (19, 20), # Pinky
    (5, 9), (9, 13), (13, 17),             # Palm base
]

LEFT_HAND_EDGES: Final[List[Tuple[int, int]]] = [(u + 25, v + 25) for u, v in HAND_EDGES_LOCAL]
RIGHT_HAND_EDGES: Final[List[Tuple[int, int]]] = [(u + 46, v + 46) for u, v in HAND_EDGES_LOCAL]

CROSS_EDGES: Final[List[Tuple[int, int]]] = [
    (15, 25),  # Pose Left Wrist (15) -> Left Hand Root (25)
    (16, 46),  # Pose Right Wrist (16) -> Right Hand Root (46)
]

ALL_GRAPH_EDGES: Final[List[Tuple[int, int]]] = (
    POSE_EDGES + LEFT_HAND_EDGES + RIGHT_HAND_EDGES + CROSS_EDGES
)


# ---------------------------------------------------------
# 3. Canonical Topology Contract (V = 75, C = 4)
# ---------------------------------------------------------

@dataclass(frozen=True)
class LandmarkTopology:
    """Canonical landmark counts, channel specs, and offset slices."""

    num_pose: int = len(POSE_UPPER_BODY_INDICES)  # 25
    num_left_hand: int = HAND_LANDMARK_COUNT        # 21
    num_right_hand: int = HAND_LANDMARK_COUNT       # 21
    num_face: int = len(FACE_CORE_INDICES)          # 8
    channels: int = 4                               # (x, y, z, confidence)
    target_sequence_length: int = 90

    @property
    def total_vertices(self) -> int:
        return self.num_pose + self.num_left_hand + self.num_right_hand + self.num_face

    @property
    def frame_shape(self) -> Tuple[int, int]:
        return (self.total_vertices, self.channels)

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
        return np.zeros(self.frame_shape, dtype=np.float32)


SCHEMA = LandmarkTopology()