from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from enum import Enum

class WorkflowState(str, Enum):
    PENDING = "PENDING"
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    WAITING_FOR_PERMISSION = "WAITING_FOR_PERMISSION"
    WAITING_FOR_USER = "WAITING_FOR_USER"
    RETRYING = "RETRYING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

class StepState(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"

class WorkflowStep(BaseModel):
    id: str
    capability: str
    parameters: Dict[str, Any] = {}
    timeout: int = 30
    retry_count: int = 0
    depends_on: List[str] = []
    
    # State tracking
    state: StepState = StepState.PENDING
    result: Optional[Any] = None
    error: Optional[str] = None
    start_time: Optional[float] = None
    end_time: Optional[float] = None

class WorkflowDefinition(BaseModel):
    id: str
    name: str
    description: str
    goal: str
    steps: List[WorkflowStep]
    
class WorkflowInstance(WorkflowDefinition):
    instance_id: str
    state: WorkflowState = WorkflowState.PENDING
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    current_step_id: Optional[str] = None
    progress: float = 0.0
