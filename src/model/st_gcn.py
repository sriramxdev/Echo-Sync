"""Spatial-Temporal Graph Convolutional Block implementations."""

from __future__ import annotations
import torch
import torch.nn as nn
from src.model.graph import GRAPH


class SpatialGraphConv(nn.Module):
    """Spatial graph convolution using skeletal adjacency."""

    def __init__(self, in_channels: int, out_channels: int):
        super().__init__()
        self.conv = nn.Conv2d(in_channels, out_channels, kernel_size=1)
        # Register normalized adjacency buffer (75, 75)
        self.register_buffer("A", GRAPH.A)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Input shape: (N, C, T, V)
        N, C, T, V = x.size()
        
        # Multiply across the joint graph: (V, V) @ (N*T, V, C) -> einsum
        # Reorder to (N, T, C, V) for graph propagation
        x_mapped = torch.einsum("vw, nctw -> nctv", self.A, x)
        
        # 1x1 conv across channel dimensions
        out = self.conv(x_mapped)
        return out


class STGCNBlock(nn.Module):
    """Core ST-GCN block: Spatial Graph Conv -> BatchNorm -> Temporal Conv -> Residual."""

    def __init__(self, in_channels: int, out_channels: int, temporal_kernel_size: int = 9, stride: int = 1):
        super().__init__()
        
        # Spatial Graph Conv
        self.sgcn = SpatialGraphConv(in_channels, out_channels)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.relu = nn.ReLU(inplace=True)

        # Temporal Conv (stride > 1 downsizes sequence length T)
        padding = (temporal_kernel_size - 1) // 2
        self.tgcn = nn.Sequential(
            nn.BatchNorm2d(out_channels),
            nn.Conv2d(
                out_channels,
                out_channels,
                kernel_size=(temporal_kernel_size, 1),
                stride=(stride, 1),
                padding=(padding, 0),
            ),
            nn.BatchNorm2d(out_channels),
        )

        # Residual connection
        if in_channels != out_channels or stride != 1:
            self.residual = nn.Sequential(
                nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=(stride, 1)),
                nn.BatchNorm2d(out_channels),
            )
        else:
            self.residual = nn.Identity()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x shape: (N, C, T, V)
        res = self.residual(x)
        x = self.relu(self.bn1(self.sgcn(x)))
        x = self.tgcn(x) + res
        return self.relu(x)