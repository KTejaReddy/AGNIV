from typing import Dict, Any, Optional
from enum import Enum
import uuid
import time
import asyncio
from app.core.logging import logger
from .event_bus import event_bus, Event

class TaskStatus(str, Enum):
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

class Task:
    def __init__(self, id: str, name: str, payload: Dict[str, Any], priority: int = 0):
        self.id = id
        self.name = name
        self.payload = payload
        self.priority = priority
        self.status = TaskStatus.QUEUED
        self.created_at = time.time()
        self.started_at: Optional[float] = None
        self.completed_at: Optional[float] = None
        
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status.value,
            "priority": self.priority,
            "duration": (self.completed_at - self.started_at) if self.completed_at and self.started_at else 0
        }

class TaskManager:
    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self._queue = asyncio.PriorityQueue()
        self._running = False

    async def initialize(self):
        self._running = True
        event_bus.subscribe("PLAN_CREATED", self.handle_plan_created)
        asyncio.create_task(self._worker())
        logger.info("Task Manager initialized")

    async def handle_plan_created(self, event: Event):
        plan_dict = event.payload
        logger.info(f"Task Manager received plan: {plan_dict.get('goal', 'Unnamed plan')}")
        await self.create_task(
            name=f"Execution plan: {plan_dict.get('goal', 'Unknown')}",
            payload={"plan": plan_dict}
        )

    async def create_task(self, name: str, payload: Dict[str, Any], priority: int = 0) -> str:
        task_id = str(uuid.uuid4())
        task = Task(id=task_id, name=name, payload=payload, priority=priority)
        self.tasks[task_id] = task
        await self._queue.put((-priority, task_id))
        
        await event_bus.publish(Event(
            id=str(uuid.uuid4()),
            type="TASK_CREATED",
            source="TaskManager",
            payload=task.to_dict(),
            timestamp=time.time()
        ))
        
        return task_id

    def list_tasks(self):
        return [task.to_dict() for task in self.tasks.values()]

    async def _worker(self):
        while self._running:
            try:
                _, task_id = await self._queue.get()
                task = self.tasks.get(task_id)
                if not task or task.status == TaskStatus.CANCELLED:
                    self._queue.task_done()
                    continue

                task.status = TaskStatus.RUNNING
                task.started_at = time.time()
                
                await event_bus.publish(Event(
                    id=str(uuid.uuid4()),
                    type="TASK_STARTED",
                    source="TaskManager",
                    payload=task.to_dict(),
                    timestamp=time.time()
                ))
                
                from .capability_manager import capability_manager
                from app.services.voice.session import voice_session
                from app.core.engine.action_planner import action_planner
                
                # runtime_controller handles state transitions
                
                plan_dict = task.payload.get("plan", {})
                steps = plan_dict.get("steps", [])
                reply = plan_dict.get("reply", "")
                
                task_failed = False
                failure_reason = ""
                
                for step_idx, step in enumerate(steps):
                    intent_name = step.get("capability", "UNKNOWN")
                    intent_params = step.get("params", {})
                    
                    voice_session.log(f"Capability: {intent_name}")
                    voice_session.capabilities_executed.append(intent_name)
                    logger.info(f"Executing step {step_idx + 1}/{len(steps)}: {intent_name}")
                    
                    success, result = await capability_manager.execute_capability(intent_name, intent_params)
                    
                    if not success:
                        task_failed = True
                        failure_reason = str(result)
                        voice_session.log(f"Error: {intent_name} failed: {failure_reason}")
                        voice_session.session_errors.append(f"{intent_name}: {failure_reason}")
                        logger.error(f"Task {task.id} failed at step {step_idx + 1} ({intent_name}): {failure_reason}")
                        # Inject the failure into the conversation memory
                        action_planner.conversation_history.append({
                            "role": "system",
                            "content": f"Action {intent_name} failed. Reason: {failure_reason}. Please explain the failure to the user and suggest what they can do next."
                        })
                        break
                
                task.completed_at = time.time()
                task.status = TaskStatus.FAILED if task_failed else TaskStatus.COMPLETED
                
                # Feedback loop
                if task_failed:
                    # Execute a fallback action planner run to generate explanation
                    from app.core.engine.input_manager import input_manager, InputType
                    # Trigger a silent internal voice routing to generate the spoken failure
                    input_manager.route_input_threadsafe(InputType.VOICE, {"text": f"Explain why {failure_reason} failed."})
                elif reply:
                    await capability_manager.execute_capability("SPEAK_TEXT", {"text": reply})
                    
                await event_bus.publish(Event(
                    id=str(uuid.uuid4()),
                    type="TASK_FINISHED" if not task_failed else "TASK_FAILED",
                    source="TaskManager",
                    payload={"task": task.to_dict(), "result": failure_reason if task_failed else "Success"},
                    timestamp=time.time()
                ))
                
                self._queue.task_done()
            except Exception as e:
                logger.error(f"Task worker error: {e}")

task_manager = TaskManager()
