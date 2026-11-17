import { useState } from "react";
import { Zap, Sprout, Wind, ShieldCheck, FlaskConical } from "lucide-react";
import type { CareDetails } from "../types";

interface CareSectionProps {
  care: CareDetails;
  isHealthy: boolean;
}

export const CareSection = ({ care, isHealthy }: CareSectionProps) => {
  const [activeTab, setActiveTab] = useState<"immediate" | "organic" | "cultural" | "prevention" | "chemical">("immediate");

  const tabs = [
    { id: "immediate", label: "Immediate Action", icon: Zap, color: "text-amber-600 bg-amber-50" },
    { id: "organic", label: "Organic Treatment", icon: Sprout, color: "text-emerald-600 bg-emerald-50" },
    { id: "cultural", label: "Cultural Practices", icon: Wind, color: "text-sky-600 bg-sky-50" },
    { id: "prevention", label: "Prevention", icon: ShieldCheck, color: "text-indigo-600 bg-indigo-50" },
    { id: "chemical", label: "Chemical Options", icon: FlaskConical, color: "text-rose-600 bg-rose-50" },
  ];

  const getContent = () => {
    switch (activeTab) {
      case "immediate":
        return care.immediate_action;
      case "organic":
        return care.organic_treatment;
      case "cultural":
        return care.cultural_practices;
      case "prevention":
        return care.prevention;
      case "chemical":
        return care.chemical_treatment || "No chemical application necessary.";
      default:
        return "";
    }
  };

  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-base font-bold text-slate-900">
            {isHealthy ? "Care & Growth Recommendations" : "Treatment & Care Recommendations"}
          </h3>
          <p className="text-xs text-slate-500">
            Evidence-based agricultural agronomy guidance for sustained crop vitality.
          </p>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex space-x-2 border-b border-slate-200 pb-2 overflow-x-auto mb-4">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`flex items-center space-x-1.5 px-3 py-2 rounded-lg text-xs font-semibold whitespace-nowrap transition-all ${
                isActive
                  ? `${tab.color} shadow-xs font-bold border border-slate-200`
                  : "text-slate-600 hover:text-slate-900 hover:bg-slate-50"
              }`}
            >
              <Icon className="w-3.5 h-3.5" />
              <span>{tab.label}</span>
            </button>
          );
        })}
      </div>

      {/* Content box */}
      <div className="bg-slate-50 border border-slate-100 rounded-xl p-4 text-sm text-slate-700 leading-relaxed">
        <p>{getContent()}</p>
      </div>
    </div>
  );
};
