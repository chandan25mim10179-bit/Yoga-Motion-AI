import os

import joblib
import pandas as pd


PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)


TEST_FILE = os.path.join(
    PROJECT_ROOT,
    "datasets",
    "processed",
    "test.csv",
)


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


def main():
    print()
    print("=" * 60)
    print("YOGA MOTION AI - SAVED MODEL TEST")
    print("=" * 60)

    # Check required files.
    if not os.path.exists(TEST_FILE):
        raise FileNotFoundError(
            f"Test dataset not found: {TEST_FILE}"
        )

    if not os.path.exists(MODEL_FILE):
        raise FileNotFoundError(
            f"Model not found: {MODEL_FILE}"
        )

    if not os.path.exists(LABEL_ENCODER_FILE):
        raise FileNotFoundError(
            f"Label encoder not found: {LABEL_ENCODER_FILE}"
        )

    # Load the saved model.
    print()
    print("Loading saved model...")

    model = joblib.load(MODEL_FILE)

    # Load the saved label encoder.
    print("Loading label encoder...")

    label_encoder = joblib.load(
        LABEL_ENCODER_FILE
    )

    # Load test data.
    print("Loading test dataset...")

    test_df = pd.read_csv(TEST_FILE)

    X_test = test_df.drop(
        columns=["label"]
    )

    y_test = test_df["label"]

    # Select a few samples for prediction.
    sample_count = 10

    X_samples = X_test.head(sample_count)

    actual_labels = y_test.head(
        sample_count
    )

    # Predict using the saved model.
    predictions_encoded = model.predict(
        X_samples
    )

    predictions = label_encoder.inverse_transform(
        predictions_encoded
    )

    print()
    print("=" * 60)
    print("SAMPLE PREDICTIONS")
    print("=" * 60)

    for index in range(sample_count):

        actual = actual_labels.iloc[index]
        predicted = predictions[index]

        result = (
            "CORRECT"
            if actual == predicted
            else "INCORRECT"
        )

        print()
        print(f"Sample {index + 1}")
        print(f"Actual:    {actual}")
        print(f"Predicted: {predicted}")
        print(f"Result:    {result}")

    # Test prediction probability.
    print()
    print("=" * 60)
    print("CONFIDENCE TEST")
    print("=" * 60)

    probabilities = model.predict_proba(
        X_samples.iloc[[0]]
    )[0]

    best_index = probabilities.argmax()

    predicted_pose = label_encoder.inverse_transform(
        [best_index]
    )[0]

    confidence = probabilities[best_index] * 100

    print()
    print(f"Predicted pose: {predicted_pose}")
    print(f"Confidence: {confidence:.2f}%")

    print()
    print("=" * 60)
    print("SAVED MODEL TEST COMPLETE")
    print("=" * 60)

    print()
    print(
        "RESULT: SAVED ML MODEL LOADED AND PREDICTIONS WORKING"
    )


if __name__ == "__main__":
    main()