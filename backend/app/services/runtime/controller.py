import asyncio
import time
import uuid
from typing import Dict, Any, Optional
from app.core.logging import logger
from app.core.engine.event_bus import event_bus, Event
from app.core.engine.supervisor import supervisor

from app.services.voice.wake_word import wake_word_manager
from app.services.voice.recognition import speech_recognition_manager

class RuntimeState:
    SLEEPING = "SLEEPING"
    WAIT_WAKE_WORD = "WAIT_WAKE_WORD"
    LISTENING = "LISTENING"
    THINKING = "THINKING"
    PLANNING = "PLANNING"
    EXECUTING = "EXECUTING"
    SPEAKING = "SPEAKING"
    ERROR = "ERROR"

class RuntimeController:
    def __init__(self):
        self.state: str = RuntimeState.WAIT_WAKE_WORD
        self.is_running: bool = False
        self.presence: str = "active"
        self.session_id: str = str(uuid.uuid4())
        
    async def start(self):
        logger.info("[RuntimeController] Starting central orchestration layer.")
        self.is_running = True
        
        event_bus.subscribe("WAKE_WORD_DETECTED", self._on_wake_word)
        event_bus.subscribe("VOICE_TRANSCRIPT", self._on_voice_transcript)
        event_bus.subscribe("PLAN_CREATED", self._on_plan_created)
        event_bus.subscribe("TASK_STARTED", self._on_task_started)
        event_bus.subscribe("TASK_FINISHED", self._on_task_finished)
        event_bus.subscribe("TASK_FAILED", self._on_task_finished)
        event_bus.subscribe("TTS_STARTED", self._on_tts_started)
        event_bus.subscribe("TTS_FINISHED", self._on_tts_finished)
        
        await self._set_state(RuntimeState.WAIT_WAKE_WORD, "STARTUP")
        
        while self.is_running:
            await asyncio.sleep(1.0)
            
    async def _set_state(self, new_state: str, trigger_event: str):
        if self.state != new_state:
            prev_state = self.state
            self.state = new_state
            
            # Map events to their actual publishers and subscribers based on our architecture
            publisher_map = {
                "WAKE_WORD_DETECTED": "WakeWordManager.start_listening()",
                "VOICE_TRANSCRIPT": "SpeechRecognitionManager.start_recording()",
                "PLAN_CREATED": "ActionPlanner.handle_input_event()",
                "TASK_STARTED": "TaskManager._worker()",
                "TASK_FINISHED": "TaskManager._worker()",
                "TASK_FAILED": "TaskManager._worker()",
                "TTS_STARTED": "TTSManager._worker()",
                "TTS_FINISHED": "TTSManager._worker()"
            }
            
            subscriber_map = {
                "WAKE_WORD_DETECTED": "RuntimeController._on_wake_word()",
                "VOICE_TRANSCRIPT": "RuntimeController._on_voice_transcript()",
                "PLAN_CREATED": "RuntimeController._on_plan_created()",
                "TASK_STARTED": "RuntimeController._on_task_started()",
                "TASK_FINISHED": "RuntimeController._on_task_finished()",
                "TASK_FAILED": "RuntimeController._on_task_finished()",
                "TTS_STARTED": "RuntimeController._on_tts_started()",
                "TTS_FINISHED": "RuntimeController._on_tts_finished()"
            }
            
            publisher = publisher_map.get(trigger_event, "UnknownPublisher")
            subscriber = subscriber_map.get(trigger_event, "UnknownSubscriber")
            
            log_message = (
                f"\n[RUNTIME]\n"
                f"{prev_state} -> {self.state}\n"
                f"Event: {trigger_event}\n"
                f"Timestamp: {time.time()}\n"
                f"Session ID: {self.session_id}\n"
                f"Publisher:\n{publisher}\n"
                f"Subscriber:\n{subscriber}\n"
            )
            
            print(log_message)
            logger.info(log_message)
            
            # Enforce state rules for peripherals
            if self.state == RuntimeState.WAIT_WAKE_WORD:
                self.session_id = str(uuid.uuid4()) # New session on sleep
                speech_recognition_manager.stop_recording()
                wake_word_manager.start_listening()
            elif self.state == RuntimeState.LISTENING:
                wake_word_manager.stop_listening()
                # Yield to let PyAudio cleanly release the audio device
                await asyncio.sleep(0.1)
                speech_recognition_manager.start_recording()
            elif self.state in [RuntimeState.THINKING, RuntimeState.PLANNING, RuntimeState.EXECUTING, RuntimeState.SPEAKING]:
                # Do NOT stop recording; let the speech recognition callback ignore audio.
                wake_word_manager.stop_listening()

            await event_bus.publish(Event(
                id=f"state_{time.time()}",
                type="RUNTIME_STATE_CHANGE",
                source="RuntimeController",
                payload={"state": self.state},
                timestamp=time.time()
            ))

    async def _on_wake_word(self, event: Event):
        if self.state == RuntimeState.WAIT_WAKE_WORD:
            await self._set_state(RuntimeState.LISTENING, "WAKE_WORD_DETECTED")
            
    async def _on_voice_transcript(self, event: Event):
        text = event.payload.get("text", "").lower()
        if "go to sleep" in text:
            await self._set_state(RuntimeState.WAIT_WAKE_WORD, "VOICE_TRANSCRIPT")
            
            # Clear short-term conversation context when going to sleep
            try:
                from app.core.engine.action_planner import action_planner
                action_planner.conversation_history.clear()
                logger.info("Short-term conversation memory cleared.")
            except Exception as e:
                logger.error(f"Error clearing conversation history: {e}")
            return
            
        if self.state == RuntimeState.LISTENING:
            await self._set_state(RuntimeState.THINKING, "VOICE_TRANSCRIPT")
            
    async def _on_plan_created(self, event: Event):
        if self.state == RuntimeState.THINKING:
            await self._set_state(RuntimeState.PLANNING, "PLAN_CREATED")
        
    async def _on_task_started(self, event: Event):
        await self._set_state(RuntimeState.EXECUTING, "TASK_STARTED")
        
    async def _on_task_finished(self, event: Event):
        # We wait for TTS to start, or if there's no reply, we go back to listening
        # We don't transition here unless we know TTS won't happen.
        # But for exhaustive logging, we could transition to a brief state, or just wait.
        pass

    async def _on_tts_started(self, event: Event):
        await self._set_state(RuntimeState.SPEAKING, "TTS_STARTED")

    async def _on_tts_finished(self, event: Event):
        if self.state == RuntimeState.SPEAKING:
            await self._set_state(RuntimeState.LISTENING, "TTS_FINISHED")

runtime_controller = RuntimeController()
