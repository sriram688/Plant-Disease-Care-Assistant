import { useState } from "react";
import { Navbar } from "./components/Navbar";
import { Footer } from "./components/Footer";
import { Home } from "./pages/Home";
import { Detect } from "./pages/Detect";
import { DiseaseLibrary } from "./pages/DiseaseLibrary";
import { History } from "./pages/History";
import { ModelDashboard } from "./pages/ModelDashboard";
import { About } from "./pages/About";

export function App() {
  const [activeTab, setActiveTab] = useState<string>("home");

  const renderContent = () => {
    switch (activeTab) {
      case "home":
        return <Home setActiveTab={setActiveTab} />;
      case "detect":
        return <Detect />;
      case "library":
        return <DiseaseLibrary />;
      case "history":
        return <History />;
      case "model":
        return <ModelDashboard />;
      case "about":
        return <About />;
      default:
        return <Home setActiveTab={setActiveTab} />;
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 text-slate-900 font-sans selection:bg-emerald-100 selection:text-emerald-900">
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8">
        {renderContent()}
      </main>
      <Footer />
    </div>
  );
}

export default App;
