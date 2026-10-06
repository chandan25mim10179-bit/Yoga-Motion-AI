import os
import sys

import pandas as pd
from sklearn.model_selection import train_test_split


# Add project root to Python path.
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.insert(0, PROJECT_ROOT)


# Dataset paths.
DATASET_FILE = os.path.join(
    PROJECT_ROOT,
    "datasets",
    "processed",
    "yoga_pose_dataset.csv",
)

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


TEST_SIZE = 0.20
RANDOM_STATE = 42


def main():
    print()
    print("=" * 60)
    print("YOGA MOTION AI - DATASET PREPARATION")
    print("=" * 60)

    # Check that the original dataset exists.
    if not os.path.exists(DATASET_FILE):
        raise FileNotFoundError(
            f"Dataset not found: {DATASET_FILE}"
        )

    print()
    print("Loading dataset...")

    df = pd.read_csv(DATASET_FILE)

    print(f"Total samples: {len(df)}")
    print(f"Total columns: {len(df.columns)}")

    # Separate features and labels.
    X = df.drop(columns=["label"])
    y = df["label"]

    print(f"Number of features: {X.shape[1]}")
    print(f"Number of classes: {y.nunique()}")

    print()
    print("Class distribution:")
    print(y.value_counts().sort_index())

    # Check for missing values.
    if X.isnull().values.any():
        raise ValueError(
            "Dataset contains missing feature values."
        )

    # Check for infinite values.
    if not X.map(
        lambda value: pd.notna(value)
        and value != float("inf")
        and value != float("-inf")
    ).all().all():
        raise ValueError(
            "Dataset contains infinite or invalid values."
        )

    # Stratified train/test split.
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    # Recombine features and labels.
    train_df = X_train.copy()
    train_df["label"] = y_train.values

    test_df = X_test.copy()
    test_df["label"] = y_test.values

    # Save datasets.
    train_df.to_csv(
        TRAIN_FILE,
        index=False,
    )

    test_df.to_csv(
        TEST_FILE,
        index=False,
    )

    print()
    print("=" * 60)
    print("DATASET SPLIT COMPLETE")
    print("=" * 60)

    print()
    print(f"Training samples: {len(train_df)}")
    print(f"Testing samples: {len(test_df)}")

    print()
    print("Training class distribution:")
    print(train_df["label"].value_counts().sort_index())

    print()
    print("Testing class distribution:")
    print(test_df["label"].value_counts().sort_index())

    print()
    print("Training file:")
    print(TRAIN_FILE)

    print()
    print("Testing file:")
    print(TEST_FILE)

    print()
    print("RESULT: DATASET READY FOR ML TRAINING")


if __name__ == "__main__":
    main()