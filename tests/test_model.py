import torch
from src.model.backbone import GlobalSignBackbone

def test_backbone_forward():
    # Batch=2, Channels=4 (x,y,z,conf), Time=90, Vertices=75
    mock_input = torch.randn(2, 4, 90, 75)
    model = GlobalSignBackbone(in_channels=4)
    model.eval()

    with torch.no_grad():
        out = model(mock_input)

    assert out.shape == (2, 256, 90, 75), f"Unexpected output shape: {out.shape}"
    print(f"✓ ST-GCN Backbone initialized and passed: output shape = {out.shape}")

if __name__ == "__main__":
    test_backbone_forward()