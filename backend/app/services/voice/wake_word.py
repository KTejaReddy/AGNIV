import asyncio
import speech_recognition as sr
from app.core.logging import logger
from app.core.engine import event_bus, Event
from .session import voice_session
import uuid
import time
import threading

import difflib

def is_wake_word_fuzzy(text, wake_words, threshold=0.75):
    text_words = text.split()
    for ww in wake_words:
        ww_len = len(ww.split())
        for i in range(len(text_words) - ww_len + 1):
            ngram = " ".join(text_words[i:i+ww_len])
            ratio = difflib.SequenceMatcher(None, ww, ngram).ratio()
            if ratio >= threshold:
                return ww
    return None

class WakeWordManager:
    def __init__(self):
        self.wake_words = ["hey agniv", "agniv"]
        self.recognizer = sr.Recognizer()
        self.recognizer.pause_threshold = 0.8
        self.recognizer.non_speaking_duration = 0.5
        self.recognizer.dynamic_energy_threshold = False
        self.recognizer.energy_threshold = 300
        self.mic = None
        self.is_listening = False
        self._stop_listening_func = None

    def start_listening(self):
        if self.is_listening:
            return
            
        self.is_listening = True
        logger.info(f"[PASS] WakeWordManager started")
        
        try:
            self.mic = sr.Microphone()
            with self.mic as source:
                logger.info(f"[PASS] Microphone initialized")
                
                device_index = self.mic.device_index
                sample_rate = getattr(self.mic, 'SAMPLE_RATE', 'Unknown')
                channels = 1
                chunk = getattr(self.mic, 'CHUNK', 'Unknown')
                
                logger.info(f"Selected microphone: Index {device_index}")
                logger.info(f"Sample rate: {sample_rate}")
                logger.info(f"Channels: {channels}")
                logger.info(f"Chunk size: {chunk}")
                
                if hasattr(source, 'stream') and source.stream:
                    try:
                        buffer = source.stream.read(self.mic.CHUNK)
                        if len(buffer) > 0:
                            logger.info("[PASS] Audio stream active (chunks arriving)")
                        else:
                            logger.error("Audio buffer empty!")
                    except Exception as e:
                        logger.error(f"Failed to read chunk: {e}")
                else:
                    logger.info("[PASS] Audio stream initialized")

                logger.info("Adjusting for ambient noise (wait 1 sec)...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
        except Exception as e:
            logger.error(f"[FAIL] Microphone initialization failed: {e}")
            self.is_listening = False
            return
        
        def callback(recognizer, audio):
            from app.services.runtime.controller import runtime_controller, RuntimeState
            if runtime_controller.state not in [RuntimeState.SLEEPING, RuntimeState.WAIT_WAKE_WORD]:
                return # Ignore audio during active conversations
                
            start_ms = time.perf_counter()
            logger.info("[PASS] Audio packet received (Voice activity detected)")
            
            try:
                import audioop
                raw_data = audio.get_raw_data()
                rms = audioop.rms(raw_data, audio.sample_width)
                duration = len(raw_data) / (audio.sample_rate * audio.sample_width)
                logger.info(f"[MIC METRICS] RMS: {rms} | Energy Threshold: {recognizer.energy_threshold} | Duration: {duration:.2f}s")
            except Exception as e:
                pass
                
            try:
                text = recognizer.recognize_google(audio).lower()
                logger.info(f"Recognized transcript: '{text}'")
                
                matched_ww = is_wake_word_fuzzy(text, self.wake_words)
                if matched_ww:
                    end_ms = time.perf_counter()
                    logger.info(f"[PASS] Wake word detected: {matched_ww} (Fuzzy Match, Latency: {(end_ms - start_ms)*1000:.2f}ms)")
                    event_bus.publish_threadsafe(Event(
                        id=str(uuid.uuid4()),
                        type="WAKE_WORD_DETECTED",
                        source="WakeWordManager",
                        payload={"text": text},
                        timestamp=time.time()
                    ))
                else:
                    logger.info(f"Reason for rejection: Transcript '{text}' did not contain {self.wake_words} even with fuzzy matching")
            except sr.UnknownValueError:
                logger.info("Reason for rejection: Could not understand audio (Silence/Noise)")
            except sr.RequestError as e:
                logger.error(f"Reason for rejection: API error {e}")
                
        self._stop_listening_func = self.recognizer.listen_in_background(self.mic, callback, phrase_time_limit=3)
        logger.info("[PASS] Listening thread running")
        logger.info("[PASS] Loop active")

    def stop_listening(self):
        if self.is_listening and self._stop_listening_func:
            self._stop_listening_func(wait_for_stop=False)
            self.is_listening = False
            logger.info("Wake Word Manager stopped listening")

wake_word_manager = WakeWordManager()
