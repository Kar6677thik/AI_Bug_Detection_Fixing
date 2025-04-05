from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
from pathlib import Path

app = FastAPI(
    title="AI Bug Detection API",
    description="API for detecting and fixing bugs in source code",
    version="0.1.0"
)

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to your frontend domain if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add backend directory to path
sys.path.append(str(Path(__file__).parent.parent))

# Initialize inference engine only if dependencies are available
try:
    from backend.model.inference import InferenceEngine
    engine = InferenceEngine()
    MODEL_LOADED = True
except ImportError:
    MODEL_LOADED = False
    print("Warning: Model dependencies not installed. Analysis endpoints will not work.")

class CodeRequest(BaseModel):
    code: str
    language: str = "python"

@app.post("/analyze")
async def analyze_code(request: CodeRequest):
    """Analyze code for bugs and suggest fixes"""
    if not MODEL_LOADED:
        return {
            "success": False,
            "error": "Model dependencies not installed"
        }
    try:
        analysis = engine.analyze_code(request.code)
        return {
            "success": True,
            "results": analysis
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": MODEL_LOADED
    }

@app.get("/test")
async def test_endpoint():
    """Test endpoint to verify server is running"""
    return {
        "message": "API server is running",
        "status": "success"
    }
