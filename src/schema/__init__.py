# THIS FILE IS PART OF THE ECHO-SYNC PROJECT.
# Visit :
# src/schema/__init__.py
from src.schema.topology import (
    SCHEMA,
    LandmarkTopology,
    POSE_UPPER_BODY_INDICES,
    FACE_CORE_INDICES,
    HAND_LANDMARK_COUNT,
)

__all__ = [
    "SCHEMA",
    "LandmarkTopology",
    "POSE_UPPER_BODY_INDICES",
    "FACE_CORE_INDICES",
    "HAND_LANDMARK_COUNT",
]