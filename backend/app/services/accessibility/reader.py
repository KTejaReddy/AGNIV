import time
from .manager import accessibility_manager
from app.core.engine.event_bus import event_bus, Event
from app.core.engine.capability_manager import capability_manager
from app.core.logging import logger

class ScreenReader:
    def __init__(self):
        self.is_reading = False

    async def read_window(self):
        if not accessibility_manager.get_settings().screen_reader_enabled:
            return "Screen reader is disabled in current profile."

        # Fetch active window via screen capability
        try:
            window_info = capability_manager.execute("READ_ACTIVE_WINDOW", {})
            title = window_info.get("title", "Unknown Window")
            text = f"Active window is {title}."
            
            # Pipe directly to Voice TTS
            capability_manager.execute("SPEAK_TEXT", {"text": text})
            
            await event_bus.publish(Event(
                id=f"evt_{time.time()}",
                type="SCREEN_READING_STARTED",
                source="AccessibilitySuite",
                payload={"target": "window", "content": text},
                timestamp=time.time()
            ))
            return text
        except Exception as e:
            logger.error(f"Screen reader failed: {e}")
            return "Could not read window."

screen_reader = ScreenReader()
