from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from app.services.adaptive.manager import adaptive_manager
from app.services.adaptive.models import FeedbackType

router = APIRouter()

@router.get("/suggestions")
def get_suggestions():
    return adaptive_manager.get_suggestions()

@router.get("/patterns")
def get_patterns():
    return adaptive_manager.get_patterns()

@router.get("/history")
def get_history():
    return adaptive_manager.get_history()

@router.get("/settings")
def get_settings():
    return adaptive_manager.get_policies()

@router.post("/settings")
def update_settings(payload: Dict[str, Any]):
    adaptive_manager.update_policies(**payload)
    return adaptive_manager.get_policies()

@router.post("/feedback")
def submit_feedback(payload: Dict[str, str]):
    suggestion_id = payload.get("suggestion_id")
    feedback = payload.get("feedback")
    
    if not suggestion_id or not feedback:
        raise HTTPException(status_code=400, detail="Missing suggestion_id or feedback")
        
    try:
        feedback_type = FeedbackType(feedback)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid feedback type")
        
    adaptive_manager.submit_feedback(suggestion_id, feedback_type)
    return {"status": "success"}
