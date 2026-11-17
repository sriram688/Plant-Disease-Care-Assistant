"""Master pipeline execution script for PlantGuard AI.

Executes full automated workflow:
1. Dataset preparation and validation
2. Model training with early stopping and checkpointing
3. Comprehensive test set evaluation & metric logging
4. Demo sample assets generation
"""

import sys
import argparse
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from scripts.prepare_dataset import generate_starter_dataset, TRAIN_DIR, TARGET_CLASSES
from scripts.demo_samples import create_demo_samples
from src.train import train
from src.evaluate import evaluate
from src.config import MOBILENET_MODEL_PATH, CNN_MODEL_PATH


def run_pipeline(architecture: str = "mobilenetv2", epochs: int = 10, batch_size: int = 16) -> None:
    print("============================================================")
    print(">>> PLANTGUARD AI - AUTOMATED END-TO-END PIPELINE")
    print("============================================================\n")

    # Step 1: Ensure dataset exists
    has_data = all((TRAIN_DIR / cls).exists() and len(list((TRAIN_DIR / cls).glob("*.jpg"))) > 0 for cls in TARGET_CLASSES)
    if not has_data:
        print("Dataset not detected. Generating balanced starter dataset...")
        generate_starter_dataset(train_count_per_class=35, val_count_per_class=10, test_count_per_class=10)
    else:
        print("Existing dataset detected. Skipping starter dataset creation.")

    # Step 2: Generate sample images for UI
    create_demo_samples()

    # Step 3: Train model
    print(f"\nStep 3: Training {architecture.upper()} model for {epochs} epochs...")
    train(architecture=architecture, epochs=epochs, batch_size=batch_size)

    # Step 4: Evaluate model
    print("\nStep 4: Evaluating on independent holdout test set...")
    model_path = MOBILENET_MODEL_PATH if "mobilenet" in architecture.lower() else CNN_MODEL_PATH
    metrics = evaluate(model_path=model_path)

    print("\n" + "=" * 60)
    print(" PIPELINE EXECUTION SUCCESSFUL!")
    print(f" Test Accuracy:      {metrics['accuracy_percentage']}%")
    print(f" Macro F1-Score:     {metrics['f1_macro']}")
    print(f" Model Artifact:     {model_path}")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run complete PlantGuard AI ML pipeline")
    parser.add_argument("--architecture", type=str, default="mobilenetv2", choices=["mobilenetv2", "custom_cnn"])
    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--batch-size", type=int, default=16)
    args = parser.parse_args()

    run_pipeline(architecture=args.architecture, epochs=args.epochs, batch_size=args.batch_size)
