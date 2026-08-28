from app.core.engine.event_bus import event_bus
from app.core.logging import logger
from .manager import memory_manager
from .models import MemoryItem, MemoryType, Importance
import json

class MemoryListener:
    async def start(self):
        # We listen to WORKFLOW_COMPLETED, SKILL_COMPLETED events
        event_bus.subscribe("WORKFLOW_COMPLETED", self.on_workflow_completed)
        event_bus.subscribe("SKILL_COMPLETED", self.on_skill_completed)
        
    async def on_workflow_completed(self, event):
        payload = event.payload
        memory_manager.create_memory(MemoryItem(
            title=f"Workflow Executed: {payload.get('template_id', 'Unknown')}",
            summary="System automatically ran a workflow.",
            type=MemoryType.WORKFLOW_HISTORY,
            source="WorkflowEngine",
            related_workflows=[payload.get("template_id")],
            outcome=payload.get("status")
        ))
        
    async def on_skill_completed(self, event):
        payload = event.payload
        memory_manager.create_memory(MemoryItem(
            title=f"Skill Executed: {payload.get('skill_id', 'Unknown')}",
            summary="User invoked a semantic skill.",
            type=MemoryType.SKILL_USAGE,
            source="SkillsEngine",
            related_skills=[payload.get("skill_id")],
            outcome=payload.get("status")
        ))

memory_listener = MemoryListener()
