import asyncio
import time
import psutil
from typing import Dict, Any
from app.core.logging import logger
from app.core.engine.event_bus import event_bus, Event

class DiagnosticsEngine:
    def __init__(self):
        self.running = False
        self.subsystems = {
            "Runtime Controller": {"status": "⚪ Disabled", "is_initialized": False, "is_running": False, "last_error": "", "last_update": 0, "heartbeat": 0},
            "EventBus": {"status": "⚪ Disabled", "is_initialized": False, "is_running": False, "last_error": "", "last_update": 0, "heartbeat": 0},
            "Wake Word": {"status": "⚪ Disabled", "is_initialized": False, "is_running": False, "last_error": "", "last_update": 0, "heartbeat": 0},
            "Speech Recognition": {"status": "⚪ Disabled", "is_initialized": False, "is_running": False, "last_error": "", "last_update": 0, "heartbeat": 0},
            "Voice Session": {"status": "⚪ Disabled", "is_initialized": False, "is_running": False, "last_error": "", "last_update": 0, "heartbeat": 0},
            "TTS": {"status": "⚪ Disabled", "is_initialized": False, "is_running": False, "last_error": "", "last_update": 0, "heartbeat": 0},
            "Groq Provider": {"status": "⚪ Disabled", "is_initialized": False, "is_running": False, "last_error": "", "last_update": 0, "heartbeat": 0},
            "Action Planner": {"status": "⚪ Disabled", "is_initialized": False, "is_running": False, "last_error": "", "last_update": 0, "heartbeat": 0},
            "Task Manager": {"status": "⚪ Disabled", "is_initialized": False, "is_running": False, "last_error": "", "last_update": 0, "heartbeat": 0},
            "Capability Manager": {"status": "⚪ Disabled", "is_initialized": False, "is_running": False, "last_error": "", "last_update": 0, "heartbeat": 0},
            "Desktop Controller": {"status": "⚪ Disabled", "is_initialized": False, "is_running": False, "last_error": "", "last_update": 0, "heartbeat": 0},
            "Screen Intelligence": {"status": "⚪ Disabled", "is_initialized": False, "is_running": False, "last_error": "", "last_update": 0, "heartbeat": 0},
            "Perception": {"status": "⚪ Disabled", "is_initialized": False, "is_running": False, "last_error": "", "last_update": 0, "heartbeat": 0},
            "Memory": {"status": "⚪ Disabled", "is_initialized": False, "is_running": False, "last_error": "", "last_update": 0, "heartbeat": 0},
            "Workflow": {"status": "⚪ Disabled", "is_initialized": False, "is_running": False, "last_error": "", "last_update": 0, "heartbeat": 0},
            "Extensions": {"status": "⚪ Disabled", "is_initialized": False, "is_running": False, "last_error": "", "last_update": 0, "heartbeat": 0},
        }
        self.pipeline_stage = "Wake Word"
        self.failure_inspector = None
        self.recent_events = []
        
        event_bus.subscribe("*", self._on_event)

    async def _on_event(self, event: Event):
        self.recent_events.append(event.dict())
        if len(self.recent_events) > 50:
            self.recent_events.pop(0)
            
        etype = event.type
        if etype == "WAKE_WORD_DETECTED":
            self.pipeline_stage = "Wake Word"
            self._update_subsystem("Wake Word", "🟢 Healthy", is_running=True)
        elif etype == "VOICE_TRANSCRIPT":
            self.pipeline_stage = "Speech Recognition"
            self._update_subsystem("Speech Recognition", "🟢 Healthy", is_running=True)
            self.pipeline_stage = "Transcript"
        elif etype == "LLM_STARTED":
            self.pipeline_stage = "Groq"
            self._update_subsystem("Groq Provider", "🟡 Waiting", is_running=True)
        elif etype == "LLM_FINISHED":
            self._update_subsystem("Groq Provider", "🟢 Healthy")
        elif etype == "PLAN_CREATED":
            self.pipeline_stage = "Execution Plan"
            self._update_subsystem("Action Planner", "🟢 Healthy", is_running=True)
        elif etype == "TASK_STARTED":
            self.pipeline_stage = "Capability"
            self._update_subsystem("Capability Manager", "🟡 Waiting", is_running=True)
        elif etype == "TASK_FINISHED":
            self._update_subsystem("Capability Manager", "🟢 Healthy")
        elif etype == "TASK_FAILED":
            self._update_subsystem("Capability Manager", "🔴 Failed", error=event.payload.get("result", "Unknown task failure"))
            self._set_failure("Capability Manager", "Task Execution Failed", event.payload.get("result", ""), "Unknown", "Unknown", "Check capability arguments")
        elif etype == "TTS_STARTED":
            self.pipeline_stage = "TTS"
            self._update_subsystem("TTS", "🟡 Waiting", is_running=True)
        elif etype == "TTS_FINISHED":
            self.pipeline_stage = "Listening"
            self._update_subsystem("TTS", "🟢 Healthy")
        elif etype == "SERVICE_CRASHED":
            svc = event.payload.get("service", "")
            err = event.payload.get("error", "")
            mapped_svc = self._map_service_name(svc)
            if mapped_svc:
                self._update_subsystem(mapped_svc, "🔴 Failed", error=err)
                self._set_failure(mapped_svc, "Service Crashed", err, "supervisor.py", "start_service", "Check service logs and restart")

    def _map_service_name(self, name: str) -> str:
        mapping = {
            "RuntimeController": "Runtime Controller",
            "EventBus": "EventBus",
            "DebugService": "Runtime Controller"
        }
        return mapping.get(name, name if name in self.subsystems else None)

    def _update_subsystem(self, name: str, status: str, is_init=None, is_running=None, error=None):
        if name in self.subsystems:
            now = time.time()
            self.subsystems[name]["status"] = status
            self.subsystems[name]["last_update"] = now
            self.subsystems[name]["heartbeat"] = now
            if is_init is not None:
                self.subsystems[name]["is_initialized"] = is_init
            if is_running is not None:
                self.subsystems[name]["is_running"] = is_running
            if error is not None:
                self.subsystems[name]["last_error"] = error

    def _set_failure(self, feature: str, failure: str, root_cause: str, file: str, function: str, suggested_fix: str):
        self.failure_inspector = {
            "feature": feature,
            "failure": failure,
            "root_cause": root_cause,
            "file": file,
            "function": function,
            "suggested_fix": suggested_fix
        }

    async def initialize(self):
        logger.info("Diagnostics Engine initialized")
        self.running = True
        
        for name in self.subsystems:
            self._update_subsystem(name, "🟢 Healthy", is_init=True, is_running=True)
        self.subsystems["EventBus"]["is_initialized"] = True
        self.subsystems["EventBus"]["is_running"] = event_bus._running
        
        asyncio.create_task(self._poll_loop())

    async def _poll_loop(self):
        while self.running:
            await asyncio.sleep(1)
            self._check_heartbeats()
            await self._publish_state()

    def _check_heartbeats(self):
        now = time.time()
        for name, data in self.subsystems.items():
            if data["status"] == "⚪ Disabled":
                continue
                
            time_since_hb = now - data["heartbeat"]
            if not data["is_initialized"]:
                self.subsystems[name]["status"] = "🔴 Failed"
                self.subsystems[name]["last_error"] = "Failed to initialize"
                if not self.failure_inspector:
                     self._set_failure(name, "Initialization Failure", "Module did not start", "unknown", "init", "Check startup logs")
            elif time_since_hb > 5 and data["status"] == "🟢 Healthy":
                self.subsystems[name]["status"] = "🟡 Waiting"

    async def _publish_state(self):
        metrics = self.get_metrics()
        await event_bus.publish(Event(
            id=f"diag_{time.time()}",
            type="DIAGNOSTICS_UPDATE",
            source="DiagnosticsEngine",
            payload=metrics,
            timestamp=time.time()
        ))

    async def verify_all(self):
        results = {}
        for name in self.subsystems:
            self.subsystems[name]["heartbeat"] = time.time()
            if self.subsystems[name]["is_running"]:
                self.subsystems[name]["status"] = "🟢 Healthy"
                results[name] = "OK"
            else:
                self.subsystems[name]["status"] = "🔴 Failed"
                results[name] = "FAILED"
                
        if all(r == "OK" for r in results.values()):
            self.failure_inspector = None
            
        await self._publish_state()
        return {"status": "verification_complete", "results": results}

    def get_metrics(self):
        from app.services.voice.session import voice_session
        from app.core.engine.action_planner import action_planner
        from app.services.runtime.controller import runtime_controller
        
        try:
            from app.services.memory.session import memory_session
        except:
            memory_session = None
        try:
            from app.services.workflow.session import workflow_session
        except:
            workflow_session = None

        state_val = runtime_controller.state
        
        mem_size = memory_session.context_size if memory_session and hasattr(memory_session, "context_size") else 0
        workflow_active = workflow_session.current_workflow if workflow_session and hasattr(workflow_session, "current_workflow") else "None"
        
        sess_id = runtime_controller.session_id if hasattr(runtime_controller, "session_id") else "Unknown"

        return {
            "subsystems": self.subsystems,
            "pipeline": {
                "active_stage": self.pipeline_stage
            },
            "runtime_state": {
                "session_uuid": sess_id,
                "conversation_length": len(action_planner.conversation_history) if hasattr(action_planner, "conversation_history") else 0,
                "current_goal": "Active Conversation" if state_val not in ("IDLE", "WAIT_WAKE_WORD", "SLEEPING") else "None",
                "current_capability": "None",
                "current_workflow": workflow_active,
                "current_tts_state": "IDLE" if self.pipeline_stage != "TTS" else "SPEAKING",
                "current_stt_state": "LISTENING" if state_val == "LISTENING" else "IDLE",
                "current_memory_context_size": mem_size,
                "current_planner_state": "IDLE" if self.pipeline_stage != "Execution Plan" else "PLANNING",
                "runtime_state_val": state_val
            },
            "failure_inspector": self.failure_inspector,
            "recent_events": self.recent_events,
            "health_score": sum(1 for s in self.subsystems.values() if s["status"] == "🟢 Healthy") / max(1, len(self.subsystems)) * 100,
            "cpu_percent": psutil.cpu_percent(),
            "memory_percent": psutil.virtual_memory().percent
        }

diagnostics_engine = DiagnosticsEngine()

