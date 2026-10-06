import os
import sys
import time
from collections import Counter

import cv2

# Add project root to Python path.
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.insert(0, PROJECT_ROOT)

from backend.pose_engine import PoseEngine
from backend.yoga_analyzer import YogaAnalyzer
from backend.visualization import (
    draw_pose_landmarks,
    draw_analysis_overlay,
)


# --------------------------------------------------
# Test settings
# --------------------------------------------------

TEST_DURATION = 30

CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720


def main():
    print("=" * 60)
    print("YOGA MOTION AI - VISUAL LIVE TEST")
    print("=" * 60)

    print()
    print("Starting webcam...")
    print(f"Automatic test duration: {TEST_DURATION} seconds")
    print()
    print("The webcam window will display:")
    print("- MediaPipe pose skeleton")
    print("- Detected pose")
    print("- ML confidence")
    print("- Posture feedback")
    print()
    print("The test will stop automatically after 30 seconds.")
    print()

    # --------------------------------------------------
    # Initialize pose engine and analyzer
    # --------------------------------------------------

    pose_engine = PoseEngine()
    analyzer = YogaAnalyzer()

    # --------------------------------------------------
    # Open webcam
    # --------------------------------------------------

    camera = cv2.VideoCapture(0)

    camera.set(
        cv2.CAP_PROP_FRAME_WIDTH,
        CAMERA_WIDTH,
    )

    camera.set(
        cv2.CAP_PROP_FRAME_HEIGHT,
        CAMERA_HEIGHT,
    )

    if not camera.isOpened():
        print("ERROR: Could not open webcam.")
        pose_engine.close()
        return

    print("Webcam opened successfully.")
    print("Starting 30-second visual test...")
    print()

    # --------------------------------------------------
    # Counters
    # --------------------------------------------------

    total_frames = 0
    pose_frames = 0

    pose_predictions = Counter()

    tree_frames = 0
    correct_tree_frames = 0
    incorrect_tree_frames = 0

    feedback_counter = Counter()

    start_time = time.time()

    try:
        while True:
            # --------------------------------------------------
            # Check elapsed time
            # --------------------------------------------------

            elapsed_time = time.time() - start_time

            if elapsed_time >= TEST_DURATION:
                break

            # --------------------------------------------------
            # Read webcam frame
            # --------------------------------------------------

            success, frame = camera.read()

            if not success:
                print("WARNING: Could not read webcam frame.")
                continue

            total_frames += 1

            # --------------------------------------------------
            # Detect pose landmarks
            # --------------------------------------------------

            results = pose_engine.detect(frame)

            landmarks = pose_engine.get_landmarks(results)

            # --------------------------------------------------
            # Draw MediaPipe skeleton
            # --------------------------------------------------

            frame = draw_pose_landmarks(
                frame,
                results,
            )

            # --------------------------------------------------
            # Analyze pose
            # --------------------------------------------------

            if landmarks is not None:

                pose_frames += 1

                analysis = analyzer.analyze(
                    landmarks
                )

                pose = analysis["pose"]
                confidence = analysis["confidence"]
                posture = analysis["posture"]

                # Count ML predictions.
                if pose:
                    pose_predictions[pose] += 1

                # --------------------------------------------------
                # Tree Pose posture statistics
                # --------------------------------------------------

                if pose == "tree":

                    tree_frames += 1

                    if posture.get("correct", False):
                        correct_tree_frames += 1
                    else:
                        incorrect_tree_frames += 1

                    feedback_list = posture.get(
                        "feedback",
                        [],
                    )

                    for message in feedback_list:
                        feedback_counter[message] += 1

                # --------------------------------------------------
                # Draw analysis information
                # --------------------------------------------------

                feedback = posture.get(
                    "feedback",
                    [],
                )

                frame = draw_analysis_overlay(
                    frame,
                    pose,
                    confidence,
                    feedback,
                )

                # --------------------------------------------------
                # Display Tree Pose angle information
                # --------------------------------------------------

                if pose == "tree":

                    standing_leg = posture.get(
                        "standing_leg"
                    )

                    raised_leg = posture.get(
                        "raised_leg"
                    )

                    knee_angle = posture.get(
                        "knee_angle"
                    )

                    if standing_leg:
                        cv2.putText(
                            frame,
                            f"Standing leg: {standing_leg}",
                            (20, 270),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.65,
                            (255, 255, 255),
                            2,
                            cv2.LINE_AA,
                        )

                    if raised_leg:
                        cv2.putText(
                            frame,
                            f"Raised leg: {raised_leg}",
                            (20, 305),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.65,
                            (255, 255, 255),
                            2,
                            cv2.LINE_AA,
                        )

                    if knee_angle is not None:
                        cv2.putText(
                            frame,
                            f"Raised knee angle: {knee_angle:.1f} deg",
                            (20, 340),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.65,
                            (255, 255, 255),
                            2,
                            cv2.LINE_AA,
                        )

            else:

                # No pose detected.
                frame = draw_analysis_overlay(
                    frame,
                    None,
                    0.0,
                    ["No body detected."],
                )

            # --------------------------------------------------
            # Countdown display
            # --------------------------------------------------

            remaining = max(
                0,
                TEST_DURATION - int(elapsed_time),
            )

            cv2.putText(
                frame,
                f"Test time remaining: {remaining}s",
                (20, 680),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2,
                cv2.LINE_AA,
            )

            # --------------------------------------------------
            # Show webcam window
            # --------------------------------------------------

            cv2.imshow(
                "Yoga Motion AI - Live Analysis",
                frame,
            )

            # --------------------------------------------------
            # Optional early exit
            # --------------------------------------------------

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                print("Q pressed. Stopping early...")
                break

    except Exception as error:

        print()
        print("ERROR during live visual test:")
        print(error)

    finally:

        # --------------------------------------------------
        # Release resources
        # --------------------------------------------------

        camera.release()
        cv2.destroyAllWindows()
        pose_engine.close()

    # --------------------------------------------------
    # Final results
    # --------------------------------------------------

    print()
    print("=" * 60)
    print("VISUAL LIVE TEST COMPLETE")
    print("=" * 60)

    print(
        f"Total frames processed: {total_frames}"
    )

    print(
        f"Frames with pose: {pose_frames}"
    )

    if total_frames > 0:

        detection_percentage = (
            pose_frames / total_frames
        ) * 100

        print(
            f"Pose detection percentage: "
            f"{detection_percentage:.1f}%"
        )

    print()
    print("ML pose predictions:")

    if pose_predictions:

        for pose_name, count in pose_predictions.most_common():

            percentage = (
                count / pose_frames
            ) * 100 if pose_frames else 0

            print(
                f"{pose_name:<20}"
                f"{count:>6} frames "
                f"({percentage:.1f}%)"
            )

    else:

        print("No poses detected.")

    print()

    print(
        f"Tree Pose frames: {tree_frames}"
    )

    if tree_frames > 0:

        print(
            f"Correct Tree Pose frames: "
            f"{correct_tree_frames}"
        )

        print(
            f"Incorrect Tree Pose frames: "
            f"{incorrect_tree_frames}"
        )

        correct_percentage = (
            correct_tree_frames
            / tree_frames
        ) * 100

        print(
            f"Correct Tree Pose percentage: "
            f"{correct_percentage:.1f}%"
        )

    print()

    print("Posture feedback detected:")

    if feedback_counter:

        for message, count in feedback_counter.most_common():

            print(
                f"{message}: {count} frames"
            )

    else:

        print("No posture feedback recorded.")

    print()
    print(
        "RESULT: VISUAL ML + POSTURE TEST COMPLETE"
    )
    print("=" * 60)


if __name__ == "__main__":
    main()