"""Model metrics, evaluation reporting, and diagnostic artifacts router for PlantGuard AI."""

import json
from pathlib import Path
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse

from backend.schemas import ModelMetricsResponse
from src.config import (
    METRICS_FILE,
    CONFUSION_MATRIX_PATH,
    TRAINING_CURVES_PATH,
    MOBILENET_MODEL_PATH,
    CNN_MODEL_PATH,
    CLASS_NAMES,
)

router = APIRouter(prefix="/api/model-info", tags=["Model Information"])


@router.get(
    "",
    response_model=ModelMetricsResponse,
    summary="Get independent model evaluation metrics",
    description="Returns genuine holdout test set evaluation metrics including accuracy, precision, recall, F1, and confusion matrix.",
)
def get_model_metrics():
    """Retrieve model evaluation metrics and performance profile."""
    if not METRICS_FILE.exists():
        # Provide fallback baseline representation if evaluate has not yet run
        active_model = "MobileNetV2" if MOBILENET_MODEL_PATH.exists() else "Custom CNN"
        return {
            "model_name": active_model,
            "total_test_samples": 0,
            "classes_count": len(CLASS_NAMES),
            "accuracy": 0.0,
            "accuracy_percentage": 0.0,
            "precision_macro": 0.0,
            "recall_macro": 0.0,
            "f1_macro": 0.0,
            "precision_weighted": 0.0,
            "recall_weighted": 0.0,
            "f1_weighted": 0.0,
            "confusion_matrix": [[0] * len(CLASS_NAMES) for _ in range(len(CLASS_NAMES))],
            "class_labels": CLASS_NAMES,
            "per_class_metrics": {},
            "limitations": "Evaluation pending. Run 'python -m src.evaluate' to generate independent test metrics.",
            "has_curves": TRAINING_CURVES_PATH.exists(),
            "has_confusion_matrix_img": CONFUSION_MATRIX_PATH.exists(),
        }

    try:
        with open(METRICS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        data["has_curves"] = TRAINING_CURVES_PATH.exists()
        data["has_confusion_matrix_img"] = CONFUSION_MATRIX_PATH.exists()
        return data
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to read evaluation metrics: {str(exc)}",
        )


@router.get(
    "/confusion-matrix",
    summary="Get confusion matrix plot image",
)
def get_confusion_matrix_image():
    """Download/view holdout confusion matrix plot."""
    if not CONFUSION_MATRIX_PATH.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Confusion matrix image has not been generated yet.",
        )
    return FileResponse(CONFUSION_MATRIX_PATH, media_type="image/png")


@router.get(
    "/training-curves",
    summary="Get training loss and accuracy curve plot",
)
def get_training_curves_image():
    """Download/view training & validation curve plot."""
    if not TRAINING_CURVES_PATH.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Training curves image has not been generated yet.",
        )
    return FileResponse(TRAINING_CURVES_PATH, media_type="image/png")
