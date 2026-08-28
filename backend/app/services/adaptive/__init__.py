import asyncio
from app.core.logging import logger
from .detector import pattern_detector

def register_adaptive_engine():
    logger.info("Initializing Adaptive Intelligence Engine...")
    asyncio.create_task(pattern_detector.start())
    logger.info("Adaptive Intelligence Engine initialized successfully.")
