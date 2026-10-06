import os
import sys

import cv2
import mediapipe as mp

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

OUTPUT_IMAGE = os.path.join(
    PROJECT_ROOT,
    "datasets",
    "sample",
    "test_person_landmarks.jpg",
)


def main():
    image = cv2.imread(INPUT_IMAGE)

    if image is None:
        raise FileNotFoundError(
            f"Could not load image: {INPUT_IMAGE}"
        )

    engine = PoseEngine()
    results = engine.detect(image)

    if results.pose_landmarks is None:
        print("No human pose detected.")
        engine.close()
        return

    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
    )

    success = cv2.imwrite(OUTPUT_IMAGE, image)

    if not success:
        raise RuntimeError(
            f"Could not save output image: {OUTPUT_IMAGE}"
        )

    print("POSE VISUALIZATION CREATED SUCCESSFULLY")
    print("Input :", INPUT_IMAGE)
    print("Output:", OUTPUT_IMAGE)
    print("Landmarks:", len(results.pose_landmarks.landmark))

    engine.close()


if __name__ == "__main__":
    main()