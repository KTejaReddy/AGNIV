import pyttsx3
import queue
import threading
import asyncio
from app.core.logging import logger
from app.core.engine import event_bus, Event
from .session import voice_session
import uuid
import time

class TTSManager:
    def __init__(self):
        self._queue = queue.Queue()
        self._running = False
        self._thread = None
        
    def start(self):
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._worker, daemon=True)
        self._thread.start()
        logger.info("TTS Manager started")

    def _worker(self):
        try:
            import pythoncom
            pythoncom.CoInitialize()
        except ImportError:
            pass
            
        import win32com.client
        try:
            speaker = win32com.client.Dispatch("SAPI.SpVoice")
            speaker.Rate = 2 # equivalent to 150 words per minute (range is -10 to 10)
        except Exception as e:
            logger.error(f"Failed to initialize SAPI.SpVoice: {e}")
            return
            
        while self._running:
            try:
                text = self._queue.get(timeout=1)
                logger.info("[TTS] TTS_QUEUE_RECEIVED")
                
                event_bus.publish_threadsafe(Event(
                        id=str(uuid.uuid4()),
                        type="TTS_STARTED",
                        source="TTSManager",
                        payload={"text": text},
                        timestamp=time.time()
                    ))
                
                voice_session.log(f"TTS Started: {text[:20]}...")
                try:
                    speaker.Speak(text)
                except Exception as e:
                    logger.error(f"SAPI Speak error: {e}")
                voice_session.log("TTS Finished")
                
                event_bus.publish_threadsafe(Event(
                        id=str(uuid.uuid4()),
                        type="TTS_FINISHED",
                        source="TTSManager",
                        payload={},
                        timestamp=time.time()
                    ))
                self._queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"TTS error: {e}")

    def speak(self, text: str):
        self._queue.put(text)
        
    def cancel(self):
        # pyttsx3 doesn't easily cancel running speech without killing processes.
        # But we can clear the queue.
        with self._queue.mutex:
            self._queue.queue.clear()
        
    def get_voices(self):
        import win32com.client
        try:
            speaker = win32com.client.Dispatch("SAPI.SpVoice")
            voices = speaker.GetVoices()
            return [{"id": str(i), "name": voices.Item(i).GetDescription()} for i in range(voices.Count)]
        except Exception:
            return []

tts_manager = TTSManager()
