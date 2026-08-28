import time
from typing import Dict, Any

class ScreenSessionManager:
    def __init__(self):
        self.active = False
        self.current_monitor = 1
        self.fps = 0
        self.latency = 0
        
        self.state: Dict[str, Any] = {
            "active_window": None,
            "ocr_results": None,
            "ui_tree": None,
            "notifications": []
        }
        
    def get_status(self):
        return {
            "active": self.active,
            "current_monitor": self.current_monitor,
            "fps": self.fps,
            "latency": self.latency,
            "state": self.state
        }
        
    def update_state(self, key: str, value: Any):
        self.state[key] = value

screen_session = ScreenSessionManager()
