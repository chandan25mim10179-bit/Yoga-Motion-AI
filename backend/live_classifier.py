import os
import sys
import time

import cv2
import joblib
import mediapipe as mp
import pandas as pd


PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.insert(0, PROJECT_ROOT)


from backend.features import extract_features
from backend.pose_engine import PoseEngine


MODEL_FILE = os.path.join(
    PROJECT_ROOT,
    "models",
    "yoga_pose_classifier.joblib",
)

LABEL_ENCODER_FILE = os.path.join(
    PROJECT_ROOT,
    "models",
    "label_encoder.joblib",
)


FEATURE_COLUMNS = [
    f"feature_{index}"
    for index in range(132)
]


# Automatic test duration.
TEST_DURATION_SECONDS = 30


def main():

    print()
    print("=" * 60)
    print("YOGA MOTION AI - AUTOMATIC LIVE ML TEST")
    print("=" * 60)

    # --------------------------------------------------
    # Load trained ML model
    # --------------------------------------------------

    print()
    print("Loading trained ML model...")

    if not os.path.exists(MODEL_FILE):
        raise FileNotFoundError(
            f"Model not found: {MODEL_FILE}"
        )

    model = joblib.load(MODEL_FILE)

    print("Loading label encoder...")

    if not os.path.exists(LABEL_ENCODER_FILE):
        raise FileNotFoundError(
            f"Label encoder not found: {LABEL_ENCODER_FILE}"
        )

    label_encoder = joblib.load(
        LABEL_ENCODER_FILE
    )

    # --------------------------------------------------
    # Start MediaPipe
    # --------------------------------------------------

    print("Starting MediaPipe pose detection...")

    engine = PoseEngine()

    # --------------------------------------------------
    # Open webcam
    # --------------------------------------------------

    print("Opening webcam...")

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():

        engine.close()

        raise RuntimeError(
            "Could not open webcam."
        )

    # Set webcam resolution.
    camera.set(
        cv2.CAP_PROP_FRAME_WIDTH,
        1280
    )

    camera.set(
        cv2.CAP_PROP_FRAME_HEIGHT,
        720
    )

    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    print()
    print("=" * 60)
    print("30-SECOND AUTOMATIC TEST STARTED")
    print("=" * 60)

    print()
    print("Perform one of the 10 trained yoga poses.")
    print()
    print("The test will automatically stop after 30 seconds.")
    print("You do NOT need to press Q.")
    print()
    print("Press Q only if you want to stop early.")
    print()

    # --------------------------------------------------
    # Test statistics
    # --------------------------------------------------

    frame_count = 0
    pose_count = 0

    prediction_history = []

    start_time = time.time()

    try:

        while True:

            # --------------------------------------------------
            # Calculate remaining time
            # --------------------------------------------------

            elapsed_time = time.time() - start_time

            remaining_time = max(
                0,
                TEST_DURATION_SECONDS - elapsed_time
            )

            # Automatically stop after 30 seconds.
            if elapsed_time >= TEST_DURATION_SECONDS:
                break

            # --------------------------------------------------
            # Read webcam frame
            # --------------------------------------------------

            success, frame = camera.read()

            if not success:
                continue

            frame_count += 1

            # --------------------------------------------------
            # Detect pose
            # --------------------------------------------------

            results = engine.detect(frame)

            landmarks = engine.get_landmarks(
                results
            )

            display_frame = frame.copy()

            predicted_pose = None
            confidence = 0.0

            # --------------------------------------------------
            # Pose detected
            # --------------------------------------------------

            if landmarks is not None:

                pose_count += 1

                # Draw skeleton.
                mp_drawing.draw_landmarks(
                    display_frame,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                )

                # Extract 132 features.
                features = extract_features(
                    landmarks
                )

                # Convert features into DataFrame
                # using the same feature names as training.
                features_for_model = pd.DataFrame(
                    [features],
                    columns=FEATURE_COLUMNS,
                )

                # --------------------------------------------------
                # ML prediction
                # --------------------------------------------------

                probabilities = model.predict_proba(
                    features_for_model
                )[0]

                best_index = probabilities.argmax()

                prediction_encoded = (
                    model.classes_[best_index]
                )

                predicted_pose = (
                    label_encoder.inverse_transform(
                        [prediction_encoded]
                    )[0]
                )

                confidence = (
                    probabilities[best_index] * 100
                )

                # Save prediction history.
                prediction_history.append(
                    predicted_pose
                )

                # --------------------------------------------------
                # Display prediction
                # --------------------------------------------------

                cv2.putText(
                    display_frame,
                    f"Pose: {predicted_pose}",
                    (20, 45),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (0, 255, 0),
                    2,
                )

                cv2.putText(
                    display_frame,
                    f"Confidence: {confidence:.1f}%",
                    (20, 85),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (255, 255, 255),
                    2,
                )

                cv2.putText(
                    display_frame,
                    "POSE DETECTED",
                    (20, 125),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2,
                )

            # --------------------------------------------------
            # No pose detected
            # --------------------------------------------------

            else:

                cv2.putText(
                    display_frame,
                    "No pose detected",
                    (20, 45),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (0, 0, 255),
                    2,
                )

                cv2.putText(
                    display_frame,
                    "Keep your full body visible",
                    (20, 85),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 255, 255),
                    2,
                )

            # --------------------------------------------------
            # Display countdown
            # --------------------------------------------------

            cv2.putText(
                display_frame,
                f"Time left: {remaining_time:.1f}s",
                (20, 165),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2,
            )

            cv2.putText(
                display_frame,
                "Automatic test: 30 seconds",
                (20, 200),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2,
            )

            # --------------------------------------------------
            # Show webcam
            # --------------------------------------------------

            cv2.imshow(
                "Yoga Motion AI - 30 Second Automatic Test",
                display_frame,
            )

            # --------------------------------------------------
            # Optional early exit
            # --------------------------------------------------

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                print()
                print("Q pressed. Stopping test early.")
                break

    finally:

        camera.release()
        engine.close()
        cv2.destroyAllWindows()

    # --------------------------------------------------
    # Final results
    # --------------------------------------------------

    print()
    print("=" * 60)
    print("30-SECOND AUTOMATIC TEST COMPLETE")
    print("=" * 60)

    print()
    print(f"Total frames processed: {frame_count}")
    print(f"Frames with pose: {pose_count}")

    if prediction_history:

        prediction_series = pd.Series(
            prediction_history
        )

        most_common_pose = (
            prediction_series
            .value_counts()
            .idxmax()
        )

        most_common_count = (
            prediction_series
            .value_counts()
            .max()
        )

        total_predictions = len(
            prediction_history
        )

        percentage = (
            most_common_count
            / total_predictions
            * 100
        )

        print()
        print(
            f"Most detected pose: {most_common_pose}"
        )

        print(
            f"Pose detections for this pose: "
            f"{most_common_count}/{total_predictions}"
        )

        print(
            f"Detection percentage: {percentage:.1f}%"
        )

        print()
        print("All detected poses:")

        print(
            prediction_series.value_counts()
        )

    else:

        print()
        print(
            "No pose predictions were recorded."
        )

    print()
    print("=" * 60)
    print("RESULT: AUTOMATIC LIVE ML TEST COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()