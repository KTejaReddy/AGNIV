import time
import asyncio
import uuid
from app.core.engine import event_bus, Event, capability_manager
from app.core.logging import logger
from .session import interaction_session

class GreetingEngine:
    def __init__(self):
        self.last_greeting_time = 0.0
        self.greeting_cooldown = 300.0 # 5 minutes

    async def handle_trigger(self, trigger_type: str):
        now = time.time()
        if now - self.last_greeting_time < self.greeting_cooldown:
            return # Skip repetitive greetings
            
        greeting_text = "Hello!"
        
        if trigger_type == "USER_RETURNED":
            greeting_text = "Welcome back."
        elif trigger_type == "WAVE":
            hour = time.localtime().tm_hour
            if hour < 12:
                greeting_text = "Good morning."
            elif hour < 18:
                greeting_text = "Good afternoon."
            else:
                greeting_text = "Good evening."

        self.last_greeting_time = now
        logger.info(f"Greeting Triggered: {greeting_text}")
        
        interaction_session.add_event("GREETING_SENT", {"text": greeting_text})
        
        # Dispatch TTS
        capability_manager.get_capability("SPEAK_TEXT") # For logging purposes
        await event_bus.publish(Event(
            id=str(uuid.uuid4()),
            type="INTENT_EXECUTED", # Simulate routing to TTS
            source="GreetingEngine",
            payload={"action": "SPEAK_TEXT", "params": {"text": greeting_text}},
            timestamp=now
        ))

greeting_engine = GreetingEngine()
