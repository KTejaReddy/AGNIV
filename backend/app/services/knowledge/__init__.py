from app.core.logging import logger
from .manager import knowledge_manager
from .sources import knowledge_sources
from .search import knowledge_search

def register_knowledge_capabilities():
    logger.info("Initializing Knowledge Engine...")
    knowledge_sources.seed_initial_knowledge()
    logger.info("Knowledge Engine initialized successfully.")
