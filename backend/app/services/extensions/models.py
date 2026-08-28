from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from enum import Enum
import uuid


class ExtensionType(str, Enum):
    CAPABILITY = "capability"
    SKILL = "skill"
    WORKFLOW_PACK = "workflow_pack"
    INTEGRATION = "integration"
    UI_PANEL = "ui_panel"
    ACCESSIBILITY_PACK = "accessibility_pack"


class ExtensionStatus(str, Enum):
    INSTALLED = "installed"
    ENABLED = "enabled"
    DISABLED = "disabled"
    ERROR = "error"
    PENDING = "pending"


class Permission(str, Enum):
    FILE_READ = "file.read"
    FILE_WRITE = "file.write"
    NETWORK = "network"
    DESKTOP = "desktop"
    VOICE = "voice"
    SCREEN = "screen"
    PERCEPTION = "perception"
    MEMORY = "memory"
    WORKFLOW = "workflow"
    SKILLS = "skills"
    KNOWLEDGE = "knowledge"
    COGNITIVE = "cognitive"


class ExtensionDependency(BaseModel):
    name: str
    min_version: Optional[str] = None
    max_version: Optional[str] = None


class ExtensionAuthor(BaseModel):
    name: str
    email: Optional[str] = None
    url: Optional[str] = None


class ExtensionManifest(BaseModel):
    """The agniv-extension.json manifest schema."""
    id: str
    name: str
    version: str
    type: ExtensionType
    description: str
    author: ExtensionAuthor
    agniv_version: str = ">=1.0.0"
    entry_point: str = "main.py"
    permissions: List[Permission] = []
    dependencies: List[ExtensionDependency] = []
    tags: List[str] = []
    homepage: Optional[str] = None
    license: Optional[str] = "MIT"


class ExtensionRecord(BaseModel):
    """Runtime state of a loaded extension."""
    id: str
    manifest: ExtensionManifest
    status: ExtensionStatus = ExtensionStatus.INSTALLED
    path: str
    error: Optional[str] = None
    metadata: Dict[str, Any] = {}
