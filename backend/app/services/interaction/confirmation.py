import time
import asyncio
import uuid
from app.core.engine import event_bus, Event
from app.core.logging import logger
from .session import interaction_session

class ConfirmationEngine:
    def __init__(self):
        pass

    async def request_confirmation(self, action: str, params: dict, source: str):
        conf_id = str(uuid.uuid4())
        interaction_session.pending_confirmations.append({
            "id": conf_id,
            "action": action,
            "params": params,
            "source": source,
            "timestamp": time.time()
        })
        
        logger.info(f"Confirmation requested for: {action}")
        interaction_session.add_event("CONFIRMATION_REQUESTED", {"action": action})
        
        await event_bus.publish(Event(
            id=conf_id,
            type="CONFIRMATION_REQUESTED",
            source="ConfirmationEngine",
            payload={"action": action, "params": params},
            timestamp=time.time()
        ))
        return conf_id

    async def resolve_confirmation(self, accepted: bool):
        if not interaction_session.pending_confirmations:
            return
            
        pending = interaction_session.pending_confirmations.pop(0)
        
        status_str = "ACCEPTED" if accepted else "REJECTED"
        logger.info(f"Confirmation {status_str} for: {pending['action']}")
        
        interaction_session.add_event("CONFIRMATION_RECEIVED", {"action": pending["action"], "accepted": accepted})
        
        await event_bus.publish(Event(
            id=str(uuid.uuid4()),
            type="CONFIRMATION_RECEIVED",
            source="ConfirmationEngine",
            payload={"original_request": pending, "accepted": accepted},
            timestamp=time.time()
        ))

confirmation_engine = ConfirmationEngine()
