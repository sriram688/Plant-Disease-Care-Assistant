"""Pydantic data validation schemas for PlantGuard AI API requests and responses."""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class SeverityDetails(BaseModel):
    level: str
    affected_percentage: float
    method: str
    is_experimental: bool
    notes: str


class CareDetails(BaseModel):
    immediate_action: str
    organic_treatment: str
    chemical_treatment: str
    cultural_practices: str
    prevention: str


class TopPredictionItem(BaseModel):
    class_name: str
    plant: str
    disease: str
    status: str
    confidence: float
    confidence_percentage: float


class PredictionResponse(BaseModel):
    id: Optional[int] = None
    filename: Optional[str] = None
    image_url: Optional[str] = None
    class_name: str
    plant: str
    disease: str
    status: str
    confidence: float
    confidence_percentage: float
    severity: str
    severity_details: SeverityDetails
    scientific_name: str
    description: str
    symptoms: str
    diagnostic_cues: Optional[str] = ""
    recommendations: List[str]
    care_details: CareDetails
    top_predictions: List[TopPredictionItem]
    explanation: str
    disclaimer: str


class DiseaseInfoResponse(BaseModel):
    class_name: str
    plant: str
    disease: str
    status: str
    scientific_name: str
    description: str
    symptoms: str
    severity_guidelines: str
    diagnostic_cues: str
    care: CareDetails


class HistoryItemResponse(BaseModel):
    id: int
    filename: str
    image_url: Optional[str] = None
    plant: str
    disease: str
    status: str
    confidence: float
    severity: str
    severity_percentage: Optional[float] = None
    scientific_name: Optional[str] = None
    explanation: Optional[str] = None
    user_feedback: Optional[str] = None
    created_at: Optional[str] = None


class FeedbackRequest(BaseModel):
    feedback: str = Field(..., description="'helpful', 'accurate', 'incorrect', etc.")


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    active_model: str
    classes_count: int
    version: str
    framework: str


class ModelMetricsResponse(BaseModel):
    model_name: str
    total_test_samples: int
    classes_count: int
    accuracy: float
    accuracy_percentage: float
    precision_macro: float
    recall_macro: float
    f1_macro: float
    precision_weighted: float
    recall_weighted: float
    f1_weighted: float
    confusion_matrix: List[List[int]]
    class_labels: List[str]
    per_class_metrics: Dict[str, Any]
    limitations: str
    has_curves: bool
    has_confusion_matrix_img: bool
