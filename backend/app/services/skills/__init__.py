from app.core.logging import logger
from .builtins import load_builtins

def register_skills_engine():
    logger.info("Initializing Skills Engine...")
    load_builtins()
    logger.info("Skills Engine initialized successfully.")
