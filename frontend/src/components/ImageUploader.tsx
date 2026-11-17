import { useState, useRef } from "react";
import { UploadCloud, Sparkles, RefreshCw, AlertCircle } from "lucide-react";
import { predictImage, predictFromUrl } from "../services/api";
import type { PredictionResult } from "../types";

interface ImageUploaderProps {
  onPredictionComplete: (result: PredictionResult, previewUrl: string) => void;
  isLoading: boolean;
  setIsLoading: (loading: boolean) => void;
  error: string | null;
  setError: (err: string | null) => void;
}

const SAMPLE_IMAGES = [
  { name: "Tomato Early Blight", file: "tomato_early_blight_sample.jpg", plant: "Tomato" },
  { name: "Tomato Healthy", file: "tomato_healthy_sample.jpg", plant: "Tomato" },
  { name: "Tomato Late Blight", file: "tomato_late_blight_sample.jpg", plant: "Tomato" },
  { name: "Potato Early Blight", file: "potato_early_blight_sample.jpg", plant: "Potato" },
  { name: "Potato Healthy", file: "potato_healthy_sample.jpg", plant: "Potato" },
  { name: "Pepper Bacterial Spot", file: "pepper_bacterial_spot_sample.jpg", plant: "Pepper" },
];

export const ImageUploader = ({
  onPredictionComplete,
  isLoading,
  setIsLoading,
  error,
  setError,
}: ImageUploaderProps) => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [isDragOver, setIsDragOver] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFile = (file: File) => {
    setError(null);
    if (!file.type.startsWith("image/")) {
      setError("Please select a valid image file (JPEG, PNG, WebP).");
      return;
    }
    if (file.size > 15 * 1024 * 1024) {
      setError("Image size exceeds the 15MB limit.");
      return;
    }

    setSelectedFile(file);
    const url = URL.createObjectURL(file);
    setPreviewUrl(url);
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragOver(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleAnalyze = async () => {
    if (!selectedFile) {
      setError("Please select or upload an image first.");
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const result = await predictImage(selectedFile);
      onPredictionComplete(result, previewUrl || "");
    } catch (err: any) {
      setError(err.message || "Failed to analyze leaf image. Ensure backend is running.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleSelectSample = async (sample: typeof SAMPLE_IMAGES[0]) => {
    setIsLoading(true);
    setError(null);
    const url = `/samples/${sample.file}`;
    setPreviewUrl(url);

    try {
      const result = await predictFromUrl(url, sample.file);
      onPredictionComplete(result, url);
    } catch (err: any) {
      setError(err.message || "Failed to analyze sample. Make sure demo samples are generated.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setSelectedFile(null);
    setPreviewUrl(null);
    setError(null);
    if (fileInputRef.current) fileInputRef.current.value = "";
  };

  return (
    <div className="space-y-6">
      {/* Upload Zone */}
      <div
        onDragOver={(e) => {
          e.preventDefault();
          setIsDragOver(true);
        }}
        onDragLeave={() => setIsDragOver(false)}
        onDrop={handleDrop}
        onClick={() => !previewUrl && fileInputRef.current?.click()}
        className={`relative border-2 border-dashed rounded-3xl p-8 text-center transition-all ${
          isDragOver
            ? "border-emerald-500 bg-emerald-50/50 scale-[1.01]"
            : previewUrl
            ? "border-emerald-300 bg-white"
            : "border-slate-300 hover:border-emerald-400 bg-white hover:bg-slate-50/50 cursor-pointer"
        }`}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept="image/jpeg,image/png,image/webp"
          className="hidden"
          onChange={(e) => e.target.files?.[0] && handleFile(e.target.files[0])}
        />

        {previewUrl ? (
          <div className="flex flex-col items-center space-y-4">
            <div className="relative w-64 h-64 rounded-2xl overflow-hidden shadow-lg border border-slate-200">
              <img
                src={previewUrl}
                alt="Selected plant leaf"
                className="w-full h-full object-cover"
              />
              {isLoading && (
                <div className="absolute inset-0 bg-black/40 backdrop-blur-xs flex flex-col items-center justify-center text-white">
                  <RefreshCw className="w-8 h-8 animate-spin text-emerald-400 mb-2" />
                  <span className="text-xs font-semibold">Running Neural Inference...</span>
                </div>
              )}
            </div>

            <div className="flex items-center space-x-3">
              <button
                type="button"
                onClick={handleReset}
                disabled={isLoading}
                className="px-4 py-2 text-xs font-semibold text-slate-600 bg-slate-100 hover:bg-slate-200 rounded-xl transition-all"
              >
                Choose Another Image
              </button>
              <button
                type="button"
                onClick={handleAnalyze}
                disabled={isLoading}
                className="px-6 py-2 text-xs font-semibold text-white bg-emerald-600 hover:bg-emerald-700 rounded-xl shadow-md shadow-emerald-200 flex items-center space-x-2 transition-all disabled:opacity-50"
              >
                {isLoading ? (
                  <>
                    <RefreshCw className="w-4 h-4 animate-spin" />
                    <span>Analyzing...</span>
                  </>
                ) : (
                  <>
                    <Sparkles className="w-4 h-4" />
                    <span>Analyze Disease</span>
                  </>
                )}
              </button>
            </div>
          </div>
        ) : (
          <div className="flex flex-col items-center justify-center space-y-3 py-6">
            <div className="w-16 h-16 rounded-2xl bg-emerald-50 text-emerald-600 flex items-center justify-center shadow-xs">
              <UploadCloud className="w-8 h-8" />
            </div>
            <div>
              <p className="text-sm font-semibold text-slate-800">
                Drag and drop a plant leaf image here, or{" "}
                <span className="text-emerald-600 underline">browse your files</span>
              </p>
              <p className="text-xs text-slate-400 mt-1">
                Supports JPEG, PNG, WebP up to 15MB. Ensure good lighting on the leaf blade.
              </p>
            </div>
          </div>
        )}
      </div>

      {/* Error Banner */}
      {error && (
        <div className="flex items-center space-x-2.5 p-3.5 bg-rose-50 border border-rose-200 text-rose-700 rounded-xl text-xs">
          <AlertCircle className="w-4 h-4 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Quick Test Drive Samples */}
      <div className="bg-emerald-50/60 border border-emerald-100 rounded-2xl p-4">
        <div className="flex items-center justify-between mb-3">
          <span className="text-xs font-bold text-emerald-900 uppercase tracking-wider flex items-center space-x-1.5">
            <Sparkles className="w-3.5 h-3.5 text-emerald-600" />
            <span>Instant Demo Samples (1-Click Test Drive)</span>
          </span>
          <span className="text-[11px] text-emerald-700">Click any card to analyze</span>
        </div>
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-2">
          {SAMPLE_IMAGES.map((sample, idx) => (
            <button
              key={idx}
              type="button"
              disabled={isLoading}
              onClick={() => handleSelectSample(sample)}
              className="p-2.5 bg-white border border-emerald-200/80 rounded-xl hover:border-emerald-500 hover:shadow-xs text-left transition-all group disabled:opacity-50"
            >
              <div className="text-[10px] font-semibold text-emerald-600 uppercase tracking-wider">
                {sample.plant}
              </div>
              <div className="text-xs font-medium text-slate-800 group-hover:text-emerald-700 line-clamp-1">
                {sample.name.replace(sample.plant, "").trim()}
              </div>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};
