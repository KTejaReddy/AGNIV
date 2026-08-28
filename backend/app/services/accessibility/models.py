from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from enum import Enum
import uuid

class AccessibilityProfile(str, Enum):
    DEAF = "DEAF"
    BLIND = "BLIND"
    MOTOR = "MOTOR"
    GENERAL = "GENERAL"

class AccessibilitySettings(BaseModel):
    profile: AccessibilityProfile = AccessibilityProfile.GENERAL
    sign_recognition_enabled: bool = False
    live_captions_enabled: bool = False
    screen_reader_enabled: bool = False
    gesture_confirmations_enabled: bool = False
    caption_font_size: int = 16
    caption_theme: str = "dark"

class SignData(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    sign_name: str
    confidence: float
    timestamp: float
