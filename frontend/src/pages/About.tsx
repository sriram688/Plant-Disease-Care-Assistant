import { Leaf, ShieldAlert, Cpu, Database, Compass, CheckCircle2 } from "lucide-react";

export const About = () => {
  return (
    <div className="py-6 sm:py-10 space-y-12 max-w-4xl mx-auto">
      {/* Header */}
      <div className="text-center space-y-3">
        <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs font-semibold">
          <Leaf className="w-3.5 h-3.5 text-emerald-600" />
          <span>Open-Source Technical Portfolio Project</span>
        </div>
        <h1 className="text-4xl font-extrabold text-slate-900 tracking-tight">
          About PlantGuard AI
        </h1>
        <p className="text-sm text-slate-600 max-w-2xl mx-auto leading-relaxed">
          An open-source, production-engineered deep learning system designed for agricultural
          pathology detection, transparent severity estimation, and agronomic decision-support.
        </p>
      </div>

      {/* Project Vision & Mission */}
      <section className="bg-white rounded-3xl border border-slate-200 p-8 shadow-xs space-y-4">
        <h2 className="text-xl font-bold text-slate-900 flex items-center space-x-2">
          <Compass className="w-5 h-5 text-emerald-600" />
          <span>Project Vision & Academic Context</span>
        </h2>
        <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
          Plant diseases cause significant yield loss for smallholder farmers and home growers
          worldwide. While deep learning has proven adept at image classification, many academic
          models suffer from severe black-box obscurity, artificially inflated accuracy claims,
          and a lack of actionable post-diagnosis treatment instructions.
        </p>
        <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
          <strong>PlantGuard AI</strong> was engineered as an exemplary production-ready capstone
          project. It prioritizes genuine, transparent evaluation on holdout test partitions,
          clearly flags automated severity estimates as experimental, and provides concrete organic
          and cultural treatment recommendations.
        </p>
      </section>

      {/* Architectural Stack */}
      <section className="space-y-4">
        <h2 className="text-xl font-bold text-slate-900 flex items-center space-x-2">
          <Cpu className="w-5 h-5 text-emerald-600" />
          <span>System Architecture & Technologies</span>
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs space-y-2">
            <h3 className="text-sm font-bold text-slate-900">Machine Learning Core</h3>
            <ul className="text-xs text-slate-600 space-y-1.5 list-disc list-inside">
              <li><strong>Backbone:</strong> MobileNetV2 (ImageNet weights) & 4-block Custom CNN.</li>
              <li><strong>Framework:</strong> TensorFlow / Keras 2.16 with Python 3.11.</li>
              <li><strong>Data Augmentation:</strong> Rotation (±15°), horizontal flips, gentle zooms.</li>
              <li><strong>Severity Analysis:</strong> OpenCV HSV contour & lesion ratio segmentation.</li>
            </ul>
          </div>

          <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs space-y-2">
            <h3 className="text-sm font-bold text-slate-900">Backend & Web Delivery</h3>
            <ul className="text-xs text-slate-600 space-y-1.5 list-disc list-inside">
              <li><strong>API Framework:</strong> FastAPI with asynchronous ASGI execution.</li>
              <li><strong>Database:</strong> SQLite with SQLAlchemy (PostgreSQL-ready).</li>
              <li><strong>Frontend:</strong> React 19 + TypeScript + Vite + Tailwind CSS v4.</li>
              <li><strong>Containerization:</strong> Multi-stage Docker & docker-compose.</li>
            </ul>
          </div>
        </div>
      </section>

      {/* Dataset & Provenance */}
      <section className="bg-white rounded-3xl border border-slate-200 p-8 shadow-xs space-y-4">
        <h2 className="text-xl font-bold text-slate-900 flex items-center space-x-2">
          <Database className="w-5 h-5 text-emerald-600" />
          <span>Dataset Provenance & Benchmark Standards</span>
        </h2>
        <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
          PlantGuard AI supports benchmark splits curated from the public <em>PlantVillage</em> dataset
          (Hughes et al., Penn State University), distributed under Creative Commons Attribution 4.0
          International (CC-BY 4.0).
        </p>
        <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
          The official 9 benchmark classes span:
        </p>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-2 text-xs font-mono text-slate-700 bg-slate-50 p-4 rounded-2xl border border-slate-100">
          <div>
            <strong className="block text-emerald-800 font-sans mb-1">Tomato:</strong>
            • tomato_healthy<br />
            • tomato_early_blight<br />
            • tomato_late_blight<br />
            • tomato_bacterial_spot
          </div>
          <div>
            <strong className="block text-emerald-800 font-sans mb-1">Potato:</strong>
            • potato_healthy<br />
            • potato_early_blight<br />
            • potato_late_blight
          </div>
          <div>
            <strong className="block text-emerald-800 font-sans mb-1">Pepper Bell:</strong>
            • pepper_healthy<br />
            • pepper_bacterial_spot
          </div>
        </div>
      </section>

      {/* Responsible Use Disclaimer */}
      <section className="bg-amber-50/70 border border-amber-200 rounded-3xl p-8 space-y-3">
        <h2 className="text-lg font-bold text-amber-900 flex items-center space-x-2">
          <ShieldAlert className="w-5 h-5 text-amber-600" />
          <span>Responsible Use & Diagnostic Disclaimer</span>
        </h2>
        <p className="text-xs sm:text-sm text-amber-800 leading-relaxed">
          PlantGuard AI is strictly an educational, decision-support, and software demonstration tool.
          It does <strong>NOT</strong> present its predictions as a guaranteed certified agricultural
          or laboratory pathology diagnosis. Growers should verify severe crop symptoms with certified
          agronomists or local agricultural university extension centers before administering extensive
          chemical regimens.
        </p>
      </section>

      {/* Future Roadmap */}
      <section className="bg-white rounded-3xl border border-slate-200 p-8 shadow-xs space-y-4">
        <h2 className="text-xl font-bold text-slate-900">Future Roadmap & Extensions</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs text-slate-700">
          {[
            "Expansion to 38+ plant & disease classes (Apple, Grape, Corn, Rice).",
            "Offline mobile edge deployment via TensorFlow Lite and ONNX Web.",
            "Multilingual voice assistance for rural agricultural workers.",
            "Historical disease progression tracking via sequential scans.",
            "Integration with hyper-local weather alerts for pathogen outbreak warnings.",
            "Farmer community forums for peer advice and extension worker consultation.",
          ].map((item, idx) => (
            <div key={idx} className="flex items-start space-x-2 p-2 rounded-xl bg-slate-50">
              <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
              <span>{item}</span>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
};
