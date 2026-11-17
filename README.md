# 🌿 PlantGuard AI – Plant Disease & Care Assistant

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![TensorFlow 2.16](https://img.shields.io/badge/TensorFlow-2.16-FF6F00.svg?logo=tensorflow&logoColor=white)](https://tensorflow.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React 19](https://img.shields.io/badge/React-19-61DAFB.svg?logo=react&logoColor=black)](https://react.dev/)
[![Tailwind CSS v4](https://img.shields.io/badge/Tailwind_CSS-v4.0-38B2AC.svg?logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![Docker Ready](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white)](Dockerfile)

> **An open-source, production-engineered deep learning web application that diagnoses plant foliar diseases, estimates symptom severity, delivers actionable organic and conventional agronomic care protocols, and provides transparent model performance metrics.**

---

## 📌 Table of Contents

- [Overview & Problem Statement](#-overview--problem-statement)
- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [Dataset & Provenance](#-dataset--provenance)
- [Model Engineering & Methodology](#-model-engineering--methodology)
- [Severity Estimation Methodology](#-severity-estimation-methodology)
- [Installation & Quickstart](#-installation--quickstart)
- [Model Training & Evaluation](#-model-training--evaluation)
- [FastAPI Backend Documentation](#-fastapi-backend-documentation)
- [React Frontend Interface](#-react-frontend-interface)
- [Screenshots & Visuals](#-screenshots--visuals)
- [Automated Testing](#-automated-testing)
- [Docker Deployment](#-docker-deployment)
- [Limitations & Real-World Constraints](#-limitations--real-world-constraints)
- [Responsible-Use Statement & Educational Disclaimer](#-responsible-use-statement--educational-disclaimer)
- [Future Extensions](#-future-extensions)
- [Contributing](#-contributing)
- [License](#-license)

---

## 📖 Overview & Problem Statement

Crop losses from unmanaged fungal and bacterial foliar diseases present a major challenge to food security, crop yield, and livelihood stability—especially for smallholder farmers and horticultural growers. 

Traditional machine learning projects for plant pathology often:
1. **Report inflated or misleading accuracy scores** without presenting genuine independent test set metrics.
2. **Fabricate clinical disease severity levels** without pathology-ground-truth labeling in the source dataset.
3. **Stop at classification**, failing to provide the farmer or student with actionable, sustainable care, organic remedies, and prevention advice.
4. **Lack production-ready engineering**, existing only as unwieldy monolithic Jupyter notebooks.

**PlantGuard AI** addresses these gaps directly. Designed as an exemplary B.Tech final-year capstone, academic portfolio, and open-source demonstration, PlantGuard AI combines deep learning (MobileNetV2 / Custom CNN) with computer vision severity heuristics, evidence-based agricultural care protocols, interactive prediction audit trails, and an uncompromised model evaluation dashboard.

---

## ✨ Key Features

- **Leaf Disease Detection**: Instant prediction across 9 benchmark tomato, potato, and pepper foliar conditions.
- **Dual Architecture Comparison**: Benchmarks a lightweight 4-block baseline CNN against a transfer-learning **MobileNetV2** backbone.
- **Honest Severity Staging**:
  - Healthy foliage is reliably categorized as `None`.
  - Diseased leaves compute an OpenCV-based necrotic lesion surface area ratio ($<15\%$ Low, $15-35\%$ Medium, $>35\%$ High) and are explicitly disclosed as an **automated visual heuristic (experimental)**.
- **Actionable Care & Agronomy Protocols**:
  - Immediate quarantine/pruning actions.
  - Certified organic treatments (copper fungicides, Bacillus subtilis, cold-pressed neem oil).
  - Cultural agronomic practices (drip irrigation, canopy airflow, spacing, mulching).
  - Long-term prevention strategies (resistant crop varieties, multi-year Solanaceae crop rotation).
  - Regulated chemical options where appropriate.
- **Plain-Language Explanations**: Diagnostic summaries highlighting characteristic symptoms (target-board concentric rings, chlorotic yellow halos, water-soaked dark lesions).
- **Persistent Scan History**: SQLite-backed prediction history with thumbnail previews, confidence levels, and user feedback audit logging.
- **Transparent Model Dashboard**: Real holdout test set accuracy, macro/weighted precision, recall, F1-scores, full confusion matrix heatmap, and training/validation loss curves.
- **1-Click Test Drive**: Curated demo test samples built directly into the UI for instant browser testing without searching for leaf photos.

---

## 🏗️ System Architecture

```mermaid
flowchart TD
    User([User / Farmer / Student]) -->|Uploads Leaf Image| Frontend[React 19 + TypeScript + Tailwind UI]
    Frontend -->|POST /api/predict| API[FastAPI Backend Server]
    
    subgraph Preprocessing & Validation
        API --> InputCheck[Format & Size Validation]
        InputCheck --> ResizeNorm[Lanczos 224x224 & [0, 1] Rescaling]
    end

    subgraph Deep Learning Inference
        ResizeNorm --> Model[MobileNetV2 / Custom CNN]
        Model --> Softmax[Softmax Probability Distribution]
        Softmax --> TopK[Top-1 Disease & Top-3 Candidates]
    end

    subgraph Pathology & Knowledge Services
        ResizeNorm --> SeverityCV[OpenCV Lesion Area Heuristic]
        TopK --> MetaService[Domain Metadata Service]
        SeverityCV --> SeverityResult[Severity: None / Low / Med / High]
        MetaService --> CarePlan[Curated Care & Prevention Protocols]
    end

    subgraph Persistence & Audit
        TopK --> DB[(SQLite Database / PostgreSQL)]
        SeverityResult --> DB
    end

    TopK --> ResponseAgg[JSON Diagnostic Envelope]
    SeverityResult --> ResponseAgg
    CarePlan --> ResponseAgg
    ResponseAgg -->|Structured JSON| Frontend
```

---

## 🗂️ Dataset & Provenance

PlantGuard AI structures data into three non-leaking partitions:

```
dataset/
├── train/       (70% - Data augmentation applied)
├── validation/  (15% - Zero augmentation)
└── test/        (15% - Independent holdout evaluation)
```

### Supported Benchmark Classes

| Class Directory | Plant | Condition | Pathogen / Causative Agent |
| :--- | :--- | :--- | :--- |
| `pepper_bacterial_spot` | Pepper | Bacterial Spot | *Xanthomonas campestris pv. vesicatoria* |
| `pepper_healthy` | Pepper | Healthy | *Capsicum annuum* (Normal) |
| `potato_early_blight` | Potato | Early Blight | *Alternaria solani* |
| `potato_healthy` | Potato | Healthy | *Solanum tuberosum* (Normal) |
| `potato_late_blight` | Potato | Late Blight | *Phytophthora infestans* |
| `tomato_bacterial_spot` | Tomato | Bacterial Spot | *Xanthomonas perforans / vesicatoria* |
| `tomato_early_blight` | Tomato | Early Blight | *Alternaria solani* |
| `tomato_healthy` | Tomato | Healthy | *Solanum lycopersicum* (Normal) |
| `tomato_late_blight` | Tomato | Late Blight | *Phytophthora infestans* |

### Source Attribution & License
The dataset schema aligns with the gold-standard **PlantVillage** benchmark (Hughes & Salathé, Penn State University), distributed under the **Creative Commons Attribution 4.0 International (CC-BY 4.0)** license.

---

## 🔬 Model Engineering & Methodology

### 1. Data Augmentation Pipeline
Applied strictly to training partitions to preserve biological realism while guarding against overfitting:
- **Random Horizontal Flip**: Biologically invariant for bilateral foliar leaves.
- **Random Rotation ($\pm 15^\circ$)**: Accounts for hand-held phone camera rotation.
- **Random Zoom ($\pm 8\%$)**: Simulates variable photographer distances.
- **Random Translation ($\pm 4\%$)**: Robustness to non-centered leaves.
- **Random Brightness ($\pm 8\%$)**: Simulates varying solar exposure without altering disease lesion pigmentation.

### 2. Architectures
- **Custom 4-Block CNN**: 4 successive `Conv2D(32/64/128/256)` blocks with `BatchNormalization`, `ReLU`, `MaxPooling2D`, `SpatialDropout`, and `GlobalAveragePooling2D`.
- **MobileNetV2 (Transfer Learning)**: Pre-trained on ImageNet, utilizing inverted residual blocks and linear bottlenecks for efficient mobile-grade inference.

---

## 📐 Severity Estimation Methodology

PlantGuard AI enforces scientific transparency regarding severity estimation:

```
      Leaf Image
          ↓
  Foliage HSV Masking (H: 10-95, S: 20-255, V: 20-255)
          ↓
  Lesion HSV Masking (Necrotic chlorosis, brown spotting, dark centers)
          ↓
  Lesion Area Ratio = (Lesion Pixels) / (Total Leaf Pixels)
          ↓
  Categorization:
    • None   → Healthy leaf classification (0% lesions)
    • Low    → Lesion Area < 15%
    • Medium → Lesion Area 15% - 35%
    • High   → Lesion Area > 35%
```

> **Educational Caveat**: Because public leaf datasets do not provide clinical pathology severity staging labels, this score is derived via computer-vision surface segmentation and is explicitly marked in the API response and web UI as **"Estimated via Leaf Lesion Area Heuristic (Experimental)"**.

---

## 🚀 Installation & Quickstart

### Prerequisites
- Python 3.11 (`python --version`)
- Node.js 18+ and npm (`node --version`)
- Git

### 1. Clone Repository
```bash
git clone https://github.com/your-username/plantguard-ai.git
cd plantguard-ai
```

### 2. Configure Python Virtual Environment
```bash
# Windows
py -3.11 -m venv .venv
.venv\Scripts\activate

# Linux / macOS
python3.11 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Setup Frontend
```bash
cd frontend
npm install
cd ..
```

---

## 🧠 Model Training & Evaluation

To prepare the dataset, train the neural network, generate independent test evaluation metrics, and create demo assets with a single command:

```bash
# Automated 1-command pipeline
python scripts/run_all.py --architecture mobilenetv2 --epochs 10 --batch-size 16
```

Or execute modular pipeline steps individually:

```bash
# Step 1: Generate balanced starter benchmark dataset
python scripts/prepare_dataset.py --mode starter --train-count 35 --val-count 10 --test-count 10

# Step 2: Train MobileNetV2 or Custom CNN
python -m src.train --architecture mobilenetv2 --epochs 10 --batch-size 16

# Step 3: Run holdout evaluation
python -m src.evaluate --model models/plantguard_mobilenetv2.keras

# Step 4: Generate UI demo samples
python scripts/demo_samples.py
```

---

## ⚡ FastAPI Backend Documentation

Launch the ASGI backend server:

```bash
# From project root with .venv activated
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### Core API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | API greeting and system metadata |
| `GET` | `/api/health` | Service health, model load status, and active architecture |
| `POST` | `/api/predict` | Multipart image upload for disease inference & severity staging |
| `GET` | `/api/diseases` | Full catalog of 9 supported conditions, symptoms, and care plans |
| `GET` | `/api/diseases/{class_name}` | Detailed pathology profile for a specific class |
| `GET` | `/api/history` | Paginated diagnosis logs with confidence and severity records |
| `DELETE`| `/api/history/{id}` | Remove a diagnosis scan from the database |
| `POST` | `/api/history/{id}/feedback` | Log farmer or researcher accuracy feedback |
| `GET` | `/api/model-info` | Real holdout test set accuracy, precision, recall, and F1 |
| `GET` | `/api/model-info/confusion-matrix` | Download holdout confusion matrix heatmap image |
| `GET` | `/api/model-info/training-curves` | Download loss and accuracy training curves plot |

Interactive Swagger documentation is accessible at: [`http://localhost:8000/docs`](http://localhost:8000/docs)

---

## 💻 React Frontend Interface

Launch the Vite React 19 development server:

```bash
cd frontend
npm run dev
```

Visit [`http://localhost:5173`](http://localhost:5173) in your browser.

### Key Pages
1. **Home**: Hero section, technical overview, and end-to-end diagnostic pipeline.
2. **Disease Detection**: Drag-and-drop file uploader with 1-click demo test samples, live leaf preview, and instant analysis.
3. **Diagnosis Results**: High-impact diagnosis card with confidence gauge, top-3 candidates, severity meter, and categorized care protocols.
4. **Disease Library**: Searchable and filterable knowledge base with detailed symptoms and diagnostic visual cues.
5. **Prediction History**: Table of previous scans with thumbnails, confidence, and feedback logging.
6. **Model Dashboard**: Real test set metrics, confusion matrix visualization, and training/validation curves.
7. **About**: Educational mission, responsible use disclaimer, dataset provenance, and future roadmap.

---

## 🖼️ Screenshots & Visuals

```
┌────────────────────────────────────────────────────────────────────────┐
│  🌿 PlantGuard AI – Plant Disease & Care Assistant      [● MobileNetV2]│
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│   Protect Your Harvest with AI-Powered Plant Diagnostics               │
│                                                                        │
│   [ 📷 Drag & Drop Leaf Image or Choose from 1-Click Samples ]         │
│   [Tomato Early Blight] [Tomato Healthy] [Potato Early Blight] ...     │
│                                                                        │
├────────────────────────────────────────────────────────────────────────┤
│  DIAGNOSTIC CARD:                                                      │
│  Plant: Tomato | Condition: Early Blight (Alternaria solani)           │
│  Confidence: 94.2%  ████████████████████████████░░░░░                  │
│  Severity: Medium (22.4% Lesion Area) [Info: Experimental CV Heuristic]│
│                                                                        │
│  [Immediate Action] [Organic Treatment] [Cultural Practices]           │
│  • Prune lower infected leaflets showing target-board concentric spots.│
│  • Apply organic copper fungicide or bio-fungicide (Bacillus subtilis).│
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 🧪 Automated Testing

Comprehensive test suite covering image preprocessing, model compilation, severity analysis, metadata lookups, and FastAPI endpoints:

```bash
pytest -v tests/
```

Test coverage includes:
- `tests/test_preprocessing.py`: Byte validation, Lanczos resizing, normalization, leaf contour segmentation.
- `tests/test_severity.py`: Healthy `None` severity, diseased `Low/Medium/High` severity with experimental flag.
- `tests/test_metadata.py`: CSV schema integrity and fallback lookups for all 9 classes.
- `tests/test_model.py`: Custom CNN layer compilation and tensor shape integrity.
- `tests/test_api.py`: FastAPI endpoints (`/`, `/api/health`, `/api/diseases`, `/api/model-info`, file upload validation).

---

## 🐳 Docker Deployment

Run the complete multi-stage containerized stack using Docker Compose:

```bash
docker-compose up --build
```

Access the unified service on port `8000`.

---

## ⚠️ Limitations & Real-World Constraints

1. **Environmental Variance**: Laboratory benchmark datasets feature leaves on neutral backgrounds. Performance in uncontrolled field environments with extreme shadow angles or cluttered soil backgrounds may require higher confidence thresholds.
2. **Coinfections**: Plants infected simultaneously with multiple pathogens (e.g. bacterial spot and early blight) will be mapped to the dominant softmax class.
3. **Severity Staging**: As public benchmark datasets lack clinical pathology staging labels, severity is computed as an automated surface lesion ratio rather than clinical histological depth.

---

## 📜 Responsible-Use Statement & Educational Disclaimer

> **IMPORTANT NOTICE**:
> PlantGuard AI is developed exclusively for educational, technical demonstration, and academic capstone purposes. The predictions, severity scores, and treatment recommendations provided by this system do **NOT** constitute a certified agricultural, pathological, or agronomic diagnosis. 
> Commercial growers and farmers should consult certified agricultural extension officers or university plant pathology laboratories before applying chemical treatments or making significant crop management decisions.

---

## 🔮 Future Extensions

- **Broader Species Coverage**: Extend training to 38+ plant-disease pairs across maize, apple, grape, and rice.
- **Edge Inference**: Export quantized models to TensorFlow Lite and ONNX Web for offline smartphone inference in rural regions.
- **Multilingual Support**: Translate recommendations into regional languages (Hindi, Spanish, Swahili, Telugu).
- **Disease Progression Tracking**: Time-series analysis allowing farmers to monitor disease recovery across repeat weekly scans.

---

## 🤝 Contributing

We welcome contributions! Please review our [CONTRIBUTING.md](CONTRIBUTING.md) guide and adhere to our [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

---

## 📄 License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.
