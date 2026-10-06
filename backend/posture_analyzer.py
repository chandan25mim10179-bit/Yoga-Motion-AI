import math


# --------------------------------------------------
# MediaPipe landmark indices
# --------------------------------------------------

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


def calculate_angle(point_a, point_b, point_c):
    """
    Calculate the angle at point_b.

    The angle is formed by:
        point_a -> point_b -> point_c

    Args:
        point_a: (x, y)
        point_b: (x, y)
        point_c: (x, y)

    Returns:
        Angle in degrees.
    """

    ax, ay = point_a
    bx, by = point_b
    cx, cy = point_c

    vector_ba = (
        ax - bx,
        ay - by,
    )

    vector_bc = (
        cx - bx,
        cy - by,
    )

    dot_product = (
        vector_ba[0] * vector_bc[0]
        + vector_ba[1] * vector_bc[1]
    )

    magnitude_ba = math.sqrt(
        vector_ba[0] ** 2
        + vector_ba[1] ** 2
    )

    magnitude_bc = math.sqrt(
        vector_bc[0] ** 2
        + vector_bc[1] ** 2
    )

    if magnitude_ba == 0 or magnitude_bc == 0:
        return 0.0

    cosine_angle = (
        dot_product
        / (magnitude_ba * magnitude_bc)
    )

    cosine_angle = max(
        -1.0,
        min(1.0, cosine_angle),
    )

    angle = math.degrees(
        math.acos(cosine_angle)
    )

    return angle


def landmark_point(landmark):
    """
    Convert a MediaPipe landmark into an (x, y) point.
    """

    return (
        landmark.x,
        landmark.y,
    )


def analyze_tree_pose(landmarks):
    """
    Analyze a Tree Pose using MediaPipe landmarks.

    The function automatically determines which leg
    appears to be the standing leg.

    Returns:
        Dictionary containing:
        - correct
        - standing_leg
        - raised_leg
        - knee_angle
        - feedback
    """

    if landmarks is None:
        return {
            "correct": False,
            "standing_leg": None,
            "raised_leg": None,
            "knee_angle": None,
            "feedback": [
                "No body detected."
            ],
        }

    # --------------------------------------------------
    # Get important body points
    # --------------------------------------------------

    left_hip = landmark_point(
        landmarks[LEFT_HIP]
    )

    right_hip = landmark_point(
        landmarks[RIGHT_HIP]
    )

    left_knee = landmark_point(
        landmarks[LEFT_KNEE]
    )

    right_knee = landmark_point(
        landmarks[RIGHT_KNEE]
    )

    left_ankle = landmark_point(
        landmarks[LEFT_ANKLE]
    )

    right_ankle = landmark_point(
        landmarks[RIGHT_ANKLE]
    )

    # --------------------------------------------------
    # Determine which leg is raised.
    #
    # In image coordinates, a smaller y value means
    # the point is higher on the screen.
    # --------------------------------------------------

    left_ankle_height = left_ankle[1]
    right_ankle_height = right_ankle[1]

    if left_ankle_height < right_ankle_height:

        raised_leg = "left"
        standing_leg = "right"

        raised_hip = left_hip
        raised_knee = left_knee
        raised_ankle = left_ankle

        standing_hip = right_hip
        standing_knee = right_knee
        standing_ankle = right_ankle

    else:

        raised_leg = "right"
        standing_leg = "left"

        raised_hip = right_hip
        raised_knee = right_knee
        raised_ankle = right_ankle

        standing_hip = left_hip
        standing_knee = left_knee
        standing_ankle = left_ankle

    # --------------------------------------------------
    # Calculate raised-leg knee angle.
    # --------------------------------------------------

    knee_angle = calculate_angle(
        raised_hip,
        raised_knee,
        raised_ankle,
    )

    # --------------------------------------------------
    # Check whether the standing leg is reasonably
    # straight.
    # --------------------------------------------------

    standing_knee_angle = calculate_angle(
        standing_hip,
        standing_knee,
        standing_ankle,
    )

    # --------------------------------------------------
    # Check whether raised foot is sufficiently
    # above the standing ankle.
    # --------------------------------------------------

    foot_height_difference = (
        standing_ankle[1]
        - raised_ankle[1]
    )

    feedback = []

    # --------------------------------------------------
    # Raised knee check
    # --------------------------------------------------

    if knee_angle > 120:

        feedback.append(
            "Bend your raised knee more."
        )

    # --------------------------------------------------
    # Standing leg check
    # --------------------------------------------------

    if standing_knee_angle < 160:

        feedback.append(
            "Straighten your standing leg."
        )

    # --------------------------------------------------
    # Raised foot check
    # --------------------------------------------------

    if foot_height_difference < 0.05:

        feedback.append(
            "Lift your raised foot higher."
        )

    # --------------------------------------------------
    # Final result
    # --------------------------------------------------

    correct = len(feedback) == 0

    if correct:

        feedback.append(
            "Good Tree Pose!"
        )

    return {
        "correct": correct,
        "standing_leg": standing_leg,
        "raised_leg": raised_leg,
        "knee_angle": round(
            knee_angle,
            1,
        ),
        "standing_knee_angle": round(
            standing_knee_angle,
            1,
        ),
        "feedback": feedback,
    }

