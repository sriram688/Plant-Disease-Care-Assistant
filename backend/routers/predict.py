"""Prediction router for PlantGuard AI.

Accepts image uploads, performs validation, runs inference and severity assessment,
records scan metadata to the database, and returns comprehensive disease diagnostics.
"""

import uuid
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import PredictionRecord
from backend.schemas import PredictionResponse
from src.predict import prediction_engine
from src.preprocessing import validate_image_file, ImageValidationError
from src.config import UPLOADS_DIR

router = APIRouter(prefix="/api", tags=["Prediction"])


@router.post(
    "/predict",
    response_model=PredictionResponse,
    summary="Predict plant disease from leaf image",
    description="Accepts a leaf image file (JPEG, PNG, WebP), predicts disease status, estimates severity, and returns care advice.",
)
async def predict_plant_disease(
    file: UploadFile = File(..., description="Plant leaf image file"),
    db: Session = Depends(get_db),
):
    """Diagnose leaf image and return structured disease prognosis."""
    # Ensure uploads directory exists
    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

    # Read uploaded bytes
    try:
        content = await file.read()
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to read uploaded file: {str(exc)}",
        )

    # Validate file format and size
    try:
        validate_image_file(content, filename=file.filename)
    except ImageValidationError as val_err:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(val_err),
        )

    # Persist uploaded image for history preview and reference
    file_ext = Path(file.filename or "upload.jpg").suffix.lower() or ".jpg"
    unique_name = f"{uuid.uuid4().hex[:12]}{file_ext}"
    saved_file_path = UPLOADS_DIR / unique_name

    try:
        with open(saved_file_path, "wb") as f:
            f.write(content)
    except Exception as io_err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to store uploaded image: {str(io_err)}",
        )

    # Execute ML inference and severity estimation
    try:
        prediction_result = prediction_engine.predict(content)
    except FileNotFoundError as fnf_err:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Inference model is not currently available: {str(fnf_err)}",
        )
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Inference processing failed: {str(err)}",
        )

    # Log record to SQLite database
    image_relative_url = f"/uploads/{unique_name}"
    db_record = PredictionRecord(
        filename=unique_name,
        image_url=image_relative_url,
        plant=prediction_result["plant"],
        disease=prediction_result["disease"],
        status=prediction_result["status"],
        confidence=prediction_result["confidence"],
        severity=prediction_result["severity"],
        severity_percentage=prediction_result["severity_details"]["affected_percentage"],
        scientific_name=prediction_result["scientific_name"],
        explanation=prediction_result["explanation"],
    )

    try:
        db.add(db_record)
        db.commit()
        db.refresh(db_record)
        record_id = db_record.id
    except Exception:
        db.rollback()
        record_id = None

    # Merge ID and image url into response
    response_payload = {
        "id": record_id,
        "filename": unique_name,
        "image_url": image_relative_url,
        **prediction_result,
    }

    return response_payload
