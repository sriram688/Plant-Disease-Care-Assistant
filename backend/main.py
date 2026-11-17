"""PlantGuard AI - FastAPI Main Application Server.

Provides RESTful endpoints for real-time plant disease detection, severity analysis,
agricultural recommendations, scan history tracking, and model performance metrics.
"""

from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse

from backend.database import init_db
from backend.routers import predict, diseases, history, model_info
from src.config import (
    UPLOADS_DIR,
    MODELS_DIR,
    CLASS_NAMES,
    MOBILENET_MODEL_PATH,
    CNN_MODEL_PATH,
)
from src.predict import prediction_engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager for startup and shutdown procedures."""
    # Ensure necessary runtime directories exist
    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    # Initialize SQLite database schema
    init_db()

    # Preload model if available
    try:
        if MOBILENET_MODEL_PATH.exists() or CNN_MODEL_PATH.exists():
            prediction_engine.load_model()
            print("PlantGuard AI inference model successfully loaded into memory.")
        else:
            print("Notice: No trained model checkpoint detected yet. Training can be executed via 'python scripts/run_all.py'.")
    except Exception as exc:
        print(f"Warning: Model pre-loading deferred: {exc}")

    yield

    print("PlantGuard AI server shutting down gracefully.")


app = FastAPI(
    title="PlantGuard AI API",
    description=(
        "Production-grade, open-source Machine Learning API for plant disease classification, "
        "disease severity estimation, and evidence-based agricultural care recommendations."
    ),
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Enable CORS for React frontend (development & production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in strict production environments
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static asset routes
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(UPLOADS_DIR)), name="uploads")

# Include Modular Routers
app.include_router(predict.router)
app.include_router(diseases.router)
app.include_router(history.router)
app.include_router(model_info.router)


@app.get("/", tags=["General"])
def root():
    """Root health and system greeting."""
    return {
        "project": "PlantGuard AI – Plant Disease & Care Assistant",
        "version": "1.0.0",
        "documentation": "/docs",
        "status": "Online",
        "disclaimer": (
            "Educational and decision-support tool. Not a substitute for certified agricultural diagnosis."
        ),
    }


@app.get("/api/health", tags=["General"])
def health_check():
    """Health check endpoint confirming system and model readiness."""
    active_model = "None"
    if MOBILENET_MODEL_PATH.exists():
        active_model = "MobileNetV2 (Transfer Learning)"
    elif CNN_MODEL_PATH.exists():
        active_model = "Custom 4-Block CNN"

    return {
        "status": "healthy",
        "model_loaded": prediction_engine.is_model_loaded(),
        "active_model": active_model,
        "classes_count": len(CLASS_NAMES),
        "version": "1.0.0",
        "framework": "TensorFlow / Keras 2.16",
    }


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Catch-all unexpected error handler returning clear JSON error envelopes."""
    return JSONResponse(
        status_code=500,
        content={
            "error": "InternalServerError",
            "message": str(exc),
            "path": request.url.path,
        },
    )
