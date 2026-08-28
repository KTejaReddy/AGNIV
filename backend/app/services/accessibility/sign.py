import time
from .manager import accessibility_manager
from .models import SignData
from app.core.engine.event_bus import event_bus, Event
from app.core.logging import logger

class SignLanguageRecognizer:
    def __init__(self):
        # Basic mapping of gestures to signs
        self.dictionary = {
            "palm_open": "Hello",
            "thumbs_up": "Yes",
            "thumbs_down": "No",
            "peace_sign": "Peace",
            "fist": "Stop"
        }
        self.recognized_signs = []

    async def start(self):
        event_bus.subscribe("PERCEPTION_GESTURE", self._on_gesture)
        logger.info("Sign Language Recognizer started")

    def _on_gesture(self, event):
        if not accessibility_manager.get_settings().sign_recognition_enabled:
            return
            
        gesture = event.payload.get("gesture")
        if gesture in self.dictionary:
            sign_name = self.dictionary[gesture]
            sign = SignData(sign_name=sign_name, confidence=0.9, timestamp=time.time())
            self.recognized_signs.append(sign)
            
            # Publish it for UI and optional TTS
            import asyncio
            try:
                loop = asyncio.get_running_loop()
                loop.create_task(self._publish_sign(sign))
            except RuntimeError:
                pass

    async def _publish_sign(self, sign: SignData):
        await event_bus.publish(Event(
            id=f"evt_{time.time()}",
            type="SIGN_RECOGNIZED",
            source="AccessibilitySuite",
            payload=sign.dict(),
            timestamp=time.time()
        ))

    def get_history(self):
        return self.recognized_signs

sign_recognizer = SignLanguageRecognizer()
