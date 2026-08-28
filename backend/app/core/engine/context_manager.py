from typing import Dict, Any
from app.core.logging import logger

class ContextManager:
    def __init__(self):
        self.state: Dict[str, Any] = {
            "current_user": "system",
            "current_workspace": "default",
            "current_window": None,
            "current_mode": "idle",
            "active_plugins": []
        }

    async def initialize(self):
        logger.info("Context Manager initialized")

    def update_context(self, key: str, value: Any):
        self.state[key] = value
        
    def get_context(self) -> Dict[str, Any]:
        return self.state

context_manager = ContextManager()
