import { useState, useEffect } from "react";
import { Search, AlertCircle, RefreshCw, ChevronDown, ChevronUp } from "lucide-react";
import { getDiseases } from "../services/api";
import type { DiseaseInfo } from "../types";

export const DiseaseLibrary = () => {
  const [diseases, setDiseases] = useState<DiseaseInfo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [plantFilter, setPlantFilter] = useState("All");
  const [expandedId, setExpandedId] = useState<string | null>(null);

  useEffect(() => {
    getDiseases()
      .then((data) => {
        setDiseases(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message || "Failed to load disease library");
        setLoading(false);
      });
  }, []);

  const plants = ["All", "Tomato", "Potato", "Pepper"];

  const filteredDiseases = diseases.filter((d) => {
    const matchesPlant = plantFilter === "All" || d.plant.toLowerCase() === plantFilter.toLowerCase();
    const query = searchQuery.toLowerCase();
    const matchesQuery =
      d.disease.toLowerCase().includes(query) ||
      d.plant.toLowerCase().includes(query) ||
      d.symptoms.toLowerCase().includes(query) ||
      d.description.toLowerCase().includes(query);
    return matchesPlant && matchesQuery;
  });

  return (
    <div className="py-6 sm:py-10 space-y-8 max-w-6xl mx-auto">
      {/* Header */}
      <div className="text-center space-y-2">
        <h1 className="text-3xl font-extrabold text-slate-900">Plant Disease Library</h1>
        <p className="text-xs sm:text-sm text-slate-600 max-w-xl mx-auto">
          Comprehensive agricultural knowledge base detailing pathology, observable symptoms,
          diagnostic cues, and agronomic treatments.
        </p>
      </div>

      {/* Search & Filter Toolbar */}
      <div className="bg-white p-4 rounded-2xl border border-slate-200 shadow-xs flex flex-col sm:flex-row gap-4 justify-between items-center">
        {/* Search Input */}
        <div className="relative w-full sm:w-80">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
          <input
            type="text"
            placeholder="Search plant, disease, or symptoms..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-9 pr-4 py-2 text-xs bg-slate-50 border border-slate-200 rounded-xl focus:outline-hidden focus:border-emerald-500 transition-colors"
          />
        </div>

        {/* Filter Buttons */}
        <div className="flex items-center space-x-1 w-full sm:w-auto overflow-x-auto">
          {plants.map((p) => (
            <button
              key={p}
              onClick={() => setPlantFilter(p)}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition-all ${
                plantFilter === p
                  ? "bg-emerald-600 text-white shadow-xs"
                  : "bg-slate-100 text-slate-600 hover:bg-slate-200"
              }`}
            >
              {p}
            </button>
          ))}
        </div>
      </div>

      {/* Content */}
      {loading ? (
        <div className="flex flex-col items-center justify-center py-20 text-slate-500">
          <RefreshCw className="w-8 h-8 animate-spin text-emerald-600 mb-2" />
          <span className="text-xs font-semibold">Loading Catalog...</span>
        </div>
      ) : error ? (
        <div className="p-4 bg-rose-50 border border-rose-200 text-rose-700 rounded-2xl text-xs flex items-center space-x-2">
          <AlertCircle className="w-4 h-4" />
          <span>{error}</span>
        </div>
      ) : filteredDiseases.length === 0 ? (
        <div className="text-center py-16 bg-white rounded-3xl border border-slate-200 text-slate-500 text-xs">
          No matching plant diseases found. Try adjusting your search query.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {filteredDiseases.map((d) => {
            const isExpanded = expandedId === d.class_name;
            const isHealthy = d.status.toLowerCase() === "healthy";

            return (
              <div
                key={d.class_name}
                className="bg-white rounded-3xl border border-slate-200 p-6 shadow-xs hover:border-emerald-300 transition-all flex flex-col justify-between"
              >
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-[11px] font-bold uppercase tracking-wider px-2.5 py-0.5 rounded-full bg-slate-100 text-slate-700">
                      {d.plant}
                    </span>
                    <span
                      className={`text-[11px] font-bold uppercase tracking-wider px-2.5 py-0.5 rounded-full ${
                        isHealthy
                          ? "bg-emerald-100 text-emerald-800"
                          : "bg-rose-100 text-rose-800"
                      }`}
                    >
                      {d.status}
                    </span>
                  </div>

                  <div>
                    <h3 className="text-lg font-bold text-slate-900">{d.disease}</h3>
                    {d.scientific_name !== "N/A" && (
                      <p className="text-xs italic text-slate-400 font-serif">
                        {d.scientific_name}
                      </p>
                    )}
                  </div>

                  <p className="text-xs text-slate-600 leading-relaxed line-clamp-3">
                    {d.description}
                  </p>

                  {/* Expandable details */}
                  {isExpanded && (
                    <div className="pt-4 border-t border-slate-100 space-y-3 text-xs text-slate-700 animate-in fade-in duration-200">
                      <div>
                        <span className="font-bold text-slate-900 block mb-1">Symptoms:</span>
                        <p className="text-slate-600 leading-relaxed">{d.symptoms}</p>
                      </div>

                      {d.diagnostic_cues && (
                        <div>
                          <span className="font-bold text-slate-900 block mb-1">Diagnostic Cues:</span>
                          <p className="text-slate-600 leading-relaxed">{d.diagnostic_cues}</p>
                        </div>
                      )}

                      {d.care && (
                        <div className="bg-slate-50 p-3 rounded-xl border border-slate-100 space-y-2">
                          <span className="font-bold text-emerald-800 block text-[11px] uppercase tracking-wider">
                            Treatment Highlights
                          </span>
                          <p className="text-[11px]">
                            <strong className="text-slate-800">Organic: </strong>
                            {d.care.organic_treatment}
                          </p>
                          <p className="text-[11px]">
                            <strong className="text-slate-800">Prevention: </strong>
                            {d.care.prevention}
                          </p>
                        </div>
                      )}
                    </div>
                  )}
                </div>

                <div className="pt-4 mt-2 border-t border-slate-50 flex items-center justify-between">
                  <span className="text-[11px] font-mono text-slate-400">
                    {d.class_name}
                  </span>
                  <button
                    onClick={() => setExpandedId(isExpanded ? null : d.class_name)}
                    className="flex items-center space-x-1 text-xs font-semibold text-emerald-600 hover:text-emerald-700"
                  >
                    <span>{isExpanded ? "Show Less" : "Detailed Profile"}</span>
                    {isExpanded ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
