from pydantic import BaseModel
from typing import Optional, List
from app.core.logging import logger

class VoiceSessionManager:
    def __init__(self):
        self.current_transcript: str = ""
        self.transcript_history: List[str] = []
        self.capabilities_executed: List[str] = []
        self.session_errors: List[str] = []
        
    def log_capability(self, capability: str):
        self.capabilities_executed.append(capability)
        if len(self.capabilities_executed) > 50:
            self.capabilities_executed.pop(0)
            
    def log_error(self, error: str):
        self.session_errors.append(error)
        if len(self.session_errors) > 50:
            self.session_errors.pop(0)
        
    def log(self, message: str):
        from app.services.runtime.controller import runtime_controller
        session_id = runtime_controller.session_id
        if session_id:
            logger.info(f"[{session_id}] {message}")
        else:
            logger.info(message)
            
    def append_transcript(self, text: str):
        self.current_transcript = text
        self.transcript_history.append(text)
        if len(self.transcript_history) > 100:
            self.transcript_history.pop(0)

voice_session = VoiceSessionManager()
