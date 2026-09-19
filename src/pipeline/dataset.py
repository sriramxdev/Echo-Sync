"""PyTorch Dataset implementation for ST-GCN landmark sequences."""

from pathlib import Path
from typing import List, Tuple
import numpy as np
import torch
from torch.utils.data import Dataset


class SignGraphDataset(Dataset):
    """
    Loads pre-extracted (90, 75, 4) landmark tensors.
    Yields format required for ST-GCN: (C, T, V) -> (4, 90, 75).
    """

    def __init__(self, tensor_files: List[Path], labels: List[int]):
        assert len(tensor_files) == len(labels), "File count and label count must match"
        self.tensor_files = tensor_files
        self.labels = labels

    def __len__(self) -> int:
        return len(self.tensor_files)

    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, torch.Tensor]:
        file_path = self.tensor_files[idx]
        data = np.load(file_path)  # Shape: (T, V, C) -> (90, 75, 4)

        # Transpose to PyTorch ST-GCN shape: (C, T, V)
        data = np.transpose(data, (2, 0, 1))

        x = torch.from_numpy(data).float()
        y = torch.tensor(self.labels[idx], dtype=torch.long)
        return x, y