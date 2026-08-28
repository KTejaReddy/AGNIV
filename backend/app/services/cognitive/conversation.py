import uuid
import time
from typing import List, Dict, Any

class ConversationManager:
    def __init__(self):
        self.history: List[Dict[str, Any]] = []
    @property
    def session_id(self):
        from app.services.runtime.controller import runtime_controller
        return runtime_controller.session_id

    def add_message(self, role: str, content: str, hidden: bool = False):
        self.history.append({
            "id": str(uuid.uuid4()),
            "session_id": self.session_id,
            "role": role,
            "content": content,
            "hidden": hidden,
            "timestamp": time.time()
        })
        if len(self.history) > 50:
            self.history = self.history[-50:]
        
    def get_context(self, max_tokens: int = 4000):
        # Simplistic approach for now
        return self.history[-10:]
        
    def add_turn(self, user_text: str, ai_text: str):
        self.add_message("user", user_text)
        self.add_message("assistant", ai_text)
        
    def get_recent(self, limit: int = 10) -> List[Dict[str, Any]]:
        return self.history[-limit:]
        
    def clear(self):
        self.history = []

conversation_manager = ConversationManager()
