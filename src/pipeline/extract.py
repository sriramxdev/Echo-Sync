"""Batch extraction script to convert videos into normalized (90, 75, 4) tensors."""

from __future__ import annotations

import argparse
from pathlib import Path
import cv2
import mediapipe as mp
import numpy as np
from tqdm import tqdm

from src.pipeline.validator import LandmarkProcessor


def process_video(video_path: Path, holistic: Any) -> Optional[np.ndarray]:
    cap = cv2.VideoCapture(str(video_path))
    frames = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb_frame.flags.writeable = False
        results = holistic.process(rgb_frame)

        canonical = LandmarkProcessor.extract_canonical_frame(results)
        normalized = LandmarkProcessor.normalize_spatial_invariance(canonical)
        frames.append(normalized)

    cap.release()

    if not frames:
        return None

    seq_arr = np.array(frames, dtype=np.float32)
    # Temporal normalization to fixed shape (90, 75, 4)
    return LandmarkProcessor.temporal_resample(seq_arr, target_length=90)


def run_batch_extraction(input_dir: Path, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    mp_holistic = mp.solutions.holistic

    holistic = mp_holistic.Holistic(
        static_image_mode=False,
        model_complexity=1,
        smooth_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    )

    video_files = [f for f in input_dir.glob("**/*") if f.suffix.lower() in {".mp4", ".mov", ".avi"}]
    print(f"Found {len(video_files)} videos in {input_dir}")

    for vid in tqdm(video_files):
        out_file = output_dir / f"{vid.stem}.npy"
        if out_file.exists():
            continue

        tensor = process_video(vid, holistic)
        if tensor is not None:
            np.save(out_file, tensor)

    holistic.close()
    print(f"Extracted tensors saved to {output_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True, help="Input directory containing videos")
    parser.add_argument("--output", type=Path, required=True, help="Output directory for .npy tensors")
    args = parser.parse_args()

    run_batch_extraction(args.input, args.output)