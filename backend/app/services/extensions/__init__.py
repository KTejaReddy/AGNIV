from app.core.logging import logger
from .manager import extension_manager


def register_extension_sdk():
    logger.info("Initializing Extension SDK...")
    count = extension_manager.boot()
    logger.info(f"Extension SDK initialized. {count} extension(s) loaded.")
