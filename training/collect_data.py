import csv
import os
import sys
import time

import cv2
import mediapipe as mp

# Add project root to Python path.
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.insert(0, PROJECT_ROOT)

from backend.features import extract_features
from backend.pose_engine import PoseEngine


DATASET_FILE = os.path.join(
    PROJECT_ROOT,
    "datasets",
    "processed",
    "yoga_pose_dataset.csv",
)


POSES = {
    "1": "mountain",
    "2": "raised_hands",
    "3": "warrior_ii",
    "4": "tree",
    "5": "t_pose",
    "6": "hands_on_hips",
    "7": "side_stretch",
    "8": "chair",
    "9": "forward_bend",
    "10": "wide_leg_standing",
}


SAMPLES_PER_POSE = 50


def create_dataset_file_if_needed():
    """
    Create the dataset CSV only if it does not already exist.
    This prevents previously collected data from being deleted.
    """

    os.makedirs(
        os.path.dirname(DATASET_FILE),
        exist_ok=True,
    )

    if os.path.exists(DATASET_FILE):
        return

    feature_columns = [
        f"feature_{index}"
        for index in range(132)
    ]

    header = feature_columns + ["label"]

    with open(
        DATASET_FILE,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.writer(file)
        writer.writerow(header)


def append_sample(features, label):
    """Save one feature vector and its pose label."""

    with open(
        DATASET_FILE,
        "a",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.writer(file)

        row = list(features) + [label]

        writer.writerow(row)


def collect_pose_samples(
    pose_name,
    target_samples=SAMPLES_PER_POSE,
):
    """
    Collect real webcam samples for one yoga pose.
    """

    print()
    print("=" * 60)
    print(f"COLLECTING: {pose_name.upper()}")
    print("=" * 60)

    print()
    print(f"Target samples: {target_samples}")
    print()
    print("Instructions:")
    print("1. Stand where your whole body is visible.")
    print("2. Perform the selected pose.")
    print("3. Hold the pose naturally.")
    print("4. Move slightly while collecting samples.")
    print("5. Press Q to stop early.")
    print()

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        raise RuntimeError(
            "Could not open the webcam."
        )

    engine = PoseEngine()

    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    sample_count = 0
    last_capture_time = 0.0

    try:

        while sample_count < target_samples:

            success, frame = camera.read()

            if not success:
                print("Could not read webcam frame.")
                continue

            results = engine.detect(frame)
            landmarks = engine.get_landmarks(results)

            display_frame = frame.copy()

            if landmarks is not None:

                # Draw the 33-point pose skeleton.
                mp_drawing.draw_landmarks(
                    display_frame,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                )

                current_time = time.time()

                # Save approximately one sample every 0.20 seconds.
                if (
                    current_time - last_capture_time
                    >= 0.20
                ):

                    features = extract_features(
                        landmarks
                    )

                    append_sample(
                        features,
                        pose_name,
                    )

                    sample_count += 1
                    last_capture_time = current_time

            # Display status.
            if landmarks is not None:

                status = "POSE DETECTED"

                cv2.putText(
                    display_frame,
                    status,
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (0, 255, 0),
                    2,
                )

            else:

                status = "NO POSE DETECTED"

                cv2.putText(
                    display_frame,
                    status,
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (0, 0, 255),
                    2,
                )

            cv2.putText(
                display_frame,
                f"Pose: {pose_name}",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2,
            )

            cv2.putText(
                display_frame,
                f"Samples: {sample_count}/{target_samples}",
                (20, 120),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2,
            )

            cv2.putText(
                display_frame,
                "Press Q to stop",
                (20, 160),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2,
            )

            cv2.imshow(
                "Yoga Motion AI - Dataset Collection",
                display_frame,
            )

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:

        camera.release()
        engine.close()
        cv2.destroyAllWindows()

    print()
    print(
        f"Collected {sample_count} samples "
        f"for {pose_name}."
    )


def main():

    print()
    print("=" * 60)
    print("YOGA MOTION AI - DATASET COLLECTION")
    print("=" * 60)

    create_dataset_file_if_needed()

    print()
    print("Select the yoga pose:")
    print()

    for key, pose in POSES.items():
        print(f"{key}. {pose}")

    print()

    choice = input(
        "Enter your choice (1-10): "
    ).strip()

    if choice not in POSES:
        print("Invalid choice.")
        return

    pose_name = POSES[choice]

    collect_pose_samples(
        pose_name,
        SAMPLES_PER_POSE,
    )

    print()
    print("Dataset location:")
    print(DATASET_FILE)


if __name__ == "__main__":
    main()