def analyze_t_pose(landmarks):
    """Analyze T Pose posture using shoulder, elbow, and wrist alignment."""

    left_shoulder = landmark_point(landmarks[11])
    right_shoulder = landmark_point(landmarks[12])
    left_elbow = landmark_point(landmarks[13])
    right_elbow = landmark_point(landmarks[14])
    left_wrist = landmark_point(landmarks[15])
    right_wrist = landmark_point(landmarks[16])

    # Check whether both arms are approximately horizontal.
    left_arm_slope = abs(left_wrist[1] - left_shoulder[1])
    right_arm_slope = abs(right_wrist[1] - right_shoulder[1])

    # Check whether both elbows are reasonably straight.
    left_elbow_angle = calculate_angle(
        left_shoulder,
        left_elbow,
        left_wrist,
    )

    right_elbow_angle = calculate_angle(
        right_shoulder,
        right_elbow,
        right_wrist,
    )

    feedback = []

    if left_arm_slope > 0.12:
        feedback.append(
            "Raise or lower your left arm until it is more horizontal."
        )

    if right_arm_slope > 0.12:
        feedback.append(
            "Raise or lower your right arm until it is more horizontal."
        )

    if left_elbow_angle < 150:
        feedback.append(
            "Straighten your left elbow."
        )

    if right_elbow_angle < 150:
        feedback.append(
            "Straighten your right elbow."
        )

    if not feedback:
        feedback.append(
            "Good T Pose! Keep both arms extended and horizontal."
        )

    return {
        "correct": len(feedback) == 1 and feedback[0].startswith("Good T Pose"),
        "feedback": feedback,
        "measurements": {
            "left_elbow_angle": round(left_elbow_angle, 1),
            "right_elbow_angle": round(right_elbow_angle, 1),
            "left_arm_slope": round(left_arm_slope, 3),
            "right_arm_slope": round(right_arm_slope, 3),
        },
    }

def analyze_mountain_pose(landmarks):
    """Analyze Mountain Pose posture using MediaPipe landmarks."""

    if landmarks is None:
        return {
            "correct": False,
            "feedback": ["No body detected."],
            "measurements": {},
        }

    left_shoulder = landmark_point(landmarks[LEFT_SHOULDER])
    right_shoulder = landmark_point(landmarks[RIGHT_SHOULDER])

    left_hip = landmark_point(landmarks[LEFT_HIP])
    right_hip = landmark_point(landmarks[RIGHT_HIP])

    left_knee = landmark_point(landmarks[LEFT_KNEE])
    right_knee = landmark_point(landmarks[RIGHT_KNEE])

    left_ankle = landmark_point(landmarks[LEFT_ANKLE])
    right_ankle = landmark_point(landmarks[RIGHT_ANKLE])

    feedback = []

    # Check whether both knees are reasonably straight.
    left_knee_angle = calculate_angle(
        left_hip,
        left_knee,
        left_ankle,
    )

    right_knee_angle = calculate_angle(
        right_hip,
        right_knee,
        right_ankle,
    )

    if left_knee_angle < 165:
        feedback.append(
            "Straighten your left leg."
        )

    if right_knee_angle < 165:
        feedback.append(
            "Straighten your right leg."
        )

    # Check shoulder balance.
    shoulder_height_difference = abs(
        left_shoulder[1] - right_shoulder[1]
    )

    if shoulder_height_difference > 0.08:
        feedback.append(
            "Keep both shoulders level."
        )

    # Check hip balance.
    hip_height_difference = abs(
        left_hip[1] - right_hip[1]
    )

    if hip_height_difference > 0.08:
        feedback.append(
            "Keep both hips level."
        )

    if not feedback:
        feedback.append(
            "Good Mountain Pose! Keep your body tall and balanced."
        )

    return {
        "correct": len(feedback) == 1
        and feedback[0].startswith("Good Mountain Pose"),
        "feedback": feedback,
        "measurements": {
            "left_knee_angle": round(left_knee_angle, 1),
            "right_knee_angle": round(right_knee_angle, 1),
            "shoulder_height_difference": round(
                shoulder_height_difference,
                3,
            ),
            "hip_height_difference": round(
                hip_height_difference,
                3,
            ),
        },
    }

