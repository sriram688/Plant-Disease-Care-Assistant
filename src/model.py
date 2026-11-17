"""Model architectures for PlantGuard AI.

Provides:
1. Custom CNN: Lightweight, fast baseline convolutional neural network.
2. Transfer Learning (MobileNetV2): Pre-trained deep feature extractor optimized for vision tasks.
"""

from pathlib import Path
from typing import Tuple, Optional
import tensorflow as tf
from tensorflow.keras import layers, models, regularizers

from src.config import INPUT_SHAPE, NUM_CLASSES, LEARNING_RATE


def build_custom_cnn(
    input_shape: Tuple[int, int, int] = INPUT_SHAPE,
    num_classes: int = NUM_CLASSES,
    dropout_rate: float = 0.35,
) -> tf.keras.Model:
    """Build a modern, modular baseline Convolutional Neural Network.

    Features 4 convolutional blocks with Batch Normalization, ReLU activations,
    Max Pooling, Spatial Dropout, and Global Average Pooling to prevent overfitting.

    Args:
        input_shape: Input tensor shape (H, W, C).
        num_classes: Number of disease target classes.
        dropout_rate: Dropout rate for dense classification head.

    Returns:
        tf.keras.Model: Compiled Keras model.
    """
    inputs = layers.Input(shape=input_shape, name="image_input")

    # Block 1
    x = layers.Conv2D(32, (3, 3), padding="same", use_bias=False, name="conv1_1")(inputs)
    x = layers.BatchNormalization(name="bn1_1")(x)
    x = layers.Activation("relu", name="relu1_1")(x)
    x = layers.Conv2D(32, (3, 3), padding="same", name="conv1_2")(x)
    x = layers.Activation("relu", name="relu1_2")(x)
    x = layers.MaxPooling2D(pool_size=(2, 2), name="pool1")(x)
    x = layers.Dropout(0.15, name="drop1")(x)

    # Block 2
    x = layers.Conv2D(64, (3, 3), padding="same", use_bias=False, name="conv2_1")(x)
    x = layers.BatchNormalization(name="bn2_1")(x)
    x = layers.Activation("relu", name="relu2_1")(x)
    x = layers.Conv2D(64, (3, 3), padding="same", name="conv2_2")(x)
    x = layers.Activation("relu", name="relu2_2")(x)
    x = layers.MaxPooling2D(pool_size=(2, 2), name="pool2")(x)
    x = layers.Dropout(0.2, name="drop2")(x)

    # Block 3
    x = layers.Conv2D(128, (3, 3), padding="same", use_bias=False, name="conv3_1")(x)
    x = layers.BatchNormalization(name="bn3_1")(x)
    x = layers.Activation("relu", name="relu3_1")(x)
    x = layers.Conv2D(128, (3, 3), padding="same", name="conv3_2")(x)
    x = layers.Activation("relu", name="relu3_2")(x)
    x = layers.MaxPooling2D(pool_size=(2, 2), name="pool3")(x)
    x = layers.Dropout(0.25, name="drop3")(x)

    # Block 4
    x = layers.Conv2D(256, (3, 3), padding="same", use_bias=False, name="conv4_1")(x)
    x = layers.BatchNormalization(name="bn4_1")(x)
    x = layers.Activation("relu", name="relu4_1")(x)
    x = layers.MaxPooling2D(pool_size=(2, 2), name="pool4")(x)
    x = layers.Dropout(0.3, name="drop4")(x)

    # Classification Head
    x = layers.GlobalAveragePooling2D(name="global_avg_pool")(x)
    x = layers.Dense(128, kernel_regularizer=regularizers.l2(1e-4), name="dense_fc1")(x)
    x = layers.BatchNormalization(name="bn_dense")(x)
    x = layers.Activation("relu", name="relu_dense")(x)
    x = layers.Dropout(dropout_rate, name="head_dropout")(x)

    outputs = layers.Dense(num_classes, activation="softmax", dtype="float32", name="predictions")(x)

    model = tf.keras.Model(inputs=inputs, outputs=outputs, name="PlantGuard_CustomCNN")

    optimizer = tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE)
    model.compile(
        optimizer=optimizer,
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )

    return model


def build_transfer_model(
    input_shape: Tuple[int, int, int] = INPUT_SHAPE,
    num_classes: int = NUM_CLASSES,
    fine_tune_at: Optional[int] = None,
) -> tf.keras.Model:
    """Build a transfer-learning model based on MobileNetV2 pretrained on ImageNet.

    MobileNetV2 delivers exceptional feature extraction while remaining lightweight
    and deployable on edge devices and standard web servers.

    Args:
        input_shape: Input tensor dimensions.
        num_classes: Target classes.
        fine_tune_at: Layer index from which to unfreeze weights for fine-tuning.

    Returns:
        tf.keras.Model: Compiled transfer learning model.
    """
    inputs = layers.Input(shape=input_shape, name="image_input")

    # MobileNetV2 expects input scaled [-1, 1] if input is [0, 1]
    # tf.keras.applications.mobilenet_v2.preprocess_input maps [0, 255] or [0, 1]*255 to [-1, 1]
    # Here inputs are in [0, 1], so scale: (x * 2.0) - 1.0
    scaled_inputs = layers.Rescaling(scale=2.0, offset=-1.0, name="mobilenet_rescaling")(inputs)

    base_model = tf.keras.applications.MobileNetV2(
        input_shape=input_shape,
        include_top=False,
        weights="imagenet",
    )

    # Default: freeze base model weights
    base_model.trainable = False

    if fine_tune_at is not None:
        base_model.trainable = True
        for layer in base_model.layers[:fine_tune_at]:
            layer.trainable = False

    x = base_model(scaled_inputs, training=False)
    x = layers.GlobalAveragePooling2D(name="global_avg_pool")(x)
    x = layers.BatchNormalization(name="bn_features")(x)
    x = layers.Dense(256, kernel_regularizer=regularizers.l2(1e-4), name="fc_dense_1")(x)
    x = layers.BatchNormalization(name="bn_dense")(x)
    x = layers.Activation("relu", name="relu_dense")(x)
    x = layers.Dropout(0.4, name="dropout_fc")(x)

    outputs = layers.Dense(num_classes, activation="softmax", dtype="float32", name="predictions")(x)

    model = tf.keras.Model(inputs=inputs, outputs=outputs, name="PlantGuard_MobileNetV2")

    optimizer = tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE)
    model.compile(
        optimizer=optimizer,
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )

    return model


def get_model(architecture: str = "mobilenetv2", **kwargs) -> tf.keras.Model:
    """Model factory returning either 'mobilenetv2' or 'custom_cnn'."""
    arch = architecture.lower()
    if arch in ("mobilenet", "mobilenetv2", "transfer"):
        return build_transfer_model(**kwargs)
    elif arch in ("cnn", "custom", "custom_cnn"):
        return build_custom_cnn(**kwargs)
    else:
        raise ValueError(f"Unknown architecture '{architecture}'. Choose 'mobilenetv2' or 'custom_cnn'.")


def save_trained_model(model: tf.keras.Model, filepath: Path) -> None:
    """Save trained model in standard Keras format."""
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    model.save(filepath)


def load_trained_model(filepath: Path) -> tf.keras.Model:
    """Load model from disk with error checking."""
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"Model file not found at: {filepath}")
    return tf.keras.models.load_model(filepath)
