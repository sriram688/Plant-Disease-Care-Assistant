"""Generate and curate demo sample images for frontend and CLI quick-testing."""

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from scripts.prepare_dataset import generate_synthetic_leaf, TARGET_CLASSES

SAMPLES_DIR = BASE_DIR / "samples"
FRONTEND_SAMPLES_DIR = BASE_DIR / "frontend" / "public" / "samples"


def create_demo_samples() -> None:
    """Generate high-quality demo test images for instant UI testing."""
    SAMPLES_DIR.mkdir(parents=True, exist_ok=True)
    FRONTEND_SAMPLES_DIR.mkdir(parents=True, exist_ok=True)

    samples = [
        ("tomato_early_blight", "tomato_early_blight_sample.jpg", 5001),
        ("tomato_healthy", "tomato_healthy_sample.jpg", 5002),
        ("tomato_late_blight", "tomato_late_blight_sample.jpg", 5003),
        ("potato_early_blight", "potato_early_blight_sample.jpg", 5004),
        ("potato_healthy", "potato_healthy_sample.jpg", 5005),
        ("pepper_bacterial_spot", "pepper_bacterial_spot_sample.jpg", 5006),
        ("pepper_healthy", "pepper_healthy_sample.jpg", 5007),
    ]

    print("Generating demo test sample images...")
    for cls, fname, seed in samples:
        target1 = SAMPLES_DIR / fname
        target2 = FRONTEND_SAMPLES_DIR / fname
        generate_synthetic_leaf(cls, target1, seed=seed)
        generate_synthetic_leaf(cls, target2, seed=seed)
        print(f"  [+] Created {fname}")

    print("Demo sample images ready.")


if __name__ == "__main__":
    create_demo_samples()
