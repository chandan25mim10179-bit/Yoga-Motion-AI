import os
import sys

import cv2
import numpy as np

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.insert(0, PROJECT_ROOT)

from backend.features import extract_features
from backend.pose_engine import PoseEngine


INPUT_IMAGE = os.path.join(
    PROJECT_ROOT,
    "datasets",
    "sample",
    "test_person.jpg",
)


def test_real_image_features():
    image = cv2.imread(INPUT_IMAGE)

    assert image is not None, "Test image could not be loaded."

    engine = PoseEngine()

    results = engine.detect(image)
    landmarks = engine.get_landmarks(results)

    assert landmarks is not None, "No pose detected in test image."
    assert len(landmarks) == 33

    features = extract_features(landmarks)

    assert features.shape == (132,)
    assert features.dtype == np.float32
    assert np.isfinite(features).all()

    engine.close()


def test_invalid_landmark_count():
    invalid_landmarks = []

    try:
        extract_features(invalid_landmarks)
        assert False, "Expected ValueError was not raised."
    except ValueError:
        pass


def test_feature_values_are_numeric():
    image = cv2.imread(INPUT_IMAGE)

    assert image is not None

    engine = PoseEngine()

    results = engine.detect(image)
    landmarks = engine.get_landmarks(results)

    assert landmarks is not None

    features = extract_features(landmarks)

    assert np.issubdtype(features.dtype, np.floating)

    engine.close()


if __name__ == "__main__":
    test_real_image_features()
    test_invalid_landmark_count()
    test_feature_values_are_numeric()

    print("ALL FEATURE TESTS PASSED")