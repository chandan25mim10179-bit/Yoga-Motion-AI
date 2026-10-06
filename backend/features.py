import numpy as np


# MediaPipe Pose landmark indices
NOSE = 0

LEFT_SHOULDER = 11
RIGHT_SHOULDER = 12

LEFT_ELBOW = 13
RIGHT_ELBOW = 14

LEFT_WRIST = 15
RIGHT_WRIST = 16

LEFT_HIP = 23
RIGHT_HIP = 24

LEFT_KNEE = 25
RIGHT_KNEE = 26

LEFT_ANKLE = 27
RIGHT_ANKLE = 28

LEFT_HEEL = 29
RIGHT_HEEL = 30

LEFT_FOOT_INDEX = 31
RIGHT_FOOT_INDEX = 32


def landmarks_to_array(landmarks):
    """
    Convert MediaPipe landmarks into a NumPy array.

    Output shape:
        (33, 4)

    Columns:
        x, y, z, visibility
    """

    if landmarks is None:
        raise ValueError("Landmarks cannot be None.")

    if len(landmarks) != 33:
        raise ValueError(
            f"Expected 33 landmarks, received {len(landmarks)}."
        )

    data = []

    for landmark in landmarks:
        data.append(
            [
                landmark.x,
                landmark.y,
                landmark.z,
                landmark.visibility,
            ]
        )

    return np.asarray(data, dtype=np.float32)


def normalize_landmarks(landmarks_array):
    """
    Normalize landmark coordinates so that the feature representation
    is less dependent on the person's position and distance from camera.

    The midpoint between the left and right hips is used as the body
    reference point.

    Body scale is estimated from the distance between the shoulders
    and hips.
    """

    if landmarks_array.shape != (33, 4):
        raise ValueError(
            "Expected landmark array with shape (33, 4)."
        )

    coordinates = landmarks_array[:, :3].copy()

    # Body center: midpoint between left and right hips.
    hip_center = (
        coordinates[LEFT_HIP] + coordinates[RIGHT_HIP]
    ) / 2.0

    # Shoulder center.
    shoulder_center = (
        coordinates[LEFT_SHOULDER]
        + coordinates[RIGHT_SHOULDER]
    ) / 2.0

    # Estimate body scale using shoulder-to-hip distance.
    body_scale = np.linalg.norm(
        shoulder_center - hip_center
    )

    # Prevent division by zero.
    if body_scale < 1e-6:
        body_scale = 1.0

    normalized = (
        coordinates - hip_center
    ) / body_scale

    return normalized


def extract_features(landmarks):
    """
    Convert 33 MediaPipe landmarks into an ML-ready feature vector.

    Features include:
        - normalized x, y, z coordinates
        - landmark visibility

    Output:
        NumPy array with 132 features.
    """

    landmark_array = landmarks_to_array(landmarks)

    normalized_coordinates = normalize_landmarks(
        landmark_array
    )

    visibility = landmark_array[:, 3].reshape(-1, 1)

    features = np.concatenate(
        [
            normalized_coordinates,
            visibility,
        ],
        axis=1,
    )

    return features.flatten().astype(np.float32)
