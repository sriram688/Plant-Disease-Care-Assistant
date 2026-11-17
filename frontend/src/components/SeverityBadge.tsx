import { useState } from "react";
import { Info, AlertTriangle, ShieldCheck } from "lucide-react";
import type { SeverityDetails } from "../types";

interface SeverityBadgeProps {
  severity: "None" | "Low" | "Medium" | "High";
  details?: SeverityDetails;
}

export const SeverityBadge = ({ severity, details }: SeverityBadgeProps) => {
  const [showTooltip, setShowTooltip] = useState(false);

  const getSeverityConfig = () => {
    switch (severity) {
      case "None":
        return {
          bg: "bg-emerald-50 border-emerald-200 text-emerald-800",
          dot: "bg-emerald-500",
          icon: ShieldCheck,
          label: "None (Healthy)",
          desc: "No disease lesions detected on the foliage surface.",
        };
      case "Low":
        return {
          bg: "bg-yellow-50 border-yellow-200 text-yellow-800",
          dot: "bg-yellow-500",
          icon: AlertTriangle,
          label: "Low Severity",
          desc: "Early stage: <15% of leaf surface exhibits symptoms. Highly manageable.",
        };
      case "Medium":
        return {
          bg: "bg-orange-50 border-orange-200 text-orange-800",
          dot: "bg-orange-500",
          icon: AlertTriangle,
          label: "Medium Severity",
          desc: "Moderate progression: 15% - 35% foliage damage. Prompt intervention advised.",
        };
      case "High":
        return {
          bg: "bg-rose-50 border-rose-200 text-rose-800",
          dot: "bg-rose-500",
          icon: AlertTriangle,
          label: "High Severity",
          desc: "Severe blighting: >35% tissue necrosis. Immediate isolation or pruning required.",
        };
      default:
        return {
          bg: "bg-slate-50 border-slate-200 text-slate-700",
          dot: "bg-slate-400",
          icon: Info,
          label: "Not Staged",
          desc: "Severity not evaluated.",
        };
    }
  };

  const config = getSeverityConfig();

  return (
    <div className="relative inline-block">
      <div
        className={`flex items-center space-x-2 px-3 py-1.5 rounded-full border text-xs font-semibold ${config.bg} cursor-pointer transition-all hover:shadow-xs`}
        onClick={() => setShowTooltip(!showTooltip)}
      >
        <span className={`w-2 h-2 rounded-full ${config.dot}`} />
        <span>{config.label}</span>
        {details?.affected_percentage !== undefined && severity !== "None" && (
          <span className="opacity-75 font-normal">({details.affected_percentage}% lesion area)</span>
        )}
        <Info className="w-3.5 h-3.5 opacity-60 hover:opacity-100 transition-opacity" />
      </div>

      {showTooltip && (
        <div className="absolute z-30 w-72 left-0 mt-2 p-3 bg-white border border-slate-200 rounded-xl shadow-xl text-xs text-slate-700 space-y-2 animate-in fade-in duration-150">
          <div className="font-semibold text-slate-900 flex items-center justify-between border-b pb-1.5">
            <span>Severity Assessment</span>
            <button
              onClick={() => setShowTooltip(false)}
              className="text-slate-400 hover:text-slate-600 font-bold px-1"
            >
              ✕
            </button>
          </div>
          <p>{config.desc}</p>
          {details?.notes && (
            <div className="bg-slate-50 p-2 rounded border border-slate-100 text-[11px] text-slate-600">
              <span className="font-medium text-slate-800">Methodology: </span>
              {details.notes}
            </div>
          )}
          {details?.is_experimental && (
            <div className="text-[10px] text-amber-700 font-medium">
              * Note: Public leaf datasets lack pathology staging ground truth; severity is an automated computer-vision estimate.
            </div>
          )}
        </div>
      )}
    </div>
  );
};
