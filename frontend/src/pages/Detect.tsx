import { useState } from "react";
import { ImageUploader } from "../components/ImageUploader";
import { PredictionCard } from "../components/PredictionCard";
import type { PredictionResult } from "../types";
import { ArrowLeft } from "lucide-react";

export const Detect = () => {
  const [prediction, setPrediction] = useState<PredictionResult | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string>("");
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handlePredictionComplete = (result: PredictionResult, url: string) => {
    setPrediction(result);
    setPreviewUrl(url);
  };

  const handleReset = () => {
    setPrediction(null);
    setPreviewUrl("");
    setError(null);
  };

  return (
    <div className="max-w-4xl mx-auto py-6 sm:py-10 space-y-8">
      {/* Header */}
      <div className="text-center space-y-2">
        <h1 className="text-3xl font-extrabold text-slate-900">
          Plant Disease Diagnosis
        </h1>
        <p className="text-xs sm:text-sm text-slate-600 max-w-xl mx-auto">
          Upload a high-resolution photograph of an individual plant leaf showing upper or lower surface symptoms.
        </p>
      </div>

      {/* Main Content Area */}
      {!prediction ? (
        <div className="bg-white rounded-3xl border border-slate-200 p-6 sm:p-8 shadow-xs">
          <ImageUploader
            onPredictionComplete={handlePredictionComplete}
            isLoading={isLoading}
            setIsLoading={setIsLoading}
            error={error}
            setError={setError}
          />
        </div>
      ) : (
        <div className="space-y-6">
          <button
            onClick={handleReset}
            className="flex items-center space-x-2 text-xs font-semibold text-slate-600 hover:text-emerald-700 bg-white border border-slate-200 px-4 py-2 rounded-xl transition-all shadow-xs"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>Scan Another Leaf</span>
          </button>

          <PredictionCard result={prediction} previewUrl={previewUrl} />
        </div>
      )}
    </div>
  );
};
