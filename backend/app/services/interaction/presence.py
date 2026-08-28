import time
import asyncio
import uuid
from app.core.engine import event_bus, Event
from app.core.logging import logger
from .session import interaction_session

class PresenceManager:
    def __init__(self):
        self.last_seen_time = 0.0
        self.idle_threshold = 60.0 # seconds

    async def handle_face_event(self, event_data: dict):
        """
        Called when perception engine detects a face.
        """
        now = time.time()
        faces_detected = event_data.get("faces", [])
        
        is_present = len(faces_detected) > 0
        
        if is_present:
            if interaction_session.presence_state != "USER_ACTIVE":
                if now - self.last_seen_time > self.idle_threshold:
                    await self._emit("USER_RETURNED")
                else:
                    await self._emit("USER_ENTERED")
                    
                interaction_session.presence_state = "USER_ACTIVE"
            self.last_seen_time = now
        else:
            if interaction_session.presence_state == "USER_ACTIVE" and (now - self.last_seen_time > 5.0):
                interaction_session.presence_state = "USER_LEFT"
                await self._emit("USER_LEFT")

    async def _emit(self, state: str):
        logger.info(f"Presence State Changed: {state}")
        interaction_session.add_event(state, {})
        await event_bus.publish(Event(
            id=str(uuid.uuid4()),
            type=state,
            source="PresenceManager",
            payload={"timestamp": time.time()},
            timestamp=time.time()
        ))

presence_manager = PresenceManager()
