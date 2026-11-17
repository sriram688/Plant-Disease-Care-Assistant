"""Unit tests for disease and care metadata resolution."""

from src.metadata_service import metadata_service
from src.config import CLASS_NAMES


def test_metadata_all_classes_present():
    """Verify metadata is defined for all official benchmark classes."""
    for cls in CLASS_NAMES:
        info = metadata_service.get_disease_info(cls)
        assert "plant" in info
        assert "disease" in info
        assert "symptoms" in info
        assert "description" in info
        assert info["plant"] != "Unknown"


def test_care_recommendations_all_classes():
    """Verify care recommendations contain actionable instructions."""
    for cls in CLASS_NAMES:
        care = metadata_service.get_care_recommendations(cls)
        assert "immediate_action" in care
        assert "organic_treatment" in care
        assert "cultural_practices" in care
        assert "prevention" in care
        assert len(care["immediate_action"]) > 10


def test_disease_catalog_completeness():
    """Verify full catalog contains all registered classes."""
    catalog = metadata_service.get_all_diseases()
    assert len(catalog) == len(CLASS_NAMES)
    class_set = {item["class_name"] for item in catalog}
    assert class_set == set(CLASS_NAMES)


def test_unknown_class_fallback():
    """Verify metadata service handles uncataloged classes gracefully."""
    info = metadata_service.get_disease_info("banana_panama_disease")
    assert info["plant"] == "Unknown"
    assert "banana_panama_disease" in info["disease"]
