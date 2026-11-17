"""Configuration module for PlantGuard AI.

Centralizes paths, hyperparameters, model constants, and class registries.
"""

from pathlib import Path
from typing import List, Tuple, Dict

# Base project paths
BASE_DIR: Path = Path(__file__).resolve().parent.parent
DATASET_DIR: Path = BASE_DIR / "dataset"
TRAIN_DIR: Path = DATASET_DIR / "train"
VAL_DIR: Path = DATASET_DIR / "validation"
TEST_DIR: Path = DATASET_DIR / "test"

MODELS_DIR: Path = BASE_DIR / "models"
METADATA_DIR: Path = BASE_DIR / "metadata"
UPLOADS_DIR: Path = BASE_DIR / "backend" / "uploads"

DISEASE_INFO_FILE: Path = METADATA_DIR / "disease_info.csv"
CARE_RECOMMENDATIONS_FILE: Path = METADATA_DIR / "care_recommendations.csv"

# Model artifacts
MOBILENET_MODEL_PATH: Path = MODELS_DIR / "plantguard_mobilenetv2.keras"
CNN_MODEL_PATH: Path = MODELS_DIR / "plantguard_cnn.keras"
METRICS_FILE: Path = MODELS_DIR / "metrics.json"
CONFUSION_MATRIX_PATH: Path = MODELS_DIR / "confusion_matrix.png"
TRAINING_CURVES_PATH: Path = MODELS_DIR / "training_curves.png"

# Hyperparameters & input dimensions
IMAGE_SIZE: Tuple[int, int] = (224, 224)
INPUT_SHAPE: Tuple[int, int, int] = (224, 224, 3)
CHANNELS: int = 3
BATCH_SIZE: int = 32
DEFAULT_EPOCHS: int = 15
LEARNING_RATE: float = 0.0005
RANDOM_SEED: int = 42

# Official benchmark classes for PlantGuard AI
CLASS_NAMES: List[str] = [
    "pepper_bacterial_spot",
    "pepper_healthy",
    "potato_early_blight",
    "potato_healthy",
    "potato_late_blight",
    "tomato_bacterial_spot",
    "tomato_early_blight",
    "tomato_healthy",
    "tomato_late_blight",
]

NUM_CLASSES: int = len(CLASS_NAMES)

# Human-readable labels and plant categories
CLASS_DISPLAY_INFO: Dict[str, Dict[str, str]] = {
    "pepper_bacterial_spot": {"plant": "Pepper", "disease": "Bacterial Spot", "status": "Diseased"},
    "pepper_healthy": {"plant": "Pepper", "disease": "Healthy", "status": "Healthy"},
    "potato_early_blight": {"plant": "Potato", "disease": "Early Blight", "status": "Diseased"},
    "potato_healthy": {"plant": "Potato", "disease": "Healthy", "status": "Healthy"},
    "potato_late_blight": {"plant": "Potato", "disease": "Late Blight", "status": "Diseased"},
    "tomato_bacterial_spot": {"plant": "Tomato", "disease": "Bacterial Spot", "status": "Diseased"},
    "tomato_early_blight": {"plant": "Tomato", "disease": "Early Blight", "status": "Diseased"},
    "tomato_healthy": {"plant": "Tomato", "disease": "Healthy", "status": "Healthy"},
    "tomato_late_blight": {"plant": "Tomato", "disease": "Late Blight", "status": "Diseased"},
}

# Severity categories
SEVERITY_LEVELS: List[str] = ["None", "Low", "Medium", "High"]
