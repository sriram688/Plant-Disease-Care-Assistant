"""Image preprocessing and augmentation pipeline for PlantGuard AI.

Handles robust image loading, validation, color space normalization,
biologically sound data augmentation, and OpenCV-based leaf masking.
"""

import io
from pathlib import Path
from typing import Union, Tuple, Optional
import numpy as np
from PIL import Image, UnidentifiedImageError
import cv2

from src.config import IMAGE_SIZE, INPUT_SHAPE


SUPPORTED_FORMATS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}
MAX_IMAGE_FILE_SIZE_BYTES = 15 * 1024 * 1024  # 15 MB limit


class ImageValidationError(ValueError):
    """Raised when an uploaded image fails validation."""
    pass


def validate_image_file(file_content: bytes, filename: Optional[str] = None) -> None:
    """Validate raw file bytes to ensure they represent a valid, safe image.

    Args:
        file_content: Raw bytes of the image file.
        filename: Optional original filename to verify extension.

    Raises:
        ImageValidationError: If file is empty, too large, has invalid extension, or cannot be parsed.
    """
    if not file_content or len(file_content) == 0:
        raise ImageValidationError("Uploaded image file is empty.")

    if len(file_content) > MAX_IMAGE_FILE_SIZE_BYTES:
        raise ImageValidationError(
            f"Image exceeds maximum allowable size of {MAX_IMAGE_FILE_SIZE_BYTES // (1024 * 1024)}MB."
        )

    if filename:
        ext = Path(filename).suffix.lower()
        if ext and ext not in SUPPORTED_FORMATS:
            raise ImageValidationError(
                f"Unsupported image format '{ext}'. Allowed formats: {', '.join(sorted(SUPPORTED_FORMATS))}"
            )

    try:
        with Image.open(io.BytesIO(file_content)) as img:
            img.verify()
    except (UnidentifiedImageError, Exception) as err:
        raise ImageValidationError(f"Invalid or corrupted image data: {str(err)}") from err


def load_and_preprocess_image(
    source: Union[str, Path, bytes],
    target_size: Tuple[int, int] = IMAGE_SIZE,
    normalize: bool = True,
) -> np.ndarray:
    """Load an image from a path or raw bytes, convert to RGB, resize, and optionally normalize.

    Args:
        source: File path (str/Path) or raw image bytes.
        target_size: Desired (height, width) tuple. Default: (224, 224).
        normalize: Whether to scale pixel values to [0.0, 1.0]. Default: True.

    Returns:
        np.ndarray: Preprocessed image array of shape (height, width, 3) and dtype float32 (if normalized)
                    or uint8.

    Raises:
        ImageValidationError: If the image cannot be read or processed.
    """
    try:
        if isinstance(source, (str, Path)):
            path = Path(source)
            if not path.is_file():
                raise ImageValidationError(f"Image file does not exist: {path}")
            with open(path, "rb") as f:
                content = f.read()
        elif isinstance(source, bytes):
            content = source
        else:
            raise ImageValidationError("Source must be a file path or raw bytes.")

        validate_image_file(content)

        # Open with PIL for correct color-profile & EXIF orientation handling
        with Image.open(io.BytesIO(content)) as pil_img:
            # Handle EXIF rotation if present
            try:
                from PIL import ImageOps
                pil_img = ImageOps.exif_transpose(pil_img)
            except Exception:
                pass

            # Convert to RGB (strips alpha channel if PNG, or converts grayscale)
            rgb_img = pil_img.convert("RGB")
            # Resize using high-quality Lanczos resampling
            resized_img = rgb_img.resize(target_size, Image.Resampling.LANCZOS)
            arr = np.array(resized_img, dtype=np.float32 if normalize else np.uint8)

        if normalize:
            arr = arr / 255.0

        return arr

    except ImageValidationError:
        raise
    except Exception as exc:
        raise ImageValidationError(f"Failed to preprocess image: {str(exc)}") from exc


def get_data_augmentation_layers():
    """Build TensorFlow Keras data augmentation sequential block.

    Applied ONLY during training to preserve biological realism.
    Includes gentle rotation (±15°), horizontal flipping, slight zoom (±8%),
    minor translations, and slight brightness adjustments.
    Vertical flip is omitted or kept minimal because natural leaf photos have gravity orientation.
    """
    import tensorflow as tf

    return tf.keras.Sequential(
        [
            tf.keras.layers.RandomFlip("horizontal", name="aug_horizontal_flip"),
            tf.keras.layers.RandomRotation(0.06, fill_mode="nearest", name="aug_rotation"),
            tf.keras.layers.RandomZoom(height_factor=(-0.08, 0.08), fill_mode="nearest", name="aug_zoom"),
            tf.keras.layers.RandomTranslation(
                height_factor=0.04, width_factor=0.04, fill_mode="nearest", name="aug_translation"
            ),
            tf.keras.layers.RandomBrightness(0.08, value_range=(0.0, 1.0), name="aug_brightness"),
        ],
        name="plant_data_augmentation",
    )


def extract_leaf_contour(image_rgb_uint8: np.ndarray) -> Tuple[np.ndarray, float]:
    """Segment leaf from background using OpenCV color thresholding in HSV color space.

    Args:
        image_rgb_uint8: Input image as RGB numpy array of shape (H, W, 3) in [0, 255].

    Returns:
        Tuple of (binary mask of shape (H, W), leaf coverage percentage [0-100]).
    """
    hsv = cv2.cvtColor(image_rgb_uint8, cv2.COLOR_RGB2HSV)

    # Broad range covering healthy greens and chlorotic/brown/diseased foliage
    # Leaves range from yellow-green to dark green, down to brown/yellow
    lower_foliage = np.array([15, 25, 25], dtype=np.uint8)
    upper_foliage = np.array([95, 255, 255], dtype=np.uint8)

    foliage_mask = cv2.inRange(hsv, lower_foliage, upper_foliage)

    # Morphological cleaning to remove salt-and-pepper noise
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    foliage_mask = cv2.morphologyEx(foliage_mask, cv2.MORPH_OPEN, kernel)
    foliage_mask = cv2.morphologyEx(foliage_mask, cv2.MORPH_CLOSE, kernel)

    total_pixels = foliage_mask.shape[0] * foliage_mask.shape[1]
    leaf_pixels = int(np.count_nonzero(foliage_mask))
    coverage_pct = (leaf_pixels / total_pixels) * 100.0

    return foliage_mask, round(coverage_pct, 2)
