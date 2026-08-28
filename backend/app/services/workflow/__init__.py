import asyncio
from app.core.logging import logger
from .templates import load_default_templates
from .scheduler import workflow_scheduler

def register_workflow_engine():
    logger.info("Initializing Workflow Engine...")
    load_default_templates()
    asyncio.create_task(workflow_scheduler.start())
    logger.info("Workflow Engine initialized successfully.")
