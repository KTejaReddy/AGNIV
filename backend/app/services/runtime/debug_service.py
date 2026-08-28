import asyncio
import time
from typing import Any, Dict
from app.core.engine.event_bus import event_bus, Event
from app.core.logging import logger

# Import all session managers to read live data
from app.services.perception.session import perception_session
from app.services.perception.camera import camera_manager
from app.services.voice.session import voice_session
from app.services.cognitive.session import cognitive_session
from app.services.screen.session import screen_session
from app.services.runtime.controller import runtime_controller
# Mock imports for missing sessions, we'll try to get them dynamically or safely
try:
    from app.services.workflow.session import workflow_session
except ImportError:
    workflow_session = None
try:
    from app.services.skills.session import skills_session
except ImportError:
    skills_session = None
try:
    from app.services.memory.session import memory_session
except ImportError:
    memory_session = None
try:
    from app.services.desktop.session import desktop_session
except ImportError:
    desktop_session = None

class DebugService:
    def __init__(self):
        self.last_event: Dict[str, Any] = {}
        
        # Subscribe to ALL events to capture the last event bus message
        event_bus.subscribe("*", self._on_any_event)

    async def _on_any_event(self, event: Event):
        if event.type != "DEBUG_OVERLAY_UPDATE":
            self.last_event = {
                "type": event.type,
                "source": event.source,
                "timestamp": event.timestamp
            }

    async def start(self):
        logger.info("[DebugService] Starting live debug overlay loop.")
        while True:
            try:
                state = self.collect_state()
                await event_bus.publish(Event(
                    id=f"debug_{time.time()}",
                    type="DEBUG_OVERLAY_UPDATE",
                    source="DebugService",
                    payload=state,
                    timestamp=time.time()
                ))
            except Exception as e:
                logger.error(f"[DebugService] Error aggregating state: {e}")
                
            await asyncio.sleep(0.5)

    def collect_state(self) -> Dict[str, Any]:
        from app.services.cognitive.provider import provider_manager
        
        # Build strict 11-key schema using live runtime data
        return {
            "camera": {
                "connected": camera_manager.is_running and camera_manager.cap is not None and camera_manager.cap.isOpened(),
                "capture_fps": perception_session.capture_fps,
                "mediapipe_fps": perception_session.mediapipe_fps,
                "render_fps": perception_session.render_fps,
            },
            "screen": {
                "active": screen_session.active if screen_session else False
            },
            "voice": {
                "listening": runtime_controller.state == "LISTENING",
                "state": runtime_controller.state,
                "wake_word": voice_session.wake_word_detected if hasattr(voice_session, 'wake_word_detected') else False
            },
            "groq": {
                "status": provider_manager.connection_status.lower(),
                "latency_ms": provider_manager.last_latency_ms
            },
            "runtime": {
                "running": getattr(runtime_controller, 'is_running', False),
                "status": runtime_controller.state,
                "presence": runtime_controller.presence,
                "last_event": self.last_event
            },
            "perception": {
                "hand_landmarks": perception_session.active_trackers.get("hands", False),
                "face_landmarks": perception_session.active_trackers.get("face", False),
                "body_landmarks": perception_session.active_trackers.get("body", False),
                "current_gesture": perception_session.current_state.get("gesture", "None")
            },
            "workflow": {
                "active_workflow": workflow_session.current_workflow if workflow_session and hasattr(workflow_session, 'current_workflow') else "None"
            },
            "memory": {
                "last_retrieval": memory_session.last_retrieval if memory_session and hasattr(memory_session, 'last_retrieval') else "None"
            },
            "skills": {
                "active_skill": skills_session.active_skill if skills_session and hasattr(skills_session, 'active_skill') else "None"
            },
            "extensions": {
                "loaded": [] # Can be mapped later if needed
            },
            "desktop": {
                "active_capability": desktop_session.active_capability if desktop_session and hasattr(desktop_session, 'active_capability') else "None"
            }
        }

debug_service = DebugService()