def analyze_raised_hands_pose(landmarks):
    """Analyze Raised Hands Pose posture using MediaPipe landmarks."""

    if landmarks is None:
        return {
            "correct": False,
            "feedback": ["No body detected."],
            "measurements": {},
        }

    left_shoulder = landmark_point(landmarks[LEFT_SHOULDER])
    right_shoulder = landmark_point(landmarks[RIGHT_SHOULDER])

    left_elbow = landmark_point(landmarks[LEFT_ELBOW])
    right_elbow = landmark_point(landmarks[RIGHT_ELBOW])

    left_wrist = landmark_point(landmarks[LEFT_WRIST])
    right_wrist = landmark_point(landmarks[RIGHT_WRIST])

    feedback = []

    # Check whether both wrists are above their shoulders.
    left_wrist_above_shoulder = left_wrist[1] < left_shoulder[1]
    right_wrist_above_shoulder = right_wrist[1] < right_shoulder[1]

    if not left_wrist_above_shoulder:
        feedback.append(
            "Raise your left hand higher."
        )

    if not right_wrist_above_shoulder:
        feedback.append(
            "Raise your right hand higher."
        )

    # Calculate elbow angles to check whether the arms are reasonably extended.
    left_elbow_angle = calculate_angle(
        left_shoulder,
        left_elbow,
        left_wrist,
    )

    right_elbow_angle = calculate_angle(
        right_shoulder,
        right_elbow,
        right_wrist,
    )

    if left_elbow_angle < 150:
        feedback.append(
            "Straighten your left arm."
        )

    if right_elbow_angle < 150:
        feedback.append(
            "Straighten your right arm."
        )

    if not feedback:
        feedback.append(
            "Good Raised Hands Pose! Keep both arms raised."
        )

    return {
        "correct": len(feedback) == 1
        and feedback[0].startswith("Good Raised Hands"),
        "feedback": feedback,
        "measurements": {
            "left_elbow_angle": round(left_elbow_angle, 1),
            "right_elbow_angle": round(right_elbow_angle, 1),
            "left_wrist_height": round(left_wrist[1], 3),
            "right_wrist_height": round(right_wrist[1], 3),
        },
    }

