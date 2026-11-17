import { Leaf, ShieldAlert, Heart } from "lucide-react";

export const Footer = () => {
  return (
    <footer className="bg-slate-900 text-slate-400 text-sm mt-auto border-t border-slate-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
          {/* Brand & Purpose */}
          <div>
            <div className="flex items-center space-x-2 text-white font-bold text-lg mb-3">
              <div className="w-8 h-8 rounded-lg bg-emerald-600 flex items-center justify-center text-white">
                <Leaf className="w-5 h-5" />
              </div>
              <span>PlantGuard AI</span>
            </div>
            <p className="text-slate-400 text-xs leading-relaxed">
              An open-source, academic machine learning system engineered to assist farmers,
              agronomists, and students in identifying plant foliar diseases and applying sustainable
              care measures.
            </p>
          </div>

          {/* Academic & Open-Source Integrity */}
          <div>
            <h4 className="text-white font-semibold text-xs tracking-wider uppercase mb-3 flex items-center space-x-1.5">
              <ShieldAlert className="w-4 h-4 text-amber-400" />
              <span>Responsible Use Statement</span>
            </h4>
            <p className="text-xs text-slate-400 leading-relaxed">
              PlantGuard AI is an educational project. Its model predictions and severity estimates
              must not be considered certified laboratory plant pathology diagnoses. Always consult
              agricultural extension professionals for commercial crop treatments.
            </p>
          </div>

          {/* Open-Source Specs */}
          <div>
            <h4 className="text-white font-semibold text-xs tracking-wider uppercase mb-3">
              Technical Stack & License
            </h4>
            <p className="text-xs text-slate-400 mb-2">
              Powered by TensorFlow 2.16, MobileNetV2, OpenCV, FastAPI, and React 19.
            </p>
            <div className="flex items-center space-x-3 text-xs text-slate-400">
              <span className="px-2 py-1 bg-slate-800 rounded text-emerald-400 font-mono">
                MIT License
              </span>
              <span className="px-2 py-1 bg-slate-800 rounded font-mono">
                Python 3.11
              </span>
            </div>
          </div>
        </div>

        <div className="border-t border-slate-800 pt-6 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-500">
          <div>
            © 2026 PlantGuard AI Contributors. Designed for academic and open-source demonstration.
          </div>
          <div className="flex items-center space-x-4 mt-3 sm:mt-0">
            <span className="flex items-center">
              Built with <Heart className="w-3.5 h-3.5 text-rose-500 mx-1 inline" /> for sustainable agriculture
            </span>
          </div>
        </div>
      </div>
    </footer>
  );
};
