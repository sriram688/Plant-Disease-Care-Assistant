"""Unit tests for ML model architectures."""

import pytest
import tensorflow as tf
from src.model import build_custom_cnn
from src.config import NUM_CLASSES, INPUT_SHAPE


def test_build_custom_cnn_shape():
    """Verify custom CNN architecture input and output tensor dimensions."""
    model = build_custom_cnn(input_shape=(128, 128, 3), num_classes=NUM_CLASSES)

    assert isinstance(model, tf.keras.Model)
    assert model.input_shape == (None, 128, 128, 3)
    assert model.output_shape == (None, NUM_CLASSES)
    assert model.loss == "sparse_categorical_crossentropy"


def test_custom_cnn_compilation():
    """Verify custom CNN compiles cleanly with optimizer and metrics."""
    model = build_custom_cnn()
    assert model.optimizer is not None
    assert len(model.metrics) >= 1
