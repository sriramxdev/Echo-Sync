"""Global foundation ST-GCN backbone."""

from __future__ import annotations
import torch
import torch.nn as nn
from src.model.st_gcn import STGCNBlock
from src.pipeline.schema import SCHEMA


class GlobalSignBackbone(nn.Module):
    """
    Foundational ST-GCN backbone for Stage 1 pre-training.
    Input: (Batch, 4, 90, 75)
    Output feature map: (Batch, 256, 90, 75) or pooled representation.
    """

    def __init__(self, in_channels: int = 4):
        super().__init__()
        self.data_bn = nn.BatchNorm1d(SCHEMA.total_vertices * in_channels)

        # Channel expansion stages: 4 -> 64 -> 128 -> 256
        self.layer1 = STGCNBlock(in_channels, 64)
        self.layer2 = STGCNBlock(64, 64)
        self.layer3 = STGCNBlock(64, 128)
        self.layer4 = STGCNBlock(128, 256)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        N, C, T, V = x.size()

        # Batch normalization across initial feature dimensions
        x_flat = x.permute(0, 1, 3, 2).contiguous().view(N, C * V, T)
        x_bn = self.data_bn(x_flat)
        x = x_bn.view(N, C, V, T).permute(0, 1, 3, 2).contiguous()

        # Feedforward across spatial-temporal blocks
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)  # Shape: (N, 256, 90, 75)
        return x