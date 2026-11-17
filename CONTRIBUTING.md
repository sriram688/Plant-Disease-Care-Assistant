# Contributing to PlantGuard AI 🌿

Thank you for your interest in contributing to **PlantGuard AI – Plant Disease & Care Assistant**! We welcome contributions from machine learning practitioners, agricultural scientists, frontend engineers, and open-source enthusiasts.

## Code of Conduct

All contributors and maintainers are expected to adhere to our [Code of Conduct](CODE_OF_CONDUCT.md). Please report unacceptable behavior to the project maintainers.

## How Can You Contribute?

1. **Expanding Pathological Coverage**: Curate verified datasets for additional crops (e.g. apple, maize, rice, grape).
2. **Model Optimization**: Benchmark lightweight architectures (e.g. EfficientNet-Lite, MobileNetV3) for edge/mobile inference.
3. **Multilingual Care Advice**: Translate care protocols into regional agricultural languages (Hindi, Spanish, Swahili, etc.).
4. **Severity Labeling**: Contribute clinical pathology severity-annotated datasets.
5. **UI/UX Refinements**: Improve accessibility and responsive design for field use on mobile devices.
6. **Documentation**: Enhance documentation, tutorials, and demonstration walkthroughs.

## Development Workflow

### 1. Fork & Clone
```bash
git clone https://github.com/your-username/plantguard-ai.git
cd plantguard-ai
```

### 2. Set Up Virtual Environment (Python 3.11 recommended)
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Setup Frontend
```bash
cd frontend
npm install
npm run dev
```

### 4. Running Backend
```bash
uvicorn backend.main:app --reload --port 8000
```

### 5. Running Automated Tests
```bash
pytest -v tests/
```

### 6. Submitting a Pull Request
- Create a dedicated topic branch: `git checkout -b feature/your-feature-name`
- Write unit tests for new functionality.
- Ensure all automated tests pass.
- Commit using semantic commit messages: `feat:`, `fix:`, `docs:`, `test:`, `refactor:`.
- Push to your fork and submit a Pull Request with a clear description and test evidence.

## ML Contribution Standards
- **No Synthetic Accuracy Claims**: Never commit modified test evaluation results. Metrics must be derived directly from independent holdout partitions.
- **Data Leakage Safeguards**: Never apply data augmentation to validation or test splits.
- **Reproducibility**: Set explicit random seeds (`tf.keras.utils.set_random_seed(42)`).
