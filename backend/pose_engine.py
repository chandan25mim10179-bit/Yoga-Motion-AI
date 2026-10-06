import cv2
import mediapipe as mp
import numpy as np


class PoseEngine:
    """Detect human body pose landmarks using MediaPipe."""

    def __init__(
        self,
        static_image_mode: bool = False,
        model_complexity: int = 1,
        min_detection_confidence: float = 0.5,
        min_tracking_confidence: float = 0.5,
    ):
        self.mp_pose = mp.solutions.pose

        self.pose = self.mp_pose.Pose(
            static_image_mode=static_image_mode,
            model_complexity=model_complexity,
            enable_segmentation=False,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )

    def detect(self, image: np.ndarray):
        """
        Detect pose landmarks from a BGR OpenCV image.

        Args:
            image: OpenCV BGR image.

        Returns:
            MediaPipe pose detection result.
        """
        if image is None:
            raise ValueError("Input image cannot be None.")

        if not isinstance(image, np.ndarray):
            raise ValueError("Input image must be a NumPy array.")

        if image.ndim != 3 or image.shape[2] != 3:
            raise ValueError("Input image must be a 3-channel BGR image.")

        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        rgb_image.flags.writeable = False

        results = self.pose.process(rgb_image)

        return results

    def get_landmarks(self, results):
        """
        Extract pose landmarks from MediaPipe results.

        Returns:
            List of 33 landmarks, or None if no pose is detected.
        """
        if results is None or results.pose_landmarks is None:
            return None

        return results.pose_landmarks.landmark

    def close(self):
        """Release the MediaPipe pose detector."""
        self.pose.close()
