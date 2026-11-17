"""History management and feedback router for PlantGuard AI."""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc

from backend.database import get_db
from backend.models import PredictionRecord
from backend.schemas import HistoryItemResponse, FeedbackRequest

router = APIRouter(prefix="/api/history", tags=["History"])


@router.get(
    "",
    response_model=List[HistoryItemResponse],
    summary="Get recent diagnosis history",
    description="Returns previous leaf scans, diagnostic outcomes, confidence, and severity scores.",
)
def get_prediction_history(
    limit: int = Query(50, ge=1, le=200),
    plant: Optional[str] = Query(None, description="Filter by plant: Tomato, Potato, Pepper"),
    status_filter: Optional[str] = Query(None, alias="status", description="Filter by 'Healthy' or 'Diseased'"),
    db: Session = Depends(get_db),
):
    """Retrieve history of past predictions."""
    query = db.query(PredictionRecord)

    if plant:
        query = query.filter(PredictionRecord.plant.ilike(f"%{plant}%"))
    if status_filter:
        query = query.filter(PredictionRecord.status.ilike(f"%{status_filter}%"))

    records = query.order_by(desc(PredictionRecord.created_at)).limit(limit).all()
    return [r.to_dict() for r in records]


@router.get(
    "/{record_id}",
    response_model=HistoryItemResponse,
    summary="Get specific diagnosis record",
)
def get_history_record(record_id: int, db: Session = Depends(get_db)):
    """Retrieve a single scan record by ID."""
    record = db.query(PredictionRecord).filter(PredictionRecord.id == record_id).first()
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Prediction record #{record_id} not found.",
        )
    return record.to_dict()


@router.delete(
    "/{record_id}",
    summary="Delete diagnosis record",
)
def delete_history_record(record_id: int, db: Session = Depends(get_db)):
    """Remove a diagnosis scan from the database."""
    record = db.query(PredictionRecord).filter(PredictionRecord.id == record_id).first()
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Prediction record #{record_id} not found.",
        )

    db.delete(record)
    db.commit()
    return {"message": f"Record #{record_id} deleted successfully."}


@router.post(
    "/{record_id}/feedback",
    summary="Submit user feedback on diagnosis accuracy",
)
def submit_prediction_feedback(
    record_id: int,
    payload: FeedbackRequest,
    db: Session = Depends(get_db),
):
    """Log farmer or researcher accuracy feedback on an inference outcome."""
    record = db.query(PredictionRecord).filter(PredictionRecord.id == record_id).first()
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Prediction record #{record_id} not found.",
        )

    record.user_feedback = payload.feedback
    db.commit()
    return {"message": "Feedback recorded. Thank you for contributing to PlantGuard AI accuracy improvement!"}
