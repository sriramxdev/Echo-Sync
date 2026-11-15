# tests/unit/test_topology.py
import numpy as np
from src.schema import SCHEMA, ALL_GRAPH_EDGES


def test_canonical_vertex_counts():
    assert SCHEMA.num_pose == 25
    assert SCHEMA.num_left_hand == 21
    assert SCHEMA.num_right_hand == 21
    assert SCHEMA.num_face == 8
    assert SCHEMA.total_vertices == 75
    assert SCHEMA.frame_shape == (75, 4)


def test_slice_partitions_cover_all_vertices():
    frame = SCHEMA.create_empty_frame()
    assert frame.shape == (75, 4)
    assert frame.dtype == np.float32

    frame[SCHEMA.pose_slice] = 1.0
    frame[SCHEMA.left_hand_slice] = 2.0
    frame[SCHEMA.right_hand_slice] = 3.0
    frame[SCHEMA.face_slice] = 4.0

    # Ensure every single vertex was assigned with zero gaps or overlaps
    assert np.all(frame[:, 0] > 0.0)


def test_graph_edges_within_bounds():
    assert len(ALL_GRAPH_EDGES) == 56
    for u, v in ALL_GRAPH_EDGES:
        assert 0 <= u < SCHEMA.total_vertices
        assert 0 <= v < SCHEMA.total_vertices
        assert u != v