"""Spatial graph definition and normalized adjacency matrix generation."""

from __future__ import annotations
import numpy as np
import torch
from src.pipeline.schema import ALL_GRAPH_EDGES, SCHEMA


class SkeletonGraph:
    """Builds and normalizes spatial adjacency matrices for ST-GCN."""

    def __init__(self, max_hop: int = 1):
        self.num_vertices = SCHEMA.total_vertices  # 75
        self.edges = ALL_GRAPH_EDGES
        self.max_hop = max_hop
        self.A = self._build_normalized_adjacency()

    def _build_normalized_adjacency(self) -> torch.Tensor:
        # 1. Initialize self-connection identity matrix
        adj = np.eye(self.num_vertices, dtype=np.float32)

        # 2. Populate bi-directional edges from schema
        for u, v in self.edges:
            adj[u, v] = 1.0
            adj[v, u] = 1.0

        # 3. Symmetrically normalize: D^(-1/2) * A * D^(-1/2)
        row_sum = np.sum(adj, axis=1)
        d_inv_sqrt = np.power(row_sum, -0.5, where=row_sum > 0)
        d_inv_sqrt[row_sum <= 0] = 0.0
        d_mat_inv_sqrt = np.diag(d_inv_sqrt)

        norm_adj = d_mat_inv_sqrt @ adj @ d_mat_inv_sqrt
        return torch.from_numpy(norm_adj).float()


# Global graph instance
GRAPH = SkeletonGraph()