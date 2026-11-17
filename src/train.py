"""Model training script for PlantGuard AI.

Loads structured dataset, validates class distribution, applies biologically safe
augmentation to training data only (avoiding data leakage), trains the chosen model
(Custom CNN or MobileNetV2) with early stopping and checkpointing, and saves performance curves.
"""

import argparse
import os
import json
from pathlib import Path
from typing import Dict, Tuple, Any
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend
import matplotlib.pyplot as plt
import tensorflow as tf

from src.config import (
    TRAIN_DIR,
    VAL_DIR,
    TEST_DIR,
    IMAGE_SIZE,
    BATCH_SIZE,
    DEFAULT_EPOCHS,
    LEARNING_RATE,
    RANDOM_SEED,
    CLASS_NAMES,
    MOBILENET_MODEL_PATH,
    CNN_MODEL_PATH,
    TRAINING_CURVES_PATH,
    MODELS_DIR,
)
from src.preprocessing import get_data_augmentation_layers
from src.model import build_custom_cnn, build_transfer_model


# Set global deterministic random seed
tf.keras.utils.set_random_seed(RANDOM_SEED)


def verify_dataset_structure(data_dir: Path) -> Dict[str, int]:
    """Inspect and count images per class to detect distribution issues."""
    counts = {}
    if not data_dir.exists():
        raise FileNotFoundError(f"Dataset directory not found: {data_dir}")

    for cls in CLASS_NAMES:
        cls_dir = data_dir / cls
        if cls_dir.is_dir():
            valid_files = [f for f in cls_dir.iterdir() if f.is_file() and not f.name.startswith(".")]
            counts[cls] = len(valid_files)
        else:
            counts[cls] = 0
    return counts


def create_datasets(
    train_dir: Path = TRAIN_DIR,
    val_dir: Path = VAL_DIR,
    batch_size: int = BATCH_SIZE,
    image_size: Tuple[int, int] = IMAGE_SIZE,
) -> Tuple[tf.data.Dataset, tf.data.Dataset, Dict[str, Any]]:
    """Build optimized tf.data.Dataset pipelines for training and validation."""
    print("Verifying dataset splits...")
    train_counts = verify_dataset_structure(train_dir)
    val_counts = verify_dataset_structure(val_dir)

    print("\nDataset Class Distribution:")
    for cls in CLASS_NAMES:
        print(f"  {cls:<25} | Train: {train_counts[cls]:>4} | Val: {val_counts[cls]:>4}")

    # Load raw datasets from directory
    train_ds = tf.keras.utils.image_dataset_from_directory(
        train_dir,
        class_names=CLASS_NAMES,
        color_mode="rgb",
        batch_size=batch_size,
        image_size=image_size,
        shuffle=True,
        seed=RANDOM_SEED,
    )

    val_ds = tf.keras.utils.image_dataset_from_directory(
        val_dir,
        class_names=CLASS_NAMES,
        color_mode="rgb",
        batch_size=batch_size,
        image_size=image_size,
        shuffle=False,
    )

    # Scaling layer to map [0, 255] to [0.0, 1.0]
    rescaling = tf.keras.layers.Rescaling(1.0 / 255.0)

    # Data augmentation for training ONLY
    data_aug = get_data_augmentation_layers()

    # Preprocessing pipelines
    train_ds = train_ds.map(
        lambda x, y: (rescaling(x), y),
        num_parallel_calls=tf.data.AUTOTUNE,
    )
    train_ds = train_ds.map(
        lambda x, y: (data_aug(x, training=True), y),
        num_parallel_calls=tf.data.AUTOTUNE,
    )
    train_ds = train_ds.cache().shuffle(500).prefetch(buffer_size=tf.data.AUTOTUNE)

    val_ds = val_ds.map(
        lambda x, y: (rescaling(x), y),
        num_parallel_calls=tf.data.AUTOTUNE,
    )
    val_ds = val_ds.cache().prefetch(buffer_size=tf.data.AUTOTUNE)

    info = {
        "train_counts": train_counts,
        "val_counts": val_counts,
        "total_train": sum(train_counts.values()),
        "total_val": sum(val_counts.values()),
    }
    return train_ds, val_ds, info


