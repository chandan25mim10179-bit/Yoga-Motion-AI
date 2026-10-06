import cv2
import mediapipe as mp


# MediaPipe drawing utilities
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


def draw_pose_landmarks(image, results):
    """
    Draw MediaPipe pose landmarks and body connections
    on the webcam image.

    Args:
        image: OpenCV BGR image.
        results: MediaPipe pose detection results.

    Returns:
        Image with pose landmarks drawn on it.
    """

    if image is None:
        raise ValueError("Image cannot be None.")

    if results is None:
        return image

    if results.pose_landmarks is not None:
        mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(
                color=(0, 255, 0),
                thickness=2,
                circle_radius=3,
            ),
            mp_drawing.DrawingSpec(
                color=(255, 255, 255),
                thickness=2,
            ),
        )

    return image


def draw_text(
    image,
    text,
    position,
    font_scale=0.7,
    thickness=2,
):
    """
    Draw readable text on the webcam image.
    """

    if image is None:
        raise ValueError("Image cannot be None.")

    cv2.putText(
        image,
        str(text),
        position,
        cv2.FONT_HERSHEY_SIMPLEX,
        font_scale,
        (255, 255, 255),
        thickness,
        cv2.LINE_AA,
    )

    return image


def draw_analysis_overlay(
    image,
    pose,
    confidence,
    feedback,
):
    """
    Display pose classification and posture feedback
    on the webcam image.
    """

    if image is None:
        raise ValueError("Image cannot be None.")

    # Main pose information.
    draw_text(
        image,
        f"Pose: {pose if pose else 'No pose'}",
        (20, 40),
        font_scale=0.8,
        thickness=2,
    )

    draw_text(
        image,
        f"Confidence: {confidence * 100:.1f}%",
        (20, 75),
        font_scale=0.7,
        thickness=2,
    )

    # Feedback section.
    draw_text(
        image,
        "Feedback:",
        (20, 120),
        font_scale=0.7,
        thickness=2,
    )

    if feedback:
        for index, message in enumerate(feedback[:3]):
            draw_text(
                image,
                f"- {message}",
                (20, 155 + index * 35),
                font_scale=0.6,
                thickness=2,
            )

    return image