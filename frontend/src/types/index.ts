export interface SeverityDetails {
  level: "None" | "Low" | "Medium" | "High";
  affected_percentage: number;
  method: string;
  is_experimental: boolean;
  notes: string;
}

export interface CareDetails {
  immediate_action: string;
  organic_treatment: string;
  chemical_treatment: string;
  cultural_practices: string;
  prevention: string;
}

export interface TopPredictionItem {
  class_name: string;
  plant: string;
  disease: string;
  status: "Healthy" | "Diseased";
  confidence: number;
  confidence_percentage: number;
}

export interface PredictionResult {
  id?: number;
  filename?: string;
  image_url?: string;
  class_name: string;
  plant: string;
  disease: string;
  status: "Healthy" | "Diseased";
  confidence: number;
  confidence_percentage: number;
  severity: "None" | "Low" | "Medium" | "High";
  severity_details: SeverityDetails;
  scientific_name: string;
  description: string;
  symptoms: string;
  diagnostic_cues?: string;
  recommendations: string[];
  care_details: CareDetails;
  top_predictions: TopPredictionItem[];
  explanation: string;
  disclaimer: string;
}

export interface DiseaseInfo {
  class_name: string;
  plant: string;
  disease: string;
  status: "Healthy" | "Diseased";
  scientific_name: string;
  description: string;
  symptoms: string;
  severity_guidelines: string;
  diagnostic_cues: string;
  care: CareDetails;
}

export interface HistoryItem {
  id: number;
  filename: string;
  image_url?: string;
  plant: string;
  disease: string;
  status: "Healthy" | "Diseased";
  confidence: number;
  severity: "None" | "Low" | "Medium" | "High";
  severity_percentage?: number;
  scientific_name?: string;
  explanation?: string;
  user_feedback?: string;
  created_at?: string;
}

export interface PerClassMetric {
  plant: string;
  disease: string;
  precision: number;
  recall: number;
  f1_score: number;
  support: number;
}

export interface ModelMetrics {
  model_name: string;
  total_test_samples: number;
  classes_count: number;
  accuracy: number;
  accuracy_percentage: number;
  precision_macro: number;
  recall_macro: number;
  f1_macro: number;
  precision_weighted: number;
  recall_weighted: number;
  f1_weighted: number;
  confusion_matrix: number[][];
  class_labels: string[];
  per_class_metrics: Record<string, PerClassMetric>;
  limitations: string;
  has_curves: boolean;
  has_confusion_matrix_img: boolean;
}

export interface HealthInfo {
  status: string;
  model_loaded: boolean;
  active_model: string;
  classes_count: number;
  version: string;
  framework: string;
}
