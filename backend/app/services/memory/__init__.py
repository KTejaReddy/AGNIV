import asyncio
from app.core.logging import logger
from .listener import memory_listener

def register_memory_engine():
    logger.info("Initializing Memory Engine...")
    asyncio.create_task(memory_listener.start())
    logger.info("Memory Engine initialized successfully.")
