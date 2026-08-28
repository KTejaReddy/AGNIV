from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from enum import Enum
import uuid
import time

class ConfidenceLevel(str, Enum):
    VERY_LOW = "VERY_LOW"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    VERY_HIGH = "VERY_HIGH"

class FeedbackType(str, Enum):
    ACCEPT = "ACCEPT"
    REJECT = "REJECT"
    REMIND_LATER = "REMIND_LATER"
    NEVER_SUGGEST_AGAIN = "NEVER_SUGGEST_AGAIN"

class Pattern(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: str
    frequency: int
    first_seen: float
    last_seen: float
    context_data: Dict[str, Any] = {}

class BehaviorSummary(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    description: str
    related_patterns: List[str]
    confidence: ConfidenceLevel

class Suggestion(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    reason: str
    evidence: List[str]
    confidence: ConfidenceLevel
    impact: str
    estimated_time_saved: str
    required_permissions: List[str]
    created_at: float = Field(default_factory=time.time)
    status: str = "PENDING"  # PENDING, ACCEPTED, REJECTED, DISMISSED, NEVER

class AdaptivePolicies(BaseModel):
    suggestion_frequency: str = "NORMAL"
    minimum_confidence: ConfidenceLevel = ConfidenceLevel.MEDIUM
    max_suggestions_per_day: int = 5
    quiet_hours: bool = False
