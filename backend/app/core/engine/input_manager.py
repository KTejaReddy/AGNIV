from enum import Enum
from pydantic import BaseModel
from typing import Any, Dict
from app.core.logging import logger
from .event_bus import event_bus, Event
import uuid
import time

class InputType(str, Enum):
    VOICE = "VOICE"
    CAMERA = "CAMERA"
    SCREEN = "SCREEN"
    KEYBOARD = "KEYBOARD"
    MOUSE = "MOUSE"
    PLUGIN = "PLUGIN"
    REST = "REST"
    WEBSOCKET = "WEBSOCKET"
    MOBILE = "MOBILE"

class RawInput(BaseModel):
    id: str
    type: InputType
    payload: Dict[str, Any]
    source_id: str

class InputManager:
    async def route_input(self, input_type: InputType, payload: Dict[str, Any], source_id: str = "system"):
        raw_input = RawInput(
            id=str(uuid.uuid4()),
            type=input_type,
            payload=payload,
            source_id=source_id
        )
        logger.info(f"Input received: [{input_type.value}] {raw_input.id}")
        
        # Publish to Event Bus
        await event_bus.publish(Event(
            id=str(uuid.uuid4()),
            type="INPUT_RECEIVED",
            source="InputManager",
            payload=raw_input.dict(),
            timestamp=time.time()
        ))

    def route_input_threadsafe(self, input_type: InputType, payload: Dict[str, Any], source_id: str = "system"):
        raw_input = RawInput(
            id=str(uuid.uuid4()),
            type=input_type,
            payload=payload,
            source_id=source_id
        )
        logger.info(f"Input received (threadsafe): [{input_type.value}] {raw_input.id}")
        
        event_bus.publish_threadsafe(Event(
            id=str(uuid.uuid4()),
            type="INPUT_RECEIVED",
            source="InputManager",
            payload=raw_input.dict(),
            timestamp=time.time()
        ))
        
        # Future: Pass to Action Planner here via a direct call or let it subscribe to EVENT BUS
        # For this architecture, we let ActionPlanner subscribe to "INPUT_RECEIVED"

input_manager = InputManager()
