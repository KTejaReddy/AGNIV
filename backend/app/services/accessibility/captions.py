import time
from .manager import accessibility_manager
from app.core.engine.event_bus import event_bus, Event
from app.core.logging import logger

class LiveCaptionsManager:
    async def start(self):
        # Listen for TTS outputs or User Speech
        event_bus.subscribe("SPEECH_GENERATED", self._on_speech)
        event_bus.subscribe("VOICE_INPUT_RECEIVED", self._on_speech)
        logger.info("Live Captions Manager started")

    def _on_speech(self, event):
        if not accessibility_manager.get_settings().live_captions_enabled:
            return
            
        text = event.payload.get("text", "")
        if text:
            import asyncio
            try:
                loop = asyncio.get_running_loop()
                loop.create_task(self._publish_caption(text, event.source))
            except RuntimeError:
                pass

    async def _publish_caption(self, text: str, source: str):
        await event_bus.publish(Event(
            id=f"evt_{time.time()}",
            type="CAPTION_UPDATED",
            source="AccessibilitySuite",
            payload={"text": text, "speaker": source},
            timestamp=time.time()
        ))

live_captions = LiveCaptionsManager()
