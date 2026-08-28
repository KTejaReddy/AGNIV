from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from app.services.accessibility.manager import accessibility_manager
from app.services.accessibility.models import AccessibilityProfile
from app.services.accessibility.sign import sign_recognizer
from app.services.accessibility.reader import screen_reader

router = APIRouter()

@router.get("/profile")
def get_profile():
    return {"profile": accessibility_manager.get_profile().value}

@router.post("/profile")
def set_profile(payload: Dict[str, str]):
    profile_str = payload.get("profile")
    try:
        profile = AccessibilityProfile(profile_str)
        accessibility_manager.update_profile(profile)
        return {"status": "success", "profile": profile.value}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid profile")

@router.get("/sign")
def get_signs():
    return sign_recognizer.get_history()

@router.get("/captions")
def get_captions():
    # Since they are streamed, we just return status
    return {"enabled": accessibility_manager.get_settings().live_captions_enabled}

@router.post("/read")
async def trigger_read():
    text = await screen_reader.read_window()
    return {"status": "success", "content": text}

@router.get("/settings")
def get_settings():
    return accessibility_manager.get_settings()

@router.post("/settings")
def update_settings(payload: Dict[str, Any]):
    accessibility_manager.update_settings(**payload)
    return accessibility_manager.get_settings()
