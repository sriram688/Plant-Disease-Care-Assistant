import { useState, useEffect } from "react";
import {
  BarChart3,
  TrendingUp,
  Target,
  RefreshCw,
  AlertCircle,
  Layers,
  Image as ImageIcon,
  CheckCircle2,
  AlertTriangle,
} from "lucide-react";
import { getModelMetrics } from "../services/api";
import type { ModelMetrics } from "../types";

export const ModelDashboard = () => {
  const [metrics, setMetrics] = useState<ModelMetrics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchMetrics = () => {
    setLoading(true);
    getModelMetrics()
      .then((data) => {
        setMetrics(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message || "Failed to load model metrics");
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchMetrics();
  }, []);

  return (
    <div className="py-6 sm:py-10 space-y-8 max-w-6xl mx-auto">
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-3xl font-extrabold text-slate-900">Model Evaluation Dashboard</h1>
          <p className="text-xs sm:text-sm text-slate-600">
            Transparent, uncompromised test set metrics for the active classification backbone.
          </p>
        </div>
        <button
          onClick={fetchMetrics}
          disabled={loading}
          className="flex items-center space-x-1.5 px-3 py-2 bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 text-xs font-semibold rounded-xl shadow-xs transition-all"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? "animate-spin" : ""}`} />
          <span>Refresh Metrics</span>
        </button>
      </div>

      {loading ? (
        <div className="flex flex-col items-center justify-center py-20 text-slate-500">
          <RefreshCw className="w-8 h-8 animate-spin text-emerald-600 mb-2" />
          <span className="text-xs font-semibold">Compiling Model Diagnostics...</span>
        </div>
      ) : error ? (
        <div className="p-4 bg-rose-50 border border-rose-200 text-rose-700 rounded-2xl text-xs flex items-center space-x-2">
          <AlertCircle className="w-4 h-4" />
          <span>{error}</span>
        </div>
      ) : !metrics ? null : (
        <div className="space-y-8">
          {/* Key Metrics Cards */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs">
              <div className="flex items-center justify-between text-xs text-slate-500 font-semibold mb-2">
                <span>Holdout Test Accuracy</span>
                <Target className="w-4 h-4 text-emerald-600" />
              </div>
              <div className="text-2xl sm:text-3xl font-extrabold text-slate-900">
                {metrics.accuracy_percentage}%
              </div>
              <p className="text-[11px] text-slate-400 mt-1">
                Across {metrics.total_test_samples} unseen test samples
              </p>
            </div>

            <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs">
              <div className="flex items-center justify-between text-xs text-slate-500 font-semibold mb-2">
                <span>Macro Precision</span>
                <TrendingUp className="w-4 h-4 text-teal-600" />
              </div>
              <div className="text-2xl sm:text-3xl font-extrabold text-slate-900">
                {(metrics.precision_macro * 100).toFixed(1)}%
              </div>
              <p className="text-[11px] text-slate-400 mt-1">
                Weighted: {(metrics.precision_weighted * 100).toFixed(1)}%
              </p>
            </div>

            <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs">
              <div className="flex items-center justify-between text-xs text-slate-500 font-semibold mb-2">
                <span>Macro Recall</span>
                <CheckCircle2 className="w-4 h-4 text-sky-600" />
              </div>
              <div className="text-2xl sm:text-3xl font-extrabold text-slate-900">
                {(metrics.recall_macro * 100).toFixed(1)}%
              </div>
              <p className="text-[11px] text-slate-400 mt-1">
                Weighted: {(metrics.recall_weighted * 100).toFixed(1)}%
              </p>
            </div>

            <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs">
              <div className="flex items-center justify-between text-xs text-slate-500 font-semibold mb-2">
                <span>Macro F1-Score</span>
                <Layers className="w-4 h-4 text-indigo-600" />
              </div>
              <div className="text-2xl sm:text-3xl font-extrabold text-slate-900">
                {(metrics.f1_macro * 100).toFixed(1)}%
              </div>
              <p className="text-[11px] text-slate-400 mt-1">
                Weighted: {(metrics.f1_weighted * 100).toFixed(1)}%
              </p>
            </div>
          </div>

          {/* Model Architecture & Holdout Plots */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Confusion Matrix Visual */}
            <div className="bg-white rounded-3xl border border-slate-200 p-6 shadow-xs space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="font-bold text-slate-900 text-sm flex items-center space-x-2">
                  <ImageIcon className="w-4 h-4 text-emerald-600" />
                  <span>Confusion Matrix Heatmap</span>
                </h3>
                <span className="text-[11px] text-slate-400 font-mono">Independent Holdout</span>
              </div>
              <div className="w-full bg-slate-50 rounded-2xl border border-slate-100 overflow-hidden min-h-[260px] flex items-center justify-center p-2">
                <img
                  src="/api/model-info/confusion-matrix"
                  alt="Confusion Matrix Heatmap"
                  className="w-full h-auto object-contain rounded-xl"
                  onError={(e) => {
                    (e.target as HTMLElement).style.display = "none";
                  }}
                />
              </div>
              <p className="text-[11px] text-slate-500 leading-relaxed">
                Evaluates true vs predicted classes. Darker diagonal cells represent accurate classifications.
              </p>
            </div>

            {/* Training & Validation Curves */}
            <div className="bg-white rounded-3xl border border-slate-200 p-6 shadow-xs space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="font-bold text-slate-900 text-sm flex items-center space-x-2">
                  <BarChart3 className="w-4 h-4 text-sky-600" />
                  <span>Loss & Accuracy Learning Curves</span>
                </h3>
                <span className="text-[11px] text-slate-400 font-mono">Training vs Validation</span>
              </div>
              <div className="w-full bg-slate-50 rounded-2xl border border-slate-100 overflow-hidden min-h-[260px] flex items-center justify-center p-2">
                <img
                  src="/api/model-info/training-curves"
                  alt="Training and Validation Loss and Accuracy Curves"
                  className="w-full h-auto object-contain rounded-xl"
                  onError={(e) => {
                    (e.target as HTMLElement).style.display = "none";
                  }}
                />
              </div>
              <p className="text-[11px] text-slate-500 leading-relaxed">
                Monitors generalization gap and confirms absence of severe overfitting across epochs.
              </p>
            </div>
          </div>

          {/* Per-Class Breakdown Table */}
          {metrics.per_class_metrics && Object.keys(metrics.per_class_metrics).length > 0 && (
            <div className="bg-white rounded-3xl border border-slate-200 shadow-xs overflow-hidden">
              <div className="p-6 border-b border-slate-100">
                <h3 className="font-bold text-slate-900 text-sm">
                  Class-by-Class Granular Performance Breakdown
                </h3>
                <p className="text-xs text-slate-500 mt-1">
                  Individual precision, recall, and support across all {metrics.classes_count} target classes.
                </p>
              </div>

              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs text-slate-600">
                  <thead className="bg-slate-50 text-slate-700 font-semibold border-b border-slate-200 uppercase tracking-wider text-[10px]">
                    <tr>
                      <th className="py-3 px-4">Plant</th>
                      <th className="py-3 px-4">Disease / Condition</th>
                      <th className="py-3 px-4">Precision</th>
                      <th className="py-3 px-4">Recall</th>
                      <th className="py-3 px-4">F1-Score</th>
                      <th className="py-3 px-4 text-right">Test Support</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {Object.entries(metrics.per_class_metrics).map(([key, val]) => (
                      <tr key={key} className="hover:bg-slate-50/50">
                        <td className="py-3 px-4 font-semibold text-slate-800">{val.plant}</td>
                        <td className="py-3 px-4">{val.disease}</td>
                        <td className="py-3 px-4 font-mono">{(val.precision * 100).toFixed(1)}%</td>
                        <td className="py-3 px-4 font-mono">{(val.recall * 100).toFixed(1)}%</td>
                        <td className="py-3 px-4 font-mono font-semibold text-slate-800">
                          {(val.f1_score * 100).toFixed(1)}%
                        </td>
                        <td className="py-3 px-4 text-right font-mono text-slate-500">
                          {val.support} samples
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* Transparent Limitations & Discussion */}
          <div className="bg-slate-50 rounded-3xl border border-slate-200 p-6 space-y-3">
            <h4 className="font-bold text-slate-900 text-xs uppercase tracking-wider flex items-center space-x-2">
              <AlertTriangle className="w-4 h-4 text-amber-600" />
              <span>Model Limitations & Real-World Constraints</span>
            </h4>
            <p className="text-xs text-slate-600 leading-relaxed">
              {metrics.limitations}
            </p>
            <ul className="text-xs text-slate-600 list-disc list-inside space-y-1">
              <li>Images with multiple coinfections may have ambiguous single-class predictions.</li>
              <li>Background clutter, wet leaves, or extreme shadow angles may lower confidence.</li>
              <li>Severity staging is an automated surface-lesion ratio heuristic rather than pathological histology.</li>
            </ul>
          </div>
        </div>
      )}
    </div>
  );
};
