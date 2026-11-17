"""Unit tests for image preprocessing and validation in PlantGuard AI."""

import io
import pytest
import numpy as np
from PIL import Image

from src.preprocessing import (
    load_and_preprocess_image,
    validate_image_file,
    extract_leaf_contour,
    ImageValidationError,
)
from src.config import IMAGE_SIZE


def create_test_image_bytes(format="JPEG", size=(300, 300), color=(34, 139, 34)) -> bytes:
    """Helper creating memory buffer of valid RGB test image."""
    img = Image.new("RGB", size, color=color)
    buf = io.BytesIO()
    img.save(buf, format=format)
    return buf.getvalue()


def test_validate_image_valid():
    """Test valid JPEG bytes pass validation without error."""
    img_bytes = create_test_image_bytes("JPEG")
    validate_image_file(img_bytes, "sample.jpg")


def test_validate_image_empty():
    """Test empty bytes raise ImageValidationError."""
    with pytest.raises(ImageValidationError, match="empty"):
        validate_image_file(b"", "empty.jpg")


def test_validate_image_corrupted():
    """Test malformed bytes raise ImageValidationError."""
    with pytest.raises(ImageValidationError, match="Invalid or corrupted"):
        validate_image_file(b"NOT_AN_IMAGE_STRING", "corrupted.jpg")


def test_validate_image_invalid_extension():
    """Test unsupported file extension is rejected."""
    img_bytes = create_test_image_bytes("JPEG")
    with pytest.raises(ImageValidationError, match="Unsupported image format"):
        validate_image_file(img_bytes, "malicious.exe")


def test_load_and_preprocess_image_normalized():
    """Test image is resized to target (224, 224) and scaled to [0.0, 1.0]."""
    img_bytes = create_test_image_bytes("JPEG", size=(400, 500))
    arr = load_and_preprocess_image(img_bytes, target_size=IMAGE_SIZE, normalize=True)

    assert isinstance(arr, np.ndarray)
    assert arr.shape == (224, 224, 3)
    assert arr.dtype == np.float32
    assert arr.min() >= 0.0
    assert arr.max() <= 1.0


def test_load_and_preprocess_image_uint8():
    """Test image is returned as uint8 when normalize=False."""
    img_bytes = create_test_image_bytes("PNG", size=(100, 100))
    arr = load_and_preprocess_image(img_bytes, target_size=IMAGE_SIZE, normalize=False)

    assert isinstance(arr, np.ndarray)
    assert arr.shape == (224, 224, 3)
    assert arr.dtype == np.uint8


def test_extract_leaf_contour():
    """Test leaf contour segmentation returns binary mask and coverage float."""
    # Green image simulates foliage
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    img[20:80, 20:80] = [34, 139, 34]  # Forest Green

    mask, pct = extract_leaf_contour(img)
    assert mask.shape == (100, 100)
    assert 0.0 <= pct <= 100.0
    assert pct > 0.0