def analyze_warrior_ii_pose(landmarks):
    """Analyze Warrior II Pose posture using MediaPipe landmarks."""

    if landmarks is None:
        return {
            "correct": False,
            "feedback": ["No body detected."],
            "measurements": {},
        }

    left_shoulder = landmark_point(landmarks[LEFT_SHOULDER])
    right_shoulder = landmark_point(landmarks[RIGHT_SHOULDER])

    left_elbow = landmark_point(landmarks[LEFT_ELBOW])
    right_elbow = landmark_point(landmarks[RIGHT_ELBOW])

    left_wrist = landmark_point(landmarks[LEFT_WRIST])
    right_wrist = landmark_point(landmarks[RIGHT_WRIST])

    left_hip = landmark_point(landmarks[LEFT_HIP])
    right_hip = landmark_point(landmarks[RIGHT_HIP])

    left_knee = landmark_point(landmarks[LEFT_KNEE])
    right_knee = landmark_point(landmarks[RIGHT_KNEE])

    left_ankle = landmark_point(landmarks[LEFT_ANKLE])
    right_ankle = landmark_point(landmarks[RIGHT_ANKLE])

    feedback = []

    # Calculate knee angles.
    left_knee_angle = calculate_angle(
        left_hip,
        left_knee,
        left_ankle,
    )

    right_knee_angle = calculate_angle(
        right_hip,
        right_knee,
        right_ankle,
    )

    # Calculate elbow angles.
    left_elbow_angle = calculate_angle(
        left_shoulder,
        left_elbow,
        left_wrist,
    )

    right_elbow_angle = calculate_angle(
        right_shoulder,
        right_elbow,
        right_wrist,
    )

    # Determine the bent/front leg.
    if left_knee_angle < right_knee_angle:
        bent_knee_angle = left_knee_angle
        straight_knee_angle = right_knee_angle
        bent_leg = "left"
    else:
        bent_knee_angle = right_knee_angle
        straight_knee_angle = left_knee_angle
        bent_leg = "right"

    # The front knee should be bent.
    if bent_knee_angle > 140:
        feedback.append(
            f"Bend your {bent_leg} knee more."
        )

    # The opposite leg should remain reasonably straight.
    if straight_knee_angle < 155:
        straight_leg = "right" if bent_leg == "left" else "left"

        feedback.append(
            f"Straighten your {straight_leg} leg."
        )

    # Both arms should be reasonably extended.
    if left_elbow_angle < 150:
        feedback.append(
            "Straighten your left arm."
        )

    if right_elbow_angle < 150:
        feedback.append(
            "Straighten your right arm."
        )

    # Check that both wrists are approximately at shoulder level.
    left_arm_height_difference = abs(
        left_wrist[1] - left_shoulder[1]
    )

    right_arm_height_difference = abs(
        right_wrist[1] - right_shoulder[1]
    )

    if left_arm_height_difference > 0.15:
        feedback.append(
            "Keep your left arm closer to shoulder height."
        )

    if right_arm_height_difference > 0.15:
        feedback.append(
            "Keep your right arm closer to shoulder height."
        )

    if not feedback:
        feedback.append(
            "Good Warrior II Pose! Keep your front knee bent and arms extended."
        )

    return {
        "correct": len(feedback) == 1
        and feedback[0].startswith("Good Warrior II"),
        "feedback": feedback,
        "measurements": {
            "left_knee_angle": round(left_knee_angle, 1),
            "right_knee_angle": round(right_knee_angle, 1),
            "bent_knee_angle": round(bent_knee_angle, 1),
            "straight_knee_angle": round(straight_knee_angle, 1),
            "left_elbow_angle": round(left_elbow_angle, 1),
            "right_elbow_angle": round(right_elbow_angle, 1),
            "left_arm_height_difference": round(
                left_arm_height_difference,
                3,
            ),
            "right_arm_height_difference": round(
                right_arm_height_difference,
                3,
            ),
        },
    }

