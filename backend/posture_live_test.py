import os
import sys
import cv2
import time

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.insert(0, PROJECT_ROOT)

from backend.pose_engine import PoseEngine
from backend.posture_analyzer import analyze_tree_pose


TEST_DURATION = 30

def main():
    print("Starting automatic 30-second Tree Pose posture test...")
    print("Stand in front of the camera and perform Tree Pose.")
    print("The test will stop automatically after 30 seconds.")

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("ERROR: Could not open webcam.")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    engine = PoseEngine()

    total_frames = 0
    pose_frames = 0

    correct_frames = 0
    incorrect_frames = 0

    feedback_counts = {}

    start_time = time.time()

    try:
        while True:
            elapsed_time = time.time() - start_time

            if elapsed_time >= TEST_DURATION:
                break

            success, frame = cap.read()

            if not success:
                print("WARNING: Could not read webcam frame.")
                continue

            total_frames += 1

            results = engine.detect(frame)
            landmarks = engine.get_landmarks(results)

            if landmarks is not None:
                pose_frames += 1

                analysis = analyze_tree_pose(landmarks)

                if analysis["correct"]:
                    correct_frames += 1
                else:
                    incorrect_frames += 1

                for message in analysis["feedback"]:
                    feedback_counts[message] = (
                        feedback_counts.get(message, 0) + 1
                    )

                cv2.putText(
                    frame,
                    f"Standing leg: {analysis['standing_leg']}",
                    (30, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (255, 255, 255),
                    2,
                )

                cv2.putText(
                    frame,
                    f"Raised leg: {analysis['raised_leg']}",
                    (30, 75),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (255, 255, 255),
                    2,
                )

                cv2.putText(
                    frame,
                    f"Knee angle: {analysis['knee_angle']}",
                    (30, 110),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (255, 255, 255),
                    2,
                )

                y_position = 155

                for message in analysis["feedback"]:
                    cv2.putText(
                        frame,
                        message,
                        (30, y_position),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.65,
                        (255, 255, 255),
                        2,
                    )

                    y_position += 35

            else:
                cv2.putText(
                    frame,
                    "No body detected.",
                    (30, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (255, 255, 255),
                    2,
                )

            remaining = max(
                0,
                TEST_DURATION - int(elapsed_time),
            )

            cv2.putText(
                frame,
                f"Time remaining: {remaining}s",
                (30, 700),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2,
            )

            cv2.imshow(
                "Yoga Motion AI - Tree Pose Analyzer",
                frame,
            )

            # Keep the window responsive.
            cv2.waitKey(1)

    finally:
        cap.release()
        engine.close()
        cv2.destroyAllWindows()

    print()
    print("=" * 50)
    print("30-SECOND TREE POSE POSTURE TEST COMPLETE")
    print("=" * 50)

    print(f"Total frames processed: {total_frames}")
    print(f"Frames with pose: {pose_frames}")

    if total_frames > 0:
        detection_percentage = (
            pose_frames / total_frames
        ) * 100

        print(
            f"Pose detection percentage: "
            f"{detection_percentage:.1f}%"
        )

    print(f"Correct posture frames: {correct_frames}")
    print(f"Incorrect posture frames: {incorrect_frames}")

    if pose_frames > 0:
        correct_percentage = (
            correct_frames / pose_frames
        ) * 100

        print(
            f"Correct posture percentage: "
            f"{correct_percentage:.1f}%"
        )

    print()
    print("Feedback detected during test:")

    if feedback_counts:
        sorted_feedback = sorted(
            feedback_counts.items(),
            key=lambda item: item[1],
            reverse=True,
        )

        for message, count in sorted_feedback:
            print(f"{message}: {count} frames")

    else:
        print("No feedback recorded.")

    print()
    print("RESULT: AUTOMATIC LIVE POSTURE TEST COMPLETE")


if __name__ == "__main__":
    main()