import asyncio
from app.core.engine import event_bus
from app.core.logging import logger
from .presence import presence_manager
from .attention import attention_manager
from .greeting import greeting_engine
from .rules import interaction_rules
from .confirmation import confirmation_engine

class InteractionManager:
    def __init__(self):
        self.running = False

    async def start(self):
        self.running = True
        event_bus.subscribe("PERCEPTION_EVENT", self.handle_perception_event)
        event_bus.subscribe("WINDOW_CHANGED", self.handle_window_event)
        event_bus.subscribe("WAKE_WORD_DETECTED", self.handle_wake_word_event)
        event_bus.subscribe("TTS_FINISHED", self.handle_tts_completed)
        logger.info("Interaction Manager started.")

    async def handle_tts_completed(self, event):
        from app.services.voice.recognition import speech_recognition_manager
        from app.services.voice.session import voice_session
        
        # If we are supposed to be active, ensure listening is restarted
        if speech_recognition_manager.is_recording:
            logger.info("[InteractionManager] TTS_FINISHED received. Continuous listening handled by RuntimeController.")

    async def handle_wake_word_event(self, event):
        from app.services.voice.recognition import speech_recognition_manager
        from app.services.voice.wake_word import wake_word_manager
        from app.services.voice.session import voice_session
        # runtime_controller handles state transitions
        voice_session.log("Wake word detected")

    async def handle_perception_event(self, event):
        payload = event.payload
        
        # 1. Update Presence
        await presence_manager.handle_face_event(payload)
        
        # 2. Update Attention
        # (Mocking active window/voice for now, would pull from state in real impl)
        await attention_manager.handle_context(None, payload.get("faces", []), False)
        
        # 3. Check Gestures against Rules
        gestures = payload.get("gestures", [])
        for g in gestures:
            name = g.get("name")
            if name:
                rule_intent = interaction_rules.evaluate_gesture(name)
                
                if rule_intent == "WAVE_GREETING":
                    await greeting_engine.handle_trigger("WAVE")
                elif rule_intent == "CONFIRM_ACCEPT":
                    await confirmation_engine.resolve_confirmation(True)
                elif rule_intent == "CONFIRM_REJECT":
                    await confirmation_engine.resolve_confirmation(False)

    async def handle_window_event(self, event):
        payload = event.payload
        # Re-eval attention based on new window
        await attention_manager.handle_context(payload.get("window"), [], False)

interaction_manager = InteractionManager()
