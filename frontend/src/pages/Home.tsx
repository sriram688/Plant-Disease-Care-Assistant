import {
  Activity,
  ShieldCheck,
  Sprout,
  BarChart3,
  ArrowRight,
  Sparkles,
  Layers,
} from "lucide-react";

interface HomeProps {
  setActiveTab: (tab: string) => void;
}

export const Home = ({ setActiveTab }: HomeProps) => {
  return (
    <div className="space-y-16 py-6 sm:py-10">
      {/* Hero Section */}
      <section className="text-center max-w-4xl mx-auto space-y-6">
        <div className="inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-full bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs font-semibold shadow-xs">
          <Sparkles className="w-4 h-4 text-emerald-600" />
          <span>Open-Source Educational AI for Plant Pathology</span>
        </div>

        <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold text-slate-900 tracking-tight leading-tight">
          Protect Your Harvest with{" "}
          <span className="bg-gradient-to-r from-emerald-600 to-teal-600 bg-clip-text text-transparent">
            AI-Powered
          </span>{" "}
          Plant Diagnostics
        </h1>

        <p className="text-base sm:text-lg text-slate-600 max-w-2xl mx-auto leading-relaxed">
          Upload a photo of a plant leaf to immediately detect fungal or bacterial diseases,
          estimate severity, understand observable visual cues, and receive evidence-based care advice.
        </p>

        <div className="flex flex-wrap items-center justify-center gap-4 pt-2">
          <button
            onClick={() => setActiveTab("detect")}
            className="flex items-center space-x-2 px-6 py-3.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-2xl font-semibold shadow-lg shadow-emerald-200 transition-all hover:scale-105 active:scale-95"
          >
            <Activity className="w-5 h-5" />
            <span>Analyze Leaf Now</span>
            <ArrowRight className="w-4 h-4" />
          </button>
          <button
            onClick={() => setActiveTab("library")}
            className="flex items-center space-x-2 px-6 py-3.5 bg-white hover:bg-slate-50 text-slate-700 border border-slate-200 rounded-2xl font-semibold shadow-xs transition-all"
          >
            <span>Browse Disease Library</span>
          </button>
        </div>
      </section>

      {/* Highlights Grid */}
      <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded-3xl border border-slate-200 shadow-xs space-y-3 hover:border-emerald-300 transition-colors">
          <div className="w-12 h-12 rounded-2xl bg-emerald-50 text-emerald-600 flex items-center justify-center">
            <Layers className="w-6 h-6" />
          </div>
          <h3 className="font-bold text-slate-900 text-base">Dual CNN Architecture</h3>
          <p className="text-xs text-slate-600 leading-relaxed">
            Compares a custom 4-block CNN baseline with MobileNetV2 transfer learning trained on
            tomato, potato, and pepper foliar datasets.
          </p>
        </div>

        <div className="bg-white p-6 rounded-3xl border border-slate-200 shadow-xs space-y-3 hover:border-emerald-300 transition-colors">
          <div className="w-12 h-12 rounded-2xl bg-amber-50 text-amber-600 flex items-center justify-center">
            <ShieldCheck className="w-6 h-6" />
          </div>
          <h3 className="font-bold text-slate-900 text-base">Honest Severity Staging</h3>
          <p className="text-xs text-slate-600 leading-relaxed">
            Avoids false claims. Healthy leaves show None; diseased leaves use computer vision
            lesion area segmentation clearly flagged as experimental.
          </p>
        </div>

        <div className="bg-white p-6 rounded-3xl border border-slate-200 shadow-xs space-y-3 hover:border-emerald-300 transition-colors">
          <div className="w-12 h-12 rounded-2xl bg-teal-50 text-teal-600 flex items-center justify-center">
            <Sprout className="w-6 h-6" />
          </div>
          <h3 className="font-bold text-slate-900 text-base">Actionable Agronomy Care</h3>
          <p className="text-xs text-slate-600 leading-relaxed">
            Delivers immediate actions, certified organic treatments (neem, bio-fungicides),
            cultural pruning, and disease prevention protocols.
          </p>
        </div>

        <div className="bg-white p-6 rounded-3xl border border-slate-200 shadow-xs space-y-3 hover:border-emerald-300 transition-colors">
          <div className="w-12 h-12 rounded-2xl bg-sky-50 text-sky-600 flex items-center justify-center">
            <BarChart3 className="w-6 h-6" />
          </div>
          <h3 className="font-bold text-slate-900 text-base">Open Evaluation Metrics</h3>
          <p className="text-xs text-slate-600 leading-relaxed">
            Inspect real test set metrics: accuracy, precision, recall, F1, confusion matrix,
            and class imbalance without hidden test errors.
          </p>
        </div>
      </section>

      {/* Diagnostic Pipeline Steps */}
      <section className="bg-white border border-slate-200 rounded-3xl p-8 sm:p-10 shadow-xs space-y-8">
        <div className="text-center max-w-xl mx-auto">
          <h2 className="text-2xl font-extrabold text-slate-900">End-to-End Diagnostic Pipeline</h2>
          <p className="text-xs text-slate-500 mt-1">
            How PlantGuard AI transforms raw leaf pixels into actionable agricultural insights.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-5 gap-4 relative">
          {[
            { step: "01", title: "Image Upload", desc: "RGB photo ingestion with MIME & size validation." },
            { step: "02", title: "Preprocessing", desc: "Lanczos 224x224 resize, color normalization & leaf isolation." },
            { step: "03", title: "Neural Inference", desc: "MobileNetV2 feature extraction & Softmax distribution." },
            { step: "04", title: "Severity Staging", desc: "OpenCV lesion surface coverage calculation." },
            { step: "05", title: "Care Delivery", desc: "Curated domain metadata matching immediate remedies." },
          ].map((item, idx) => (
            <div key={idx} className="bg-slate-50 rounded-2xl p-4 border border-slate-100 space-y-2">
              <span className="text-xs font-mono font-bold text-emerald-600 bg-emerald-100 px-2 py-0.5 rounded-full">
                {item.step}
              </span>
              <h4 className="font-bold text-slate-800 text-sm">{item.title}</h4>
              <p className="text-xs text-slate-500 leading-relaxed">{item.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Educational Notice Banner */}
      <section className="bg-gradient-to-r from-emerald-800 to-teal-900 rounded-3xl p-8 text-white text-center sm:text-left flex flex-col sm:flex-row items-center justify-between gap-6 shadow-md">
        <div className="space-y-2">
          <h3 className="text-xl font-bold">Academic & Open Source Initiative</h3>
          <p className="text-xs text-emerald-100 max-w-2xl leading-relaxed">
            PlantGuard AI is released under the MIT License for educational use, B.Tech final-year
            capstone presentations, and machine learning research. It does not replace professional
            diagnostic certification.
          </p>
        </div>
        <button
          onClick={() => setActiveTab("about")}
          className="shrink-0 px-5 py-2.5 bg-white text-emerald-900 hover:bg-emerald-50 rounded-xl font-semibold text-xs transition-all"
        >
          Read Specifications
        </button>
      </section>
    </div>
  );
};
