import time
import asyncio
import uuid
from app.core.engine import event_bus, Event, capability_manager
from app.core.logging import logger
from .session import interaction_session

class NotificationManager:
    def __init__(self):
        pass

    async def deliver(self, message: str, priority: str = "NORMAL"):
        attention = interaction_session.attention_state
        mode = "SILENT"
        
        # Route based on attention
        if attention == "BUSY_PRESENTING":
            mode = "DEFERRED"
        elif attention == "LOOKING_AWAY":
            mode = "VOICE"
        else:
            mode = "POPUP"
            
        if priority == "HIGH":
            mode = "IMMEDIATE_VOICE"
            
        interaction_session.notification_mode = mode
        logger.info(f"Notification routed via {mode}: {message}")
        
        interaction_session.add_event("NOTIFICATION_DELIVERED", {"message": message, "mode": mode})
        
        if "VOICE" in mode:
            await event_bus.publish(Event(
                id=str(uuid.uuid4()),
                type="INTENT_EXECUTED", # Simulating routing to Voice
                source="NotificationManager",
                payload={"action": "SPEAK_TEXT", "params": {"text": message}},
                timestamp=time.time()
            ))

notification_manager = NotificationManager()
