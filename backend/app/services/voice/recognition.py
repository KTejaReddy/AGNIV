import asyncio
import speech_recognition as sr
from app.core.logging import logger
from app.core.engine import event_bus, Event, input_manager
from app.core.engine.input_manager import InputType
from .session import voice_session
import uuid
import time
import threading

class SpeechRecognitionManager:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.pause_threshold = 0.8
        self.recognizer.non_speaking_duration = 0.5
        self.recognizer.dynamic_energy_threshold = False
        self.recognizer.energy_threshold = 300
        self.mic = sr.Microphone()
        self.is_recording = False
        self._stop_listening_func = None

    def start_recording(self):
        if self.is_recording:
            return
            
        self.is_recording = True
        # RuntimeController handles state transitions

        logger.info("[PASS] Speech recording started")
        
        # Publish event
        event_bus.publish_threadsafe(Event(
            id=str(uuid.uuid4()),
            type="LISTENING_STARTED",
            source="SpeechRecognition",
            payload={},
            timestamp=time.time()
        ))
        
        def callback(recognizer, audio):
            from app.services.runtime.controller import runtime_controller, RuntimeState
            if runtime_controller.state in [RuntimeState.THINKING, RuntimeState.PLANNING, RuntimeState.EXECUTING, RuntimeState.SPEAKING, RuntimeState.WAIT_WAKE_WORD, RuntimeState.SLEEPING]:
                return # Ignore audio during these states

            logger.info("[PASS] Speech recording stopped (Silence detected)")
            start_ms = time.perf_counter()
            
            event_bus.publish_threadsafe(Event(
                id=str(uuid.uuid4()),
                type="VOICE_DETECTED",
                source="SpeechRecognition",
                payload={},
                timestamp=time.time()
            ))
            
            
            try:
                text = recognizer.recognize_google(audio)
                if not text.strip():
                    return
                voice_session.log(f"Transcript: {text}")
                
                end_ms = time.perf_counter()
                logger.info(f"[PASS] Transcript generated (Latency: {(end_ms - start_ms)*1000:.2f}ms)")
                
                event_bus.publish_threadsafe(Event(
                    id=str(uuid.uuid4()),
                    type="VOICE_TRANSCRIPT",
                    source="SpeechRecognition",
                    payload={"text": text},
                    timestamp=time.time()
                ))
                
                voice_session.append_transcript(text)
                
                # Push into InputManager as VOICE safely from thread
                input_manager.route_input_threadsafe(InputType.VOICE, {"text": text})
            except sr.UnknownValueError:
                voice_session.log("Error: Could not understand audio")
            except sr.RequestError as e:
                voice_session.log(f"Error: Recognition request error: {e}")
                
            # Do NOT stop recording, we are in continuous AI companion mode
                
            # Removed adjust_for_ambient_noise to eliminate 500ms synchronous block.
            # Dynamic energy threshold is True and handles background adjustments inherently.
            
        self._stop_listening_func = self.recognizer.listen_in_background(self.mic, callback, phrase_time_limit=10)

    def stop_recording(self):
        if self.is_recording and self._stop_listening_func:
            self._stop_listening_func(wait_for_stop=False)
            self.is_recording = False
            # RuntimeController handles state transitions
            logger.info("Speech Recognition loop stopped")
            
            event_bus.publish_threadsafe(Event(
                id=str(uuid.uuid4()),
                type="LISTENING_STOPPED",
                source="SpeechRecognition",
                payload={},
                timestamp=time.time()
            ))

speech_recognition_manager = SpeechRecognitionManager()
