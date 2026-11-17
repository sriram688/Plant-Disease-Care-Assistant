"""SQLAlchemy ORM models for PlantGuard AI prediction history and audit tracking."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from backend.database import Base


class PredictionRecord(Base):
    """Stores leaf scan diagnostic history and predictions."""
    __tablename__ = "prediction_records"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    filename = Column(String(255), nullable=False)
    image_url = Column(String(500), nullable=True)
    plant = Column(String(100), nullable=False)
    disease = Column(String(150), nullable=False)
    status = Column(String(50), nullable=False)  # "Healthy" or "Diseased"
    confidence = Column(Float, nullable=False)
    severity = Column(String(50), nullable=False)  # "None", "Low", "Medium", "High"
    severity_percentage = Column(Float, nullable=True)
    scientific_name = Column(String(200), nullable=True)
    explanation = Column(Text, nullable=True)
    user_feedback = Column(String(50), nullable=True)  # "helpful", "incorrect", etc.
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    def to_dict(self):
        return {
            "id": self.id,
            "filename": self.filename,
            "image_url": self.image_url,
            "plant": self.plant,
            "disease": self.disease,
            "status": self.status,
            "confidence": round(self.confidence, 4),
            "severity": self.severity,
            "severity_percentage": self.severity_percentage,
            "scientific_name": self.scientific_name,
            "explanation": self.explanation,
            "user_feedback": self.user_feedback,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
