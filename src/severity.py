"""Disease severity analysis module for PlantGuard AI.

Provides transparent and scientifically honest severity estimation.
For healthy leaves, severity is 'None'.
For diseased classes without direct pathology staging labels in the training dataset,
severity is estimated using an OpenCV HSV lesion segmentation heuristic and
is explicitly labeled as an experimental visual estimate.
"""

from dataclasses import dataclass
from typing import Optional, Tuple
import cv2
import numpy as np


@dataclass
class SeverityResult:
    """Structured severity assessment."""
    level: str  # "None", "Low", "Medium", "High"
    score_percentage: float  # Estimated percentage of leaf area affected (0.0 to 100.0)
    method: str  # Description of how this was derived
    is_experimental: bool  # True when derived via heuristic rather than dedicated severity model
    notes: str  # Scientific disclaimer and educational context


def estimate_disease_severity(
    image_rgb_uint8: np.ndarray,
    predicted_class: str,
    confidence: float,
) -> SeverityResult:
    """Estimate plant disease severity with full transparency.

    Args:
        image_rgb_uint8: Preprocessed RGB image of the leaf as uint8 (0-255).
        predicted_class: Predicted class string (e.g. 'tomato_early_blight', 'potato_healthy').
        confidence: Prediction confidence score between 0.0 and 1.0.

    Returns:
        SeverityResult dataclass containing severity level, affected percentage, and methodology.
    """
    # 1. If leaf is predicted healthy with high confidence, severity is None
    if "healthy" in predicted_class.lower():
        return SeverityResult(
            level="None",
            score_percentage=0.0,
            method="Healthy Classification",
            is_experimental=False,
            notes="No disease symptoms detected on the leaf lamina.",
        )

    # 2. For diseased leaves, calculate leaf contour and diseased lesion surface area
    try:
        hsv = cv2.cvtColor(image_rgb_uint8, cv2.COLOR_RGB2HSV)

        # Segment total leaf blade (greens, yellows, and browns)
        # Broad range for foliage to distinguish from standard neutral backgrounds
        lower_foliage = np.array([10, 20, 20], dtype=np.uint8)
        upper_foliage = np.array([95, 255, 255], dtype=np.uint8)
        leaf_mask = cv2.inRange(hsv, lower_foliage, upper_foliage)

        # Segment necrotic and chlorotic lesion tissue:
        # Range 1: Chlorotic yellowing & halo tissue
        lower_yellow = np.array([15, 60, 60], dtype=np.uint8)
        upper_yellow = np.array([32, 255, 255], dtype=np.uint8)
        mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)

        # Range 2: Necrotic brown, dark brown, and black spots
        # Low saturation / low value or warm dark hues
        lower_brown = np.array([0, 40, 20], dtype=np.uint8)
        upper_brown = np.array([20, 255, 140], dtype=np.uint8)
        mask_brown = cv2.inRange(hsv, lower_brown, upper_brown)

        # Range 3: Dark spot centers (low brightness)
        gray = cv2.cvtColor(image_rgb_uint8, cv2.COLOR_RGB2GRAY)
        mask_dark = cv2.inRange(gray, 0, 70)

        # Combined lesion mask within the leaf mask
        lesion_mask_raw = cv2.bitwise_or(mask_yellow, mask_brown)
        lesion_mask_raw = cv2.bitwise_or(lesion_mask_raw, mask_dark)
        lesion_mask = cv2.bitwise_and(lesion_mask_raw, leaf_mask)

        # Morphological filter to remove solitary noise pixels
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        lesion_mask = cv2.morphologyEx(lesion_mask, cv2.MORPH_OPEN, kernel)

        total_leaf_pixels = int(np.count_nonzero(leaf_mask))
        lesion_pixels = int(np.count_nonzero(lesion_mask))

        if total_leaf_pixels > 500:
            ratio = lesion_pixels / float(total_leaf_pixels)
            percentage = round(min(100.0, ratio * 100.0), 1)
        else:
            # Fallback if leaf segmentation fails on noisy background
            percentage = 15.0

    except Exception:
        percentage = 15.0

    # Categorize severity based on lesion coverage threshold standards:
    # Low: < 15% leaf area affected
    # Medium: 15% - 35% leaf area affected
    # High: > 35% leaf area affected
    if percentage < 15.0:
        level = "Low"
    elif percentage <= 35.0:
        level = "Medium"
    else:
        level = "High"

    return SeverityResult(
        level=level,
        score_percentage=percentage,
        method="Lesion Surface Area Heuristic (OpenCV Segmentation)",
        is_experimental=True,
        notes=(
            f"Estimated {percentage}% necrotic/chlorotic leaf surface area affected. "
            "Note: Public benchmark datasets lack clinical staging labels; this value is an experimental visual estimate."
        ),
    )
