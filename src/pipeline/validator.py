"""Dataset integrity and landmark extraction validator module."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, Dict

import cv2
import mediapipe as mp


class DatasetValidator:
    """Validates video container integrity and skeletal landmark extraction."""

    SUPPORTED_EXTENSIONS = {".mp4", ".avi", ".mov", ".mkv"}

    def __init__(self, min_detection_confidence: float = 0.5):
        self.mp_holistic = mp.solutions.holistic
        self.holistic = self.mp_holistic.Holistic(
            static_image_mode=False,
            model_complexity=1,
            smooth_landmarks=True,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=0.5,
        )

    def verify_video_integrity(self, video_path: Path) -> Dict[str, Any]:
        """Checks if a video file can be opened and decoded properly."""
        if not video_path.exists():
            return {"valid": False, "error": f"File not found: {video_path}"}

        if video_path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
            return {
                "valid": False,
                "error": f"Unsupported extension: {video_path.suffix}",
            }

        cap = cv2.VideoCapture(str(video_path))
        if not cap.isOpened():
            return {"valid": False, "error": "Failed to open video container."}

        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Attempt decoding the first frame
        ret, frame = cap.read()
        cap.release()

        if not ret or frame is None:
            return {"valid": False, "error": "Corrupted stream: Unable to decode first frame."}

        return {
            "valid": True,
            "fps": fps,
            "frame_count": frame_count,
            "resolution": (width, height),
        }

    def test_landmark_extraction(self, video_path: Path, max_frames: int = 30) -> Dict[str, Any]:
        """Tests sample landmark extraction on the initial frames of a video."""
        integrity_check = self.verify_video_integrity(video_path)
        if not integrity_check["valid"]:
            return integrity_check

        cap = cv2.VideoCapture(str(video_path))
        frames_processed = 0
        landmarks_detected_count = 0

        while cap.isOpened() and frames_processed < max_frames:
            ret, frame = cap.read()
            if not ret:
                break

            # Convert BGR to RGB for MediaPipe
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            rgb_frame.flags.writeable = False
            results = self.holistic.process(rgb_frame)

            # Check for pose or hands keypoints
            has_landmarks = any(
                [
                    results.pose_landmarks is not None,
                    results.left_hand_landmarks is not None,
                    results.right_hand_landmarks is not None,
                ]
            )

            if has_landmarks:
                landmarks_detected_count += 1

            frames_processed += 1

        cap.release()

        return {
            "valid": True,
            "frames_tested": frames_processed,
            "frames_with_landmarks": landmarks_detected_count,
            "detection_rate": (
                landmarks_detected_count / frames_processed if frames_processed > 0 else 0.0
            ),
        }

    def close(self):
        """Release MediaPipe resources."""
        self.holistic.close()


def main():
    parser = argparse.ArgumentParser(description="Echo-Sync Dataset Ingestion & Validation Module")
    parser.add_argument(
        "--video",
        type=str,
        help="Path to an individual video file to validate",
        required=False,
    )
    args = parser.parse_args()

    validator = DatasetValidator()

    if args.video:
        path = Path(args.video)
        print(f"[*] Validating: {path}")
        report = validator.test_landmark_extraction(path)
        print(f"[+] Result: {report}")
    else:
        print("[*] Validator initialized successfully. Pass --video <path> to test a sample file.")

    validator.close()


if __name__ == "__main__":
    main()