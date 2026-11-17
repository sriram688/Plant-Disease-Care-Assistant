"""Prediction engine for PlantGuard AI.

Executes end-to-end inference on leaf images, calculating:
- Softmax disease probability distributions
- Top-k class candidates
- Disease severity assessment
- Agricultural care & prevention protocols
- Plain-language farmer-friendly explanations
"""

import argparse
from pathlib import Path
from typing import Union, Dict, Any, List, Optional
import numpy as np

from src.config import (
    CLASS_NAMES,
    CLASS_DISPLAY_INFO,
    MOBILENET_MODEL_PATH,
    CNN_MODEL_PATH,
    IMAGE_SIZE,
)
from src.preprocessing import load_and_preprocess_image
from src.severity import estimate_disease_severity, SeverityResult
from src.metadata_service import metadata_service


class PredictionEngine:
    """Singleton-ready inference pipeline for plant disease diagnosis."""

    def __init__(self, model_path: Optional[Path] = None) -> None:
        self.model_path = model_path
        self._model: Optional[Any] = None

    def _get_active_model_path(self) -> Path:
        """Locate available model checkpoint (prefers MobileNetV2, falls back to Custom CNN)."""
        if self.model_path and Path(self.model_path).exists():
            return Path(self.model_path)
        if MOBILENET_MODEL_PATH.exists():
            return MOBILENET_MODEL_PATH
        if CNN_MODEL_PATH.exists():
            return CNN_MODEL_PATH
        raise FileNotFoundError(
            f"No trained model found. Looked for {MOBILENET_MODEL_PATH} or {CNN_MODEL_PATH}. "
            "Please run 'python -m src.train' or 'python scripts/run_all.py' to generate a model."
        )

    def load_model(self) -> Any:
        """Load or retrieve cached Keras model."""
        if self._model is None:
            import tensorflow as tf
            active_path = self._get_active_model_path()
            self._model = tf.keras.models.load_model(active_path)
        return self._model

    def is_model_loaded(self) -> bool:
        """Check if model is currently initialized in memory."""
        return self._model is not None

    def generate_explanation(self, plant: str, disease: str, confidence: float, severity: str) -> str:
        """Compose clear, plain-language diagnostic explanation."""
        if disease.lower() == "healthy":
            return (
                f"The {plant} leaf shows uniform green chlorophyll coloration, smooth cellular lamina, "
                f"and intact venation with {confidence*100:.1f}% confidence. No active necrotic lesions or pathogen "
                "staining were observed."
            )

        return (
            f"The image exhibits symptoms consistent with {plant} {disease} (confidence: {confidence*100:.1f}%). "
            f"The estimated symptom severity is {severity}. Typical manifestations include distinctive discoloration, "
            "spotting, and tissue damage on the leaf surface."
        )

    def predict(
        self,
        image_source: Union[str, Path, bytes],
        top_k: int = 3,
    ) -> Dict[str, Any]:
        """Perform full prediction, severity estimation, and recommendation enrichment.

        Args:
            image_source: Path to image or raw image bytes.
            top_k: Number of highest-probability candidate classes to return.

        Returns:
            Dict containing detailed prediction results.
        """
        model = self.load_model()

        # Preprocess normalized for model input
        norm_img = load_and_preprocess_image(image_source, target_size=IMAGE_SIZE, normalize=True)
        # Preprocess uint8 for OpenCV severity analysis
        uint8_img = load_and_preprocess_image(image_source, target_size=IMAGE_SIZE, normalize=False)

        # Model forward pass
        input_tensor = np.expand_dims(norm_img, axis=0)
        predictions = model.predict(input_tensor, verbose=0)[0]

        # Top prediction
        predicted_idx = int(np.argmax(predictions))
        predicted_class = CLASS_NAMES[predicted_idx]
        confidence = float(predictions[predicted_idx])

        # Top-k ranking
        top_indices = np.argsort(predictions)[::-1][:top_k]
        top_predictions = []
        for idx in top_indices:
            cls_name = CLASS_NAMES[idx]
            disp = CLASS_DISPLAY_INFO.get(cls_name, {"plant": "Unknown", "disease": cls_name, "status": "Unknown"})
            top_predictions.append({
                "class_name": cls_name,
                "plant": disp["plant"],
                "disease": disp["disease"],
                "status": disp["status"],
                "confidence": round(float(predictions[idx]), 4),
                "confidence_percentage": round(float(predictions[idx]) * 100, 2),
            })

        # Severity estimation
        severity_result: SeverityResult = estimate_disease_severity(
            image_rgb_uint8=uint8_img,
            predicted_class=predicted_class,
            confidence=confidence,
        )

        # Domain metadata & care instructions
        disease_info = metadata_service.get_disease_info(predicted_class)
        care_info = metadata_service.get_care_recommendations(predicted_class)

        # Format recommendations list
        recommendations = [
            f"Immediate Action: {care_info['immediate_action']}",
            f"Organic Treatment: {care_info['organic_treatment']}",
            f"Cultural Practices: {care_info['cultural_practices']}",
            f"Prevention: {care_info['prevention']}",
        ]
        if care_info.get("chemical_treatment") and care_info["chemical_treatment"] != "N/A":
            recommendations.append(f"Chemical Option: {care_info['chemical_treatment']}")

        explanation = self.generate_explanation(
            plant=disease_info["plant"],
            disease=disease_info["disease"],
            confidence=confidence,
            severity=severity_result.level,
        )

        return {
            "class_name": predicted_class,
            "plant": disease_info["plant"],
            "disease": disease_info["disease"],
            "status": disease_info["status"],
            "confidence": round(confidence, 4),
            "confidence_percentage": round(confidence * 100, 2),
            "severity": severity_result.level,
            "severity_details": {
                "level": severity_result.level,
                "affected_percentage": severity_result.score_percentage,
                "method": severity_result.method,
                "is_experimental": severity_result.is_experimental,
                "notes": severity_result.notes,
            },
            "scientific_name": disease_info["scientific_name"],
            "description": disease_info["description"],
            "symptoms": disease_info["symptoms"],
            "diagnostic_cues": disease_info.get("diagnostic_cues", ""),
            "recommendations": recommendations,
            "care_details": {
                "immediate_action": care_info["immediate_action"],
                "organic_treatment": care_info["organic_treatment"],
                "chemical_treatment": care_info["chemical_treatment"],
                "cultural_practices": care_info["cultural_practices"],
                "prevention": care_info["prevention"],
            },
            "top_predictions": top_predictions,
            "explanation": explanation,
            "disclaimer": (
                "Educational Disclaimer: PlantGuard AI is an academic and open-source project. "
                "Its inferences are educational decision-support estimates and must not be used as a guaranteed "
                "substitute for professional agricultural consultation or lab pathology tests."
            ),
        }


# Global engine instance
prediction_engine = PredictionEngine()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PlantGuard AI - Single image inference")
    parser.add_argument("--image", type=str, required=True, help="Path to leaf image")
    parser.add_argument("--model", type=str, default=None, help="Optional model path")
    args = parser.parse_args()

    engine = PredictionEngine(model_path=Path(args.model) if args.model else None)
    result = engine.predict(args.image)
    print("\n--- PlantGuard AI Prediction ---")
    print(f"Plant:      {result['plant']}")
    print(f"Disease:    {result['disease']} ({result['status']})")
    print(f"Confidence: {result['confidence_percentage']}%")
    print(f"Severity:   {result['severity']}")
    print(f"Explanation:\n  {result['explanation']}\n")
    print("Recommendations:")
    for rec in result["recommendations"]:
        print(f"  - {rec}")
