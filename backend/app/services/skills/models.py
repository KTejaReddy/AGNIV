from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from enum import Enum

class SkillCategory(str, Enum):
    RESEARCH = "RESEARCH"
    PRODUCTIVITY = "PRODUCTIVITY"
    CODING = "CODING"
    ACCESSIBILITY = "ACCESSIBILITY"
    EDUCATION = "EDUCATION"
    SYSTEM = "SYSTEM"
    BROWSER = "BROWSER"
    FILES = "FILES"
    MEDIA = "MEDIA"
    UTILITIES = "UTILITIES"
    COMMUNICATION = "COMMUNICATION"

class SkillManifest(BaseModel):
    id: str
    name: str
    description: str
    version: str = "1.0.0"
    author: str = "AGNIV Built-in"
    category: SkillCategory
    tags: List[str] = []
    icon: str = "box"
    
    permissions: List[str] = []
    required_capabilities: List[str] = []
    required_workflows: List[str] = []
    required_knowledge: List[str] = []
    
    # Internal representation of execution steps
    workflow_template_id: Optional[str] = None
    
    is_enabled: bool = True
