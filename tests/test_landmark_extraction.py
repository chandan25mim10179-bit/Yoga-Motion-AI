import os
import sys

import cv2

# Add the project root directory to Python's module search path.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from backend.pose_engine import PoseEngine


INPUT_IMAGE = os.path.join(
    PROJECT_ROOT,
    "datasets",
    "sample",
    "test_person.jpg",
)


def main():
    image = cv2.imread(INPUT_IMAGE)

    if image is None:
        raise FileNotFoundError(
            f"Could not load image: {INPUT_IMAGE}"
        )

    engine = PoseEngine()
    results = engine.detect(image)
    landmarks = engine.get_landmarks(results)

    if landmarks is None:
        print("No pose detected.")
        engine.close()
        return

    print()
    print("LANDMARK EXTRACTION SUCCESSFUL")
    print("=" * 50)
    print(f"Total landmarks: {len(landmarks)}")
    print()

    for index, landmark in enumerate(landmarks):
        print(
            f"{index:02d} | "
            f"x={landmark.x:.4f} | "
            f"y={landmark.y:.4f} | "
            f"z={landmark.z:.4f} | "
            f"visibility={landmark.visibility:.4f}"
        )

    engine.close()


if __name__ == "__main__":
    main()