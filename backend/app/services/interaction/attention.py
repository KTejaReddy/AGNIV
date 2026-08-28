import time
import asyncio
import uuid
from app.core.engine import event_bus, Event
from app.core.logging import logger
from .session import interaction_session

class AttentionManager:
    def __init__(self):
        self.attention_timeout = 10.0

    async def handle_context(self, active_window: dict, faces: list, is_speaking: bool):
        """
        Determines attention based on multiple inputs.
        """
        previous_state = interaction_session.attention_state
        new_state = "UNKNOWN"
        
        if is_speaking:
            new_state = "TALKING"
        elif faces:
            # Simplistic check - if face is detected, assume looking at screen
            # (In a real phase, check head pose from mediapipe)
            new_state = "LOOKING_AT_SCREEN"
        else:
            new_state = "LOOKING_AWAY"
            
        if active_window and "Presentation" in active_window.get("title", ""):
            new_state = "BUSY_PRESENTING"
            
        if new_state != previous_state:
            interaction_session.attention_state = new_state
            logger.info(f"Attention State Changed: {new_state}")
            interaction_session.add_event("ATTENTION_CHANGED", {"state": new_state})
            await event_bus.publish(Event(
                id=str(uuid.uuid4()),
                type="ATTENTION_CHANGED",
                source="AttentionManager",
                payload={"state": new_state},
                timestamp=time.time()
            ))

attention_manager = AttentionManager()