def analyze_hands_on_hips_pose(landmarks):
    """Analyze Hands on Hips Pose posture using MediaPipe landmarks."""

    if landmarks is None:
        return {
            "correct": False,
            "feedback": ["No body detected."],
            "measurements": {},
        }

    left_shoulder = landmark_point(landmarks[LEFT_SHOULDER])
    right_shoulder = landmark_point(landmarks[RIGHT_SHOULDER])

    left_wrist = landmark_point(landmarks[LEFT_WRIST])
    right_wrist = landmark_point(landmarks[RIGHT_WRIST])

    left_hip = landmark_point(landmarks[LEFT_HIP])
    right_hip = landmark_point(landmarks[RIGHT_HIP])

    left_knee = landmark_point(landmarks[LEFT_KNEE])
    right_knee = landmark_point(landmarks[RIGHT_KNEE])

    left_ankle = landmark_point(landmarks[LEFT_ANKLE])
    right_ankle = landmark_point(landmarks[RIGHT_ANKLE])

    feedback = []

    # Check whether both wrists are close to the hips.
    left_wrist_hip_distance = (
        (left_wrist[0] - left_hip[0]) ** 2
        + (left_wrist[1] - left_hip[1]) ** 2
    ) ** 0.5

    right_wrist_hip_distance = (
        (right_wrist[0] - right_hip[0]) ** 2
        + (right_wrist[1] - right_hip[1]) ** 2
    ) ** 0.5

    if left_wrist_hip_distance > 0.25:
        feedback.append(
            "Place your left hand closer to your hip."
        )

    if right_wrist_hip_distance > 0.25:
        feedback.append(
            "Place your right hand closer to your hip."
        )

    # Check whether both knees are reasonably straight.
    left_knee_angle = calculate_angle(
        left_hip,
        left_knee,
        left_ankle,
    )

    right_knee_angle = calculate_angle(
        right_hip,
        right_knee,
        right_ankle,
    )

    if left_knee_angle < 165:
        feedback.append(
            "Straighten your left leg."
        )

    if right_knee_angle < 165:
        feedback.append(
            "Straighten your right leg."
        )

    # Check shoulder balance.
    shoulder_height_difference = abs(
        left_shoulder[1] - right_shoulder[1]
    )

    if shoulder_height_difference > 0.08:
        feedback.append(
            "Keep both shoulders level."
        )

    # Check hip balance.
    hip_height_difference = abs(
        left_hip[1] - right_hip[1]
    )

    if hip_height_difference > 0.08:
        feedback.append(
            "Keep both hips level."
        )

    if not feedback:
        feedback.append(
            "Good Hands on Hips Pose! Keep your hands on your hips and body balanced."
        )

    return {
        "correct": len(feedback) == 1
        and feedback[0].startswith("Good Hands on Hips"),
        "feedback": feedback,
        "measurements": {
            "left_wrist_hip_distance": round(
                left_wrist_hip_distance,
                3,
            ),
            "right_wrist_hip_distance": round(
                right_wrist_hip_distance,
                3,
            ),
            "left_knee_angle": round(
                left_knee_angle,
                1,
            ),
            "right_knee_angle": round(
                right_knee_angle,
                1,
            ),
            "shoulder_height_difference": round(
                shoulder_height_difference,
                3,
            ),
            "hip_height_difference": round(
                hip_height_difference,
                3,
            ),
        },
    }

def analyze_side_stretch_pose(landmarks):
    """Analyze Side Stretch Pose posture using MediaPipe landmarks."""

    if landmarks is None:
        return {
            "correct": False,
            "feedback": ["No body detected."],
            "measurements": {},
        }

    left_shoulder = landmark_point(landmarks[LEFT_SHOULDER])
    right_shoulder = landmark_point(landmarks[RIGHT_SHOULDER])

    left_wrist = landmark_point(landmarks[LEFT_WRIST])
    right_wrist = landmark_point(landmarks[RIGHT_WRIST])

    left_hip = landmark_point(landmarks[LEFT_HIP])
    right_hip = landmark_point(landmarks[RIGHT_HIP])

    feedback = []

    # Determine which hand is raised.
    if left_wrist[1] < right_wrist[1]:
        raised_wrist = left_wrist
        raised_shoulder = left_shoulder
        raised_side = "left"
    else:
        raised_wrist = right_wrist
        raised_shoulder = right_shoulder
        raised_side = "right"

    # The raised hand should be clearly above its shoulder.
    if raised_wrist[1] >= raised_shoulder[1]:
        feedback.append(
            f"Raise your {raised_side} arm higher."
        )

    # Check whether the shoulders are tilted,
    # which indicates a side stretch.
    shoulder_vertical_difference = abs(
        left_shoulder[1] - right_shoulder[1]
    )

    if shoulder_vertical_difference < 0.03:
        feedback.append(
            "Lean gently to one side to create the stretch."
        )

    # Check whether the raised hand is sufficiently
    # above the corresponding hip.
    raised_hip = (
        left_hip if raised_side == "left"
        else right_hip
    )

    hand_hip_height_difference = (
        raised_hip[1] - raised_wrist[1]
    )

    if hand_hip_height_difference < 0.20:
        feedback.append(
            f"Extend your {raised_side} arm upward."
        )

    if not feedback:
        feedback.append(
            "Good Side Stretch! Keep your raised arm extended and lean gently to the side."
        )

    return {
        "correct": len(feedback) == 1
        and feedback[0].startswith("Good Side Stretch"),
        "feedback": feedback,
        "measurements": {
            "raised_side": raised_side,
            "shoulder_vertical_difference": round(
                shoulder_vertical_difference,
                3,
            ),
            "hand_hip_height_difference": round(
                hand_hip_height_difference,
                3,
            ),
            "raised_wrist_height": round(
                raised_wrist[1],
                3,
            ),
        },
    }