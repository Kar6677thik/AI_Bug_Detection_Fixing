from fastapi import APIRouter, HTTPException
from ..model.inference import InferenceEngine
from pydantic import BaseModel

router = APIRouter()
engine = InferenceEngine()

class CodeRequest(BaseModel):
    code: str
    language: str = "python"

@router.post("/detect")
async def detect_bugs(request: CodeRequest):
    """Endpoint specifically for bug detection"""
    try:
        bug_report = engine.detector.detect_bugs(request.code)
        return {
            "success": True,
            "bugs": bug_report.get("bugs", []),
            "warnings": bug_report.get("warnings", []),
            "analysis": bug_report.get("analysis", "")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/fix")
async def fix_bugs(request: CodeRequest):
    """Endpoint specifically for generating fixes"""
    try:
        bug_report = engine.detector.detect_bugs(request.code)
        fixes = engine.fixer.suggest_fixes(request.code, bug_report)
        return {
            "success": True,
            "fixes": fixes
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/full-analysis")
async def full_analysis(request: CodeRequest):
    """Endpoint combining detection and fixing"""
    try:
        results = engine.analyze_code(request.code)
        return {
            "success": True,
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))