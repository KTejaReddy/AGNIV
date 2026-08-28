from app.core.engine.capability_manager import capability_manager
from app.core.logging import logger
from .wake_word import wake_word_manager
from .recognition import speech_recognition_manager
from .tts import tts_manager
from .session import voice_session

async def start_listening_cap(params):
    speech_recognition_manager.start_recording()
    return {"status": "success"}

async def stop_listening_cap(params):
    speech_recognition_manager.stop_recording()
    wake_word_manager.start_listening()
    return {"status": "success"}

async def speak_text_cap(params):
    text = params.get("text")
    tts_manager.speak(text)
    return {"status": "success"}

async def cancel_speech_cap(params):
    tts_manager.cancel()
    return {"status": "success"}

async def mute_voice_cap(params):
    # runtime_controller handles state transitions
    return {"status": "success"}

async def unmute_voice_cap(params):
    # runtime_controller handles state transitions
    return {"status": "success"}

def register_voice_capabilities():
    logger.info("Starting voice background services...")
    tts_manager.start()
    
    # Start wake word listening automatically for MVP stabilization
    logger.info("Starting Wake Word Manager...")
    wake_word_manager.start_listening()

    logger.info("Registering Voice Capabilities...")
    capability_manager.register_capability("START_LISTENING", "1.0", "Starts microphone listening", start_listening_cap)
    capability_manager.register_capability("STOP_LISTENING", "1.0", "Stops microphone listening", stop_listening_cap)
    capability_manager.register_capability("SPEAK_TEXT", "1.0", "Speaks text out loud", speak_text_cap)
    capability_manager.register_capability("CANCEL_SPEECH", "1.0", "Cancels ongoing speech", cancel_speech_cap)
    capability_manager.register_capability("MUTE_VOICE", "1.0", "Mutes voice input", mute_voice_cap)
    capability_manager.register_capability("UNMUTE_VOICE", "1.0", "Unmutes voice input", unmute_voice_cap)
    logger.info("Voice Capabilities registered successfully.")
