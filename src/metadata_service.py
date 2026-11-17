"""Domain metadata service for PlantGuard AI.

Provides structured lookups for plant disease descriptions, symptoms,
biological pathogens, care recommendations, and prevention guidelines.
"""

from typing import Dict, Any, List, Optional
import pandas as pd
from pathlib import Path

from src.config import (
    DISEASE_INFO_FILE,
    CARE_RECOMMENDATIONS_FILE,
    CLASS_DISPLAY_INFO,
    CLASS_NAMES,
)


class MetadataService:
    """Service to load, cache, and query agricultural disease information and care protocols."""

    def __init__(
        self,
        disease_info_path: Path = DISEASE_INFO_FILE,
        care_path: Path = CARE_RECOMMENDATIONS_FILE,
    ) -> None:
        self.disease_info_path = Path(disease_info_path)
        self.care_path = Path(care_path)
        self._disease_df: Optional[pd.DataFrame] = None
        self._care_df: Optional[pd.DataFrame] = None
        self._load_data()

    def _load_data(self) -> None:
        """Load and cache CSV metadata."""
        if self.disease_info_path.exists():
            self._disease_df = pd.read_csv(self.disease_info_path)
            self._disease_df.set_index("class_name", inplace=True)
        else:
            self._disease_df = pd.DataFrame()

        if self.care_path.exists():
            self._care_df = pd.read_csv(self.care_path)
            self._care_df.set_index("class_name", inplace=True)
        else:
            self._care_df = pd.DataFrame()

    def get_disease_info(self, class_name: str) -> Dict[str, Any]:
        """Fetch descriptive details and symptoms for a given disease class."""
        display = CLASS_DISPLAY_INFO.get(
            class_name,
            {"plant": "Unknown", "disease": class_name, "status": "Unknown"}
        )

        if self._disease_df is not None and class_name in self._disease_df.index:
            row = self._disease_df.loc[class_name]
            return {
                "plant": str(row.get("plant", display["plant"])),
                "disease": str(row.get("disease", display["disease"])),
                "scientific_name": str(row.get("scientific_name", "N/A")),
                "description": str(row.get("description", "No description available.")),
                "symptoms": str(row.get("symptoms", "No symptoms listed.")),
                "severity_guidelines": str(row.get("severity_guidelines", "Standard guidelines.")),
                "diagnostic_cues": str(row.get("diagnostic_cues", "Visual cues unavailable.")),
                "status": display.get("status", "Unknown"),
            }

        return {
            "plant": display["plant"],
            "disease": display["disease"],
            "scientific_name": "N/A",
            "description": "Standard disease profile not found in local catalog.",
            "symptoms": "Please inspect foliage for chlorosis, necrosis, or spotting.",
            "severity_guidelines": "Observe spread across canopy.",
            "diagnostic_cues": "Examine leaf margins and venation.",
            "status": display.get("status", "Unknown"),
        }

    def get_care_recommendations(self, class_name: str) -> Dict[str, Any]:
        """Fetch actionable agricultural care advice and treatments for a given class."""
        display = CLASS_DISPLAY_INFO.get(
            class_name,
            {"plant": "Plant", "disease": class_name, "status": "Unknown"}
        )

        if self._care_df is not None and class_name in self._care_df.index:
            row = self._care_df.loc[class_name]
            return {
                "plant": str(row.get("plant", display["plant"])),
                "disease": str(row.get("disease", display["disease"])),
                "immediate_action": str(row.get("immediate_action", "Isolate suspect plant to prevent potential spread.")),
                "organic_treatment": str(row.get("organic_treatment", "Apply neem oil or certified bio-fungicide.")),
                "chemical_treatment": str(row.get("chemical_treatment", "Consult local agricultural extension service.")),
                "cultural_practices": str(row.get("cultural_practices", "Ensure adequate plant spacing and bottom watering.")),
                "prevention": str(row.get("prevention", "Maintain strict garden hygiene and sanitize tools.")),
            }

        return {
            "plant": display["plant"],
            "disease": display["disease"],
            "immediate_action": "Monitor plant health and quarantine if symptoms spread.",
            "organic_treatment": "Apply gentle horticultural soap or neem oil spray if needed.",
            "chemical_treatment": "Consult local extension specialist before chemical application.",
            "cultural_practices": "Ensure clean water, adequate sunlight, and proper soil aeration.",
            "prevention": "Inspect leaves regularly and disinfect pruning tools.",
        }

    def get_all_diseases(self) -> List[Dict[str, Any]]:
        """Return combined catalog of all registered diseases and plants."""
        catalog = []
        for class_name in CLASS_NAMES:
            info = self.get_disease_info(class_name)
            care = self.get_care_recommendations(class_name)
            catalog.append({
                "class_name": class_name,
                **info,
                "care": care,
            })
        return catalog


# Global singleton instance
metadata_service = MetadataService()
