"""Comprehensive model evaluation module for PlantGuard AI.

Calculates genuine metrics on the independent test set:
- Accuracy, Precision, Recall, F1-Score (Macro and Weighted)
- Per-class precision, recall, and F1
- Confusion Matrix visualization
- Scikit-learn classification report
- Saves metrics.json and confusion_matrix.png
"""

import argparse
import json
from pathlib import Path
from typing import Dict, Any, Optional
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
)
import tensorflow as tf

from src.config import (
    TEST_DIR,
    IMAGE_SIZE,
    BATCH_SIZE,
    CLASS_NAMES,
    CLASS_DISPLAY_INFO,
    MOBILENET_MODEL_PATH,
    CNN_MODEL_PATH,
    CONFUSION_MATRIX_PATH,
    METRICS_FILE,
    MODELS_DIR,
)


def load_test_dataset(test_dir: Path = TEST_DIR, batch_size: int = BATCH_SIZE):
    """Load independent test dataset without shuffling to preserve label correspondence."""
    if not test_dir.exists():
        raise FileNotFoundError(f"Test directory does not exist: {test_dir}")

    test_ds = tf.keras.utils.image_dataset_from_directory(
        test_dir,
        class_names=CLASS_NAMES,
        color_mode="rgb",
        batch_size=batch_size,
        image_size=IMAGE_SIZE,
        shuffle=False,
    )

    # Scale images to [0.0, 1.0] without any data augmentation
    rescaling = tf.keras.layers.Rescaling(1.0 / 255.0)
    test_ds = test_ds.map(lambda x, y: (rescaling(x), y), num_parallel_calls=tf.data.AUTOTUNE)
    return test_ds


