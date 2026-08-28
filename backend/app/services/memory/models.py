from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from enum import Enum
from datetime import datetime
import uuid

class MemoryType(str, Enum):
    EXPERIENCE = "EXPERIENCE"
    PREFERENCE = "PREFERENCE"
    HABIT = "HABIT"
    SKILL_USAGE = "SKILL_USAGE"
    WORKFLOW_HISTORY = "WORKFLOW_HISTORY"
    SUCCESSFUL_TASK = "SUCCESSFUL_TASK"
    FAILED_TASK = "FAILED_TASK"
    PROJECT = "PROJECT"
    SESSION = "SESSION"
    CONVERSATION_SUMMARY = "CONVERSATION_SUMMARY"

class Importance(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    TEMPORARY = "TEMPORARY"

class MemoryItem(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    summary: str
    type: MemoryType
    timestamp: float = Field(default_factory=lambda: datetime.now().timestamp())
    importance: Importance = Importance.MEDIUM
    confidence: float = 1.0
    source: str
    
    related_skills: List[str] = []
    related_workflows: List[str] = []
    related_applications: List[str] = []
    tags: List[str] = []
    
    related_context: Dict[str, Any] = {}
    outcome: Optional[str] = None
