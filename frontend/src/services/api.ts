import type {
  PredictionResult,
  DiseaseInfo,
  HistoryItem,
  ModelMetrics,
  HealthInfo,
} from "../types";

const API_BASE = "";

export async function predictImage(file: File): Promise<PredictionResult> {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_BASE}/api/predict`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    let errMessage = "Inference failed";
    try {
      const err = await response.json();
      errMessage = err.detail || err.message || errMessage;
    } catch {
      // ignore
    }
    throw new Error(errMessage);
  }

  return response.json();
}

export async function predictFromUrl(url: string, filename: string): Promise<PredictionResult> {
  const imageBlob = await fetch(url).then((res) => {
    if (!res.ok) throw new Error("Failed to load sample image");
    return res.blob();
  });
  const file = new File([imageBlob], filename, { type: imageBlob.type || "image/jpeg" });
  return predictImage(file);
}

export async function getHealth(): Promise<HealthInfo> {
  const res = await fetch(`${API_BASE}/api/health`);
  if (!res.ok) throw new Error("Health check failed");
  return res.json();
}

export async function getDiseases(): Promise<DiseaseInfo[]> {
  const res = await fetch(`${API_BASE}/api/diseases`);
  if (!res.ok) throw new Error("Failed to load diseases library");
  return res.json();
}

export async function getHistory(
  limit: number = 50,
  plant?: string,
  status?: string
): Promise<HistoryItem[]> {
  const params = new URLSearchParams();
  params.append("limit", limit.toString());
  if (plant) params.append("plant", plant);
  if (status) params.append("status", status);

  const res = await fetch(`${API_BASE}/api/history?${params.toString()}`);
  if (!res.ok) throw new Error("Failed to load diagnosis history");
  return res.json();
}

export async function deleteHistory(id: number): Promise<{ message: string }> {
  const res = await fetch(`${API_BASE}/api/history/${id}`, {
    method: "DELETE",
  });
  if (!res.ok) throw new Error("Failed to delete record");
  return res.json();
}

export async function submitFeedback(id: number, feedback: string): Promise<{ message: string }> {
  const res = await fetch(`${API_BASE}/api/history/${id}/feedback`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ feedback }),
  });
  if (!res.ok) throw new Error("Failed to submit feedback");
  return res.json();
}

export async function getModelMetrics(): Promise<ModelMetrics> {
  const res = await fetch(`${API_BASE}/api/model-info`);
  if (!res.ok) throw new Error("Failed to fetch model metrics");
  return res.json();
}
