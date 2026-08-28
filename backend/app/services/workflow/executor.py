import asyncio
import time
from app.core.logging import logger
from app.core.engine.capability_manager import capability_manager
from app.core.engine import event_bus, Event
from .models import WorkflowInstance, WorkflowState, StepState

class WorkflowExecutor:
    async def execute(self, instance: WorkflowInstance):
        logger.info(f"Starting execution of workflow {instance.instance_id}")
        instance.state = WorkflowState.RUNNING
        instance.start_time = time.time()
        
        await event_bus.publish(Event(id=instance.instance_id, type="WORKFLOW_STARTED", source="WorkflowEngine", payload={"id": instance.instance_id}, timestamp=time.time()))

        total_steps = len(instance.steps)
        
        for i, step in enumerate(instance.steps):
            if instance.state == WorkflowState.CANCELLED:
                logger.info(f"Workflow {instance.instance_id} was cancelled.")
                break
                
            while instance.state == WorkflowState.PAUSED:
                await asyncio.sleep(1)
                
            instance.current_step_id = step.id
            step.state = StepState.RUNNING
            step.start_time = time.time()
            
            await event_bus.publish(Event(id=step.id, type="WORKFLOW_STEP_STARTED", source="WorkflowEngine", payload={"workflow_id": instance.instance_id, "step_id": step.id}, timestamp=time.time()))
            
            logger.info(f"Executing step {step.id}: {step.capability}")
            
            try:
                # Direct CapabilityManager call inside execution loop. 
                # (Permissions handled inside capability_manager.execute_capability)
                success, result = await capability_manager.execute_capability(step.capability, step.parameters)
                
                if success:
                    step.state = StepState.COMPLETED
                    step.result = result
                    logger.info(f"Step {step.id} completed successfully.")
                else:
                    step.state = StepState.FAILED
                    step.error = result
                    logger.error(f"Step {step.id} failed: {result}")
                    instance.state = WorkflowState.FAILED
                    break
                    
            except Exception as e:
                step.state = StepState.FAILED
                step.error = str(e)
                instance.state = WorkflowState.FAILED
                break
                
            step.end_time = time.time()
            instance.progress = ((i + 1) / total_steps) * 100
            
            await event_bus.publish(Event(id=step.id, type="WORKFLOW_STEP_COMPLETED", source="WorkflowEngine", payload={"workflow_id": instance.instance_id, "step_id": step.id, "success": step.state == StepState.COMPLETED}, timestamp=time.time()))

        if instance.state == WorkflowState.RUNNING:
            instance.state = WorkflowState.COMPLETED
            instance.progress = 100.0
            
        instance.end_time = time.time()
        
        final_event = "WORKFLOW_COMPLETED" if instance.state == WorkflowState.COMPLETED else "WORKFLOW_FAILED"
        await event_bus.publish(Event(id=instance.instance_id, type=final_event, source="WorkflowEngine", payload={"id": instance.instance_id}, timestamp=time.time()))

workflow_executor = WorkflowExecutor()
