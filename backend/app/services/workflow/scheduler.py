import asyncio
from app.core.logging import logger
from .queue_manager import workflow_queue
from .executor import workflow_executor

class WorkflowScheduler:
    def __init__(self):
        self.running = False

    async def start(self):
        self.running = True
        logger.info("Workflow Scheduler started.")
        while self.running:
            # Simple single-worker loop for Phase 10
            instance = workflow_queue.dequeue()
            if instance:
                workflow_queue.add_active(instance)
                # Fire and forget execution task so we can process multiple workflows if needed
                asyncio.create_task(self._run_wrapper(instance))
            await asyncio.sleep(1)

    async def _run_wrapper(self, instance):
        await workflow_executor.execute(instance)
        # In a more robust system, we would move to a history archive instead of just removing
        workflow_queue.remove_active(instance.instance_id)

workflow_scheduler = WorkflowScheduler()
