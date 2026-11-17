"""Diseases library and metadata router for PlantGuard AI."""

from typing import List
from fastapi import APIRouter, HTTPException, status

from backend.schemas import DiseaseInfoResponse
from src.metadata_service import metadata_service
from src.config import CLASS_NAMES

router = APIRouter(prefix="/api/diseases", tags=["Diseases"])


@router.get(
    "",
    response_model=List[DiseaseInfoResponse],
    summary="Get full plant disease knowledge base",
    description="Returns list of all supported plant disease profiles with symptoms, severity guidelines, and care recommendations.",
)
def get_all_diseases():
    """Retrieve all cataloged disease specifications."""
    return metadata_service.get_all_diseases()


@router.get(
    "/{class_name}",
    response_model=DiseaseInfoResponse,
    summary="Get disease details by class name",
    description="Retrieve extensive pathology and treatment information for a specific class.",
)
def get_disease_by_class(class_name: str):
    """Retrieve single disease profile."""
    if class_name not in CLASS_NAMES:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Disease class '{class_name}' not found. Supported classes: {', '.join(CLASS_NAMES)}",
        )

    info = metadata_service.get_disease_info(class_name)
    care = metadata_service.get_care_recommendations(class_name)
    return {
        "class_name": class_name,
        **info,
        "care": care,
    }
