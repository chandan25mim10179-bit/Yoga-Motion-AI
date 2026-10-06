import os
import sys

import pandas as pd
import joblib

from backend.posture_analyzer import (
    analyze_tree_pose,
    analyze_t_pose,
    analyze_mountain_pose,
    analyze_raised_hands_pose,
    analyze_warrior_ii_pose,
    analyze_hands_on_hips_pose,
    analyze_side_stretch_pose,
)

from backend.features import extract_features

# --------------------------------------------------
# Project paths
# --------------------------------------------------

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

MODEL_PATH = os.path.join(
    PROJECT_ROOT,
    "models",
    "yoga_pose_classifier.joblib",
)

ENCODER_PATH = os.path.join(
    PROJECT_ROOT,
    "models",
    "label_encoder.joblib",
)


# --------------------------------------------------
# Feature column names
# --------------------------------------------------

FEATURE_COLUMNS = [
    f"feature_{i}"
    for i in range(132)
]


class YogaAnalyzer:
    """
    Combine ML pose classification with
    pose-specific posture analysis.
    """

    def __init__(
        self,
        model_path=MODEL_PATH,
        encoder_path=ENCODER_PATH,
    ):
        # Load trained ML model.
        self.model = joblib.load(model_path)

        # Load label encoder.
        self.label_encoder = joblib.load(
            encoder_path
        )

    def classify_pose(self, landmarks):
        """
        Predict the yoga pose using the trained
        Random Forest classifier.

        Returns:
            pose name and confidence.
        """

        if landmarks is None:
            return {
                "pose": None,
                "confidence": 0.0,
            }

        # Extract the same 132 features used
        # during model training.
        features = extract_features(
            landmarks
        )

        # Convert features into a DataFrame
        # with the same column names used during training.
        feature_df = pd.DataFrame(
            [features],
            columns=FEATURE_COLUMNS,
        )

        # Predict encoded class.
        prediction = self.model.predict(
            feature_df
        )[0]

                # Calculate prediction confidence.
        probabilities = self.model.predict_proba(
            feature_df
        )[0]

        confidence = float(
            probabilities.max()
        )

        # Reject low-confidence predictions.
        if confidence < 0.30:
            return {
                "pose": "uncertain",
                "confidence": confidence,
                "posture": {
                    "correct": False,
                    "feedback": [
                        "Pose is uncertain. Please stand clearly and face the camera."
                    ],
                },
            }


        # Convert encoded class back to pose name.
        pose_name = self.label_encoder.inverse_transform(
            [prediction]
        )[0]

        

        return {
            "pose": pose_name,
            "confidence": confidence,
        }

    def analyze(self, landmarks):
        """
        Run the complete Yoga Motion AI analysis.

        Pipeline:

        MediaPipe landmarks
                ↓
        ML pose classification
                ↓
        Pose-specific posture analysis
                ↓
        Feedback
        """

        if landmarks is None:
            return {
                "pose": None,
                "confidence": 0.0,
                "posture": {
                    "correct": False,
                    "feedback": [
                        "No body detected."
                    ],
                },
            }

        # ------------------------------------------
        # Step 1: ML pose classification
        # ------------------------------------------

        classification = self.classify_pose(
            landmarks
        )

        pose_name = classification["pose"]

        confidence = classification[
            "confidence"
        ]

        # ------------------------------------------
        # Step 2: Pose-specific analysis
        # ------------------------------------------

        if pose_name == "tree":
          posture = analyze_tree_pose(
             landmarks
          )

        elif pose_name == "t_pose":
          posture = analyze_t_pose(
             landmarks
          )

        elif pose_name == "mountain":
          posture = analyze_mountain_pose(
             landmarks
          )

        elif pose_name == "raised_hands":
          posture = analyze_raised_hands_pose(
             landmarks
          )

        elif pose_name == "warrior_ii":
          posture = analyze_warrior_ii_pose(
             landmarks
          )
        elif pose_name == "hands_on_hips":
          posture = analyze_hands_on_hips_pose(
             landmarks
          )

        elif pose_name == "side_stretch":
          posture = analyze_side_stretch_pose(
             landmarks
          )

        elif pose_name == "uncertain":
            posture = classification["posture"]



        else:
         # Other pose analyzers will be added
         # later.
         posture = {
           "correct": True,
           "feedback": [
             "Pose detected. "
             "Detailed posture analysis "
             "for this pose is coming soon."
             ],
            }

        # ------------------------------------------
        # Final result
        # ------------------------------------------

        return {
            "pose": pose_name,
            "confidence": round(
                confidence,
                4,
            ),
            "posture": posture,
        }