from fastapi import APIRouter
from typing import Any, Dict
from app.services.voice.session import voice_session
from app.services.voice.tts import tts_manager
from app.core.engine.input_manager import input_manager, InputType
import speech_recognition as sr

router = APIRouter()

@router.get("/status")
def get_voice_status():
    from app.services.runtime.controller import runtime_controller
    return {
        "state": runtime_controller.state,
        "transcript": voice_session.current_transcript,
        "history": voice_session.transcript_history[-10:] if voice_session.transcript_history else []
    }

@router.get("/devices")
def get_devices():
    return {
        "microphones": sr.Microphone.list_microphone_names(),
        "voices": tts_manager.get_voices()
    }

@router.post("/action")
async def execute_voice_action(payload: Dict[str, Any]):
    action = payload.get("action")
    # Dispatch internally via REST to capability manager as if an Intent triggered it
    await input_manager.route_input(
        InputType.REST,
        {"action": action, "parameters": payload.get("parameters", {})}
    )
    return {"status": "dispatched"}

@router.post("/debug/inject")
async def inject_debug_event(payload: Dict[str, Any]):
    from app.core.engine.event_bus import event_bus, Event
    import uuid, time
    await event_bus.publish(Event(
        id=str(uuid.uuid4()),
        type=payload.get("type", "UNKNOWN"),
        source="DiagnosticsTool",
        payload=payload.get("payload", {}),
        timestamp=time.time()
    ))
    return {"status": "injected"}
