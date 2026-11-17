import { useState } from "react";
import { FileText, Printer, ThumbsUp, ThumbsDown, HelpCircle } from "lucide-react";
import type { PredictionResult } from "../types";
import { SeverityBadge } from "./SeverityBadge";
import { CareSection } from "./CareSection";
import { submitFeedback } from "../services/api";

interface PredictionCardProps {
  result: PredictionResult;
  previewUrl: string;
}

export const PredictionCard = ({ result, previewUrl }: PredictionCardProps) => {
  const [feedbackSent, setFeedbackSent] = useState<string | null>(null);
  const isHealthy = result.status.toLowerCase() === "healthy";

  const handleFeedback = async (type: string) => {
    if (result.id) {
      try {
        await submitFeedback(result.id, type);
        setFeedbackSent(type);
      } catch {
        // graceful handle
      }
    } else {
      setFeedbackSent(type);
    }
  };

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="space-y-6 animate-in fade-in duration-300">
      {/* Primary Diagnosis Header Card */}
      <div className="bg-white rounded-3xl border border-slate-200 p-6 md:p-8 shadow-sm">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
          {/* Leaf Image Preview */}
          <div className="lg:col-span-4 flex flex-col items-center">
            <div className="w-56 h-56 sm:w-64 sm:h-64 rounded-2xl overflow-hidden border border-slate-200 shadow-md">
              <img
                src={previewUrl || result.image_url || ""}
                alt={`${result.plant} leaf`}
                className="w-full h-full object-cover"
              />
            </div>
            <div className="mt-3 text-center">
              <span className="text-[11px] text-slate-400 font-mono">
                {result.scientific_name !== "N/A" ? result.scientific_name : result.class_name}
              </span>
            </div>
          </div>

          {/* Diagnostic Core Information */}
          <div className="lg:col-span-8 space-y-4">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <div className="flex items-center space-x-2">
                <span className="text-xs uppercase tracking-wider font-bold px-3 py-1 rounded-full bg-slate-100 text-slate-700">
                  {result.plant}
                </span>
                <span
                  className={`text-xs uppercase tracking-wider font-bold px-3 py-1 rounded-full ${
                    isHealthy
                      ? "bg-emerald-100 text-emerald-800"
                      : "bg-rose-100 text-rose-800"
                  }`}
                >
                  {result.status}
                </span>
              </div>
              <SeverityBadge severity={result.severity} details={result.severity_details} />
            </div>

            <div>
              <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900">
                {result.plant} – {result.disease}
              </h2>
              {result.scientific_name !== "N/A" && (
                <p className="text-sm italic text-slate-500 font-serif">
                  Pathogen: {result.scientific_name}
                </p>
              )}
            </div>

            {/* Confidence Bar */}
            <div className="bg-slate-50 p-4 rounded-2xl border border-slate-100 space-y-2">
              <div className="flex items-center justify-between text-xs font-semibold text-slate-700">
                <span>Model Confidence</span>
                <span className="text-emerald-700 font-bold">{result.confidence_percentage}%</span>
              </div>
              <div className="w-full h-3 bg-slate-200 rounded-full overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-emerald-500 to-teal-600 rounded-full transition-all duration-500"
                  style={{ width: `${Math.min(100, Math.max(5, result.confidence_percentage))}%` }}
                />
              </div>

              {/* Top-3 Candidates */}
              {result.top_predictions && result.top_predictions.length > 1 && (
                <div className="pt-2 text-[11px] text-slate-500 flex flex-wrap gap-x-4 gap-y-1">
                  <span className="font-semibold text-slate-700">Top Candidates:</span>
                  {result.top_predictions.map((cand, idx) => (
                    <span key={idx} className="inline-flex items-center space-x-1">
                      <span>{cand.plant} {cand.disease}:</span>
                      <span className="font-semibold text-slate-700">{cand.confidence_percentage}%</span>
                    </span>
                  ))}
                </div>
              )}
            </div>

            {/* Explanation */}
            <div className="p-4 bg-emerald-50/50 border border-emerald-100 rounded-2xl text-xs sm:text-sm text-slate-700 leading-relaxed">
              <p className="font-semibold text-emerald-900 mb-1 flex items-center space-x-1.5">
                <FileText className="w-4 h-4 text-emerald-600" />
                <span>Diagnostic Explanation</span>
              </p>
              <p>{result.explanation}</p>
            </div>

            {/* Actions & Feedback */}
            <div className="flex flex-wrap items-center justify-between gap-3 pt-2">
              <button
                onClick={handlePrint}
                className="flex items-center space-x-2 px-3 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl text-xs font-semibold transition-all"
              >
                <Printer className="w-4 h-4" />
                <span>Export / Print Report</span>
              </button>

              <div className="flex items-center space-x-2 text-xs text-slate-500">
                <span>Helpful assessment?</span>
                <button
                  onClick={() => handleFeedback("helpful")}
                  className={`p-1.5 rounded-lg border ${
                    feedbackSent === "helpful"
                      ? "bg-emerald-100 text-emerald-700 border-emerald-300"
                      : "bg-white hover:bg-slate-50 text-slate-600 border-slate-200"
                  }`}
                  title="Accurate and helpful"
                >
                  <ThumbsUp className="w-3.5 h-3.5" />
                </button>
                <button
                  onClick={() => handleFeedback("incorrect")}
                  className={`p-1.5 rounded-lg border ${
                    feedbackSent === "incorrect"
                      ? "bg-rose-100 text-rose-700 border-rose-300"
                      : "bg-white hover:bg-slate-50 text-slate-600 border-slate-200"
                  }`}
                  title="Inaccurate"
                >
                  <ThumbsDown className="w-3.5 h-3.5" />
                </button>
                {feedbackSent && (
                  <span className="text-emerald-600 font-medium text-[11px]">
                    Feedback noted!
                  </span>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Disease Pathology Details */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs space-y-2">
          <h3 className="text-sm font-bold text-slate-900">Symptoms & Clinical Manifestation</h3>
          <p className="text-xs text-slate-600 leading-relaxed">{result.symptoms}</p>
        </div>
        <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs space-y-2">
          <h3 className="text-sm font-bold text-slate-900">Diagnostic Visual Cues</h3>
          <p className="text-xs text-slate-600 leading-relaxed">
            {result.diagnostic_cues || "Observe circular margins, chlorotic yellow halos, and texture variation."}
          </p>
        </div>
      </div>

      {/* Structured Agronomic Care Protocol */}
      <CareSection care={result.care_details} isHealthy={isHealthy} />

      {/* Academic Disclaimer Box */}
      <div className="p-4 bg-amber-50/70 border border-amber-200 rounded-2xl text-xs text-amber-800 leading-relaxed">
        <div className="font-semibold mb-0.5 flex items-center space-x-1.5">
          <HelpCircle className="w-4 h-4 text-amber-600 shrink-0" />
          <span>Educational Decision-Support Notice</span>
        </div>
        <p className="text-[11px] text-amber-700">{result.disclaimer}</p>
      </div>
    </div>
  );
};
