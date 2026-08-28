import uuid
from app.core.logging import logger
from .models import WorkflowInstance, WorkflowState
from .registry import workflow_registry
from .queue_manager import workflow_queue
from .validator import workflow_validator

class WorkflowManager:
    def __init__(self):
        pass

    def run_template(self, template_id: str):
        template = workflow_registry.get_template(template_id)
        if not template:
            logger.error(f"Template {template_id} not found.")
            return None
            
        instance_id = str(uuid.uuid4())
        instance = WorkflowInstance(
            id=template.id,
            name=template.name,
            description=template.description,
            goal=template.goal,
            steps=template.steps,
            instance_id=instance_id
        )
        
        is_valid, msg = workflow_validator.validate(instance)
        if not is_valid:
            return {"error": msg}
            
        workflow_queue.enqueue(instance)
        return {"instance_id": instance_id}

    def pause(self, instance_id: str):
        instance = workflow_queue.get_instance(instance_id)
        if instance and instance.state == WorkflowState.RUNNING:
            instance.state = WorkflowState.PAUSED
            return True
        return False
        
    def resume(self, instance_id: str):
        instance = workflow_queue.get_instance(instance_id)
        if instance and instance.state == WorkflowState.PAUSED:
            instance.state = WorkflowState.RUNNING
            return True
        return False

    def cancel(self, instance_id: str):
        instance = workflow_queue.get_instance(instance_id)
        if instance:
            instance.state = WorkflowState.CANCELLED
            return True
        return False

workflow_manager = WorkflowManager()
