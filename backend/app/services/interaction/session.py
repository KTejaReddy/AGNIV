from typing import Dict, Any, List

class InteractionSessionManager:
    def __init__(self):
        self.presence_state = "UNKNOWN"
        self.attention_state = "UNKNOWN"
        self.last_interaction = 0.0
        self.pending_confirmations = []
        self.recent_events = []
        self.notification_mode = "IMMEDIATE"

    def add_event(self, event_type: str, payload: dict):
        self.recent_events.append({
            "type": event_type,
            "payload": payload
        })
        if len(self.recent_events) > 50:
            self.recent_events.pop(0)

    def get_status(self) -> Dict[str, Any]:
        return {
            "presence": self.presence_state,
            "attention": self.attention_state,
            "last_interaction": self.last_interaction,
            "pending_confirmations": self.pending_confirmations,
            "notification_mode": self.notification_mode,
            "events": self.recent_events
        }

interaction_session = InteractionSessionManager()