def plot_confusion_matrix(
    cm: np.ndarray,
    class_labels: list,
    save_path: Path,
) -> None:
    """Render and save an aesthetic, publication-ready confusion matrix heatmap."""
    save_path.parent.mkdir(parents=True, exist_ok=True)

    # Convert snake_case class names to human-readable strings
    short_labels = [
        f"{CLASS_DISPLAY_INFO.get(c, {}).get('plant', '')[:3]}. {CLASS_DISPLAY_INFO.get(c, {}).get('disease', c)}"
        for c in class_labels
    ]

    plt.figure(figsize=(10, 8))
    sns.set_theme(style="white")
    ax = sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=short_labels,
        yticklabels=short_labels,
        linewidths=0.5,
        cbar_kws={"label": "Sample Count"},
    )
    plt.title("PlantGuard AI – Test Set Confusion Matrix", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Predicted Class", fontsize=11, fontweight="bold", labelpad=10)
    plt.ylabel("Ground Truth Class", fontsize=11, fontweight="bold", labelpad=10)
    plt.xticks(rotation=45, ha="right", fontsize=9)
    plt.yticks(rotation=0, fontsize=9)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()
    print(f"Confusion matrix saved to: {save_path}")


def evaluate(
    model_path: Optional[Path] = None,
    test_dir: Path = TEST_DIR,
) -> Dict[str, Any]:
    """Run full evaluation suite on independent test partition."""
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    if model_path is None:
        if MOBILENET_MODEL_PATH.exists():
            model_path = MOBILENET_MODEL_PATH
        elif CNN_MODEL_PATH.exists():
            model_path = CNN_MODEL_PATH
        else:
            raise FileNotFoundError("No trained model found for evaluation.")

    print(f"\n==========================================")
    print(f"PlantGuard AI Model Evaluation")
    print(f"Model Checkpoint: {model_path}")
    print(f"Test Partition:   {test_dir}")
    print(f"==========================================\n")

    test_ds = load_test_dataset(test_dir=test_dir)
    model = tf.keras.models.load_model(model_path)

    # Collect true labels and predictions
    y_true = []
    y_pred_probs = []

    print("Running forward inference over test dataset...")
    for images, labels in test_ds:
        probs = model.predict(images, verbose=0)
        y_pred_probs.extend(probs)
        y_true.extend(labels.numpy())

    y_true = np.array(y_true)
    y_pred_probs = np.array(y_pred_probs)
    y_pred = np.argmax(y_pred_probs, axis=1)

    total_test_samples = len(y_true)
    if total_test_samples == 0:
        raise ValueError("Test set contains zero samples.")

    # Calculate global metrics
    acc = accuracy_score(y_true, y_pred)
    prec_macro = precision_score(y_true, y_pred, average="macro", zero_division=0)
    rec_macro = recall_score(y_true, y_pred, average="macro", zero_division=0)
    f1_macro = f1_score(y_true, y_pred, average="macro", zero_division=0)

    prec_weighted = precision_score(y_true, y_pred, average="weighted", zero_division=0)
    rec_weighted = recall_score(y_true, y_pred, average="weighted", zero_division=0)
    f1_weighted = f1_score(y_true, y_pred, average="weighted", zero_division=0)

    cm = confusion_matrix(y_true, y_pred, labels=list(range(len(CLASS_NAMES))))
    clf_report = classification_report(
        y_true,
        y_pred,
        labels=list(range(len(CLASS_NAMES))),
        target_names=CLASS_NAMES,
        output_dict=True,
        zero_division=0,
    )

    print("\n--- Test Evaluation Results ---")
    print(f"Total Test Samples:   {total_test_samples}")
    print(f"Accuracy:             {acc * 100:.2f}%")
    print(f"Macro Precision:      {prec_macro * 100:.2f}%")
    print(f"Macro Recall:         {rec_macro * 100:.2f}%")
    print(f"Macro F1-Score:       {f1_macro * 100:.2f}%")
    print(f"Weighted F1-Score:    {f1_weighted * 100:.2f}%")
    print("\nClassification Report:")
    print(classification_report(y_true, y_pred, labels=list(range(len(CLASS_NAMES))), target_names=CLASS_NAMES, zero_division=0))

    # Generate Confusion Matrix image
    plot_confusion_matrix(cm, CLASS_NAMES, CONFUSION_MATRIX_PATH)

    # Per-class breakdown
    per_class_metrics = {}
    for idx, cls in enumerate(CLASS_NAMES):
        cls_dict = clf_report.get(cls, {})
        disp = CLASS_DISPLAY_INFO.get(cls, {})
        per_class_metrics[cls] = {
            "plant": disp.get("plant", cls),
            "disease": disp.get("disease", cls),
            "precision": round(float(cls_dict.get("precision", 0.0)), 4),
            "recall": round(float(cls_dict.get("recall", 0.0)), 4),
            "f1_score": round(float(cls_dict.get("f1-score", 0.0)), 4),
            "support": int(cls_dict.get("support", 0)),
        }

    metrics_payload = {
        "model_name": Path(model_path).name,
        "total_test_samples": total_test_samples,
        "classes_count": len(CLASS_NAMES),
        "accuracy": round(float(acc), 4),
        "accuracy_percentage": round(float(acc) * 100, 2),
        "precision_macro": round(float(prec_macro), 4),
        "recall_macro": round(float(rec_macro), 4),
        "f1_macro": round(float(f1_macro), 4),
        "precision_weighted": round(float(prec_weighted), 4),
        "recall_weighted": round(float(rec_weighted), 4),
        "f1_weighted": round(float(f1_weighted), 4),
        "confusion_matrix": cm.tolist(),
        "class_labels": CLASS_NAMES,
        "per_class_metrics": per_class_metrics,
        "limitations": (
            "Model performance may degrade in unconstrained field environments with "
            "severe shadow occlusion, dual coinfections, or non-foliar diseases. "
            "Evaluations reflect independent holdout test data."
        ),
    }

    # Save to metrics.json
    with open(METRICS_FILE, "w", encoding="utf-8") as f:
        json.dump(metrics_payload, f, indent=2)
    print(f"Evaluation metrics saved to: {METRICS_FILE}")

    return metrics_payload


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PlantGuard AI Model Evaluator")
    parser.add_argument("--model", type=str, default=None, help="Path to model file")
    parser.add_argument("--test-dir", type=str, default=str(TEST_DIR), help="Path to test directory")
    args = parser.parse_args()

    evaluate(
        model_path=Path(args.model) if args.model else None,
        test_dir=Path(args.test_dir),
    )
