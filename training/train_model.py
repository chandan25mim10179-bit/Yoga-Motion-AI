import os
import sys

import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder


# Add project root to Python path.
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.insert(0, PROJECT_ROOT)


# Dataset paths.
TRAIN_FILE = os.path.join(
    PROJECT_ROOT,
    "datasets",
    "processed",
    "train.csv",
)

TEST_FILE = os.path.join(
    PROJECT_ROOT,
    "datasets",
    "processed",
    "test.csv",
)


# Model output directory.
MODEL_DIR = os.path.join(
    PROJECT_ROOT,
    "models",
)

MODEL_FILE = os.path.join(
    MODEL_DIR,
    "yoga_pose_classifier.joblib",
)

LABEL_ENCODER_FILE = os.path.join(
    MODEL_DIR,
    "label_encoder.joblib",
)


# Model configuration.
RANDOM_STATE = 42
N_ESTIMATORS = 200


def main():
    print()
    print("=" * 60)
    print("YOGA MOTION AI - ML MODEL TRAINING")
    print("=" * 60)

    # Check dataset files.
    if not os.path.exists(TRAIN_FILE):
        raise FileNotFoundError(
            f"Training dataset not found: {TRAIN_FILE}"
        )

    if not os.path.exists(TEST_FILE):
        raise FileNotFoundError(
            f"Testing dataset not found: {TEST_FILE}"
        )

    # Load datasets.
    print()
    print("Loading training dataset...")

    train_df = pd.read_csv(TRAIN_FILE)

    print("Loading testing dataset...")

    test_df = pd.read_csv(TEST_FILE)

    print()
    print(f"Training samples: {len(train_df)}")
    print(f"Testing samples: {len(test_df)}")

    # Separate features and labels.
    X_train = train_df.drop(columns=["label"])
    y_train = train_df["label"]

    X_test = test_df.drop(columns=["label"])
    y_test = test_df["label"]

    print()
    print(f"Number of features: {X_train.shape[1]}")
    print(f"Number of classes: {y_train.nunique()}")

    # Encode text labels into numbers.
    label_encoder = LabelEncoder()

    y_train_encoded = label_encoder.fit_transform(
        y_train
    )

    y_test_encoded = label_encoder.transform(
        y_test
    )

    print()
    print("Classes:")

    for index, class_name in enumerate(
        label_encoder.classes_
    ):
        print(f"{index}: {class_name}")

    # Create the Random Forest classifier.
    print()
    print("Creating Random Forest classifier...")

    model = RandomForestClassifier(
        n_estimators=N_ESTIMATORS,
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )

    # Train the model.
    print()
    print("Training model...")
    print("Please wait...")

    model.fit(
        X_train,
        y_train_encoded,
    )

    print()
    print("MODEL TRAINING COMPLETE")

    # Predict the test dataset.
    print()
    print("Evaluating model on testing dataset...")

    y_pred = model.predict(X_test)

    # Calculate accuracy.
    accuracy = accuracy_score(
        y_test_encoded,
        y_pred,
    )

    print()
    print("=" * 60)
    print("MODEL EVALUATION")
    print("=" * 60)

    print()
    print(
        f"Test Accuracy: {accuracy * 100:.2f}%"
    )

    print()
    print("Classification Report:")

    print(
        classification_report(
            y_test_encoded,
            y_pred,
            target_names=label_encoder.classes_,
            zero_division=0,
        )
    )

    # Create models directory.
    os.makedirs(
        MODEL_DIR,
        exist_ok=True,
    )

    # Save trained model.
    joblib.dump(
        model,
        MODEL_FILE,
    )

    # Save label encoder.
    joblib.dump(
        label_encoder,
        LABEL_ENCODER_FILE,
    )

    print("=" * 60)
    print("MODEL SAVED")
    print("=" * 60)

    print()
    print("Classifier:")
    print(MODEL_FILE)

    print()
    print("Label encoder:")
    print(LABEL_ENCODER_FILE)

    print()
    print(
        "RESULT: ML MODEL TRAINED AND EVALUATED SUCCESSFULLY"
    )


if __name__ == "__main__":
    main()