def plot_training_history(history: tf.keras.callbacks.History, save_path: Path) -> None:
    """Plot training and validation loss/accuracy curves."""
    save_path.parent.mkdir(parents=True, exist_ok=True)

    acc = history.history.get("accuracy", [])
    val_acc = history.history.get("val_accuracy", [])
    loss = history.history.get("loss", [])
    val_loss = history.history.get("val_loss", [])
    epochs_range = range(1, len(acc) + 1)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Accuracy Plot
    ax1.plot(epochs_range, acc, label="Training Accuracy", color="#2E7D32", linewidth=2)
    ax1.plot(epochs_range, val_acc, label="Validation Accuracy", color="#0288D1", linewidth=2, linestyle="--")
    ax1.set_title("Training and Validation Accuracy", fontsize=12, fontweight="bold")
    ax1.set_xlabel("Epochs")
    ax1.set_ylabel("Accuracy")
    ax1.set_ylim([0, 1.05])
    ax1.grid(True, linestyle=":", alpha=0.6)
    ax1.legend(loc="lower right")

    # Loss Plot
    ax2.plot(epochs_range, loss, label="Training Loss", color="#C62828", linewidth=2)
    ax2.plot(epochs_range, val_loss, label="Validation Loss", color="#FF8F00", linewidth=2, linestyle="--")
    ax2.set_title("Training and Validation Loss", fontsize=12, fontweight="bold")
    ax2.set_xlabel("Epochs")
    ax2.set_ylabel("Cross Entropy Loss")
    ax2.grid(True, linestyle=":", alpha=0.6)
    ax2.legend(loc="upper right")

    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()
    print(f"Training curves saved to: {save_path}")


def train(
    architecture: str = "mobilenetv2",
    epochs: int = DEFAULT_EPOCHS,
    batch_size: int = BATCH_SIZE,
    learning_rate: float = LEARNING_RATE,
) -> tf.keras.Model:
    """Train the selected plant disease classification model."""
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    target_save_path = MOBILENET_MODEL_PATH if "mobilenet" in architecture.lower() else CNN_MODEL_PATH

    print(f"\n==========================================")
    print(f"PlantGuard AI Training Pipeline")
    print(f"Architecture: {architecture.upper()}")
    print(f"Target Checkpoint: {target_save_path}")
    print(f"==========================================\n")

    train_ds, val_ds, info = create_datasets(
        train_dir=TRAIN_DIR,
        val_dir=VAL_DIR,
        batch_size=batch_size,
    )

    if info["total_train"] == 0:
        raise ValueError("No training images found. Please run 'python scripts/prepare_dataset.py' first.")

    # Initialize model
    if "mobilenet" in architecture.lower():
        model = build_transfer_model()
    else:
        model = build_custom_cnn()

    model.summary()

    # Callbacks
    callbacks = [
        tf.keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=5,
            restore_best_weights=True,
            verbose=1,
        ),
        tf.keras.callbacks.ModelCheckpoint(
            filepath=str(target_save_path),
            monitor="val_accuracy",
            save_best_only=True,
            verbose=1,
        ),
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.5,
            patience=2,
            min_lr=1e-6,
            verbose=1,
        ),
    ]

    print("\nStarting training loop...")
    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs,
        callbacks=callbacks,
    )

    # Save training curves plot
    plot_training_history(history, TRAINING_CURVES_PATH)

    # Save final model explicitly
    model.save(target_save_path)
    print(f"\nModel training complete! Saved to {target_save_path}")

    return model


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PlantGuard AI Model Training")
    parser.add_argument(
        "--architecture",
        type=str,
        default="mobilenetv2",
        choices=["mobilenetv2", "custom_cnn"],
        help="Model architecture: 'mobilenetv2' (transfer learning) or 'custom_cnn'",
    )
    parser.add_argument("--epochs", type=int, default=DEFAULT_EPOCHS, help="Number of training epochs")
    parser.add_argument("--batch-size", type=int, default=BATCH_SIZE, help="Batch size")
    parser.add_argument("--lr", type=float, default=LEARNING_RATE, help="Initial learning rate")
    args = parser.parse_args()

    train(
        architecture=args.architecture,
        epochs=args.epochs,
        batch_size=args.batch_size,
        learning_rate=args.lr,
    )
