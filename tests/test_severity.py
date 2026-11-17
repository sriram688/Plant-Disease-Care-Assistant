"""Unit tests for disease severity assessment logic."""

import numpy as np
import pytest

from src.severity import estimate_disease_severity, SeverityResult


def test_severity_healthy_class():
    """Verify healthy leaves always yield None severity without experimental claims."""
    dummy_img = np.full((224, 224, 3), 120, dtype=np.uint8)

    res = estimate_disease_severity(dummy_img, "tomato_healthy", confidence=0.98)
    assert isinstance(res, SeverityResult)
    assert res.level == "None"
    assert res.score_percentage == 0.0
    assert res.is_experimental is False

    res_potato = estimate_disease_severity(dummy_img, "potato_healthy", confidence=0.95)
    assert res_potato.level == "None"


def test_severity_diseased_class_with_experimental_notice():
    """Verify diseased leaves yield Low/Medium/High with explicit experimental disclosure."""
    # Leaf with foliage green background and dark lesions
    img = np.full((224, 224, 3), 40, dtype=np.uint8)
    # Foliage area
    img[30:190, 30:190] = [35, 130, 35]
    # Lesion spot
    img[80:120, 80:120] = [40, 25, 10]

    res = estimate_disease_severity(img, "tomato_early_blight", confidence=0.91)
    assert res.level in ["Low", "Medium", "High"]
    assert res.is_experimental is True
    assert "experimental" in res.notes.lower()
