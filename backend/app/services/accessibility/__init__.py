import asyncio
from app.core.logging import logger
from .sign import sign_recognizer
from .captions import live_captions
from .gestures import gesture_confirmations

def register_accessibility_suite():
    logger.info("Initializing Accessibility Suite...")
    asyncio.create_task(sign_recognizer.start())
    asyncio.create_task(live_captions.start())
    asyncio.create_task(gesture_confirmations.start())
    logger.info("Accessibility Suite initialized successfully.")
