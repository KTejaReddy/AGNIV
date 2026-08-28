from pydantic import BaseModel
from typing import Dict, Any

class PerceptionSessionManager:
    def __init__(self):
        self.active_trackers = {
            "hands": False,
            "face": False,
            "body": False,
            "gestures": False
        }
        self.capture_fps = 0.0
        self.mediapipe_fps = 0.0
        self.render_fps = 0.0
        self.latency = 0
        self.current_state: Dict[str, Any] = {
            "gesture": None,
            "face_state": None,
            "body_state": None
        }

    def set_tracker_state(self, tracker: str, enabled: bool):
        if tracker in self.active_trackers:
            self.active_trackers[tracker] = enabled

    def get_status(self):
        return {
            "trackers": self.active_trackers,
            "capture_fps": self.capture_fps,
            "mediapipe_fps": self.mediapipe_fps,
            "render_fps": self.render_fps,
            "latency": self.latency,
            "state": self.current_state
        }
        
    def update_state(self, key: str, value: Any):
        self.current_state[key] = value

perception_session = PerceptionSessionManager()
