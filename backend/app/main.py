from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.exceptions import global_exception_handler, AGNIVException

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(AGNIVException, global_exception_handler)

from typing import Any
from fastapi import Depends
from app.database.session import get_db
from sqlalchemy.orm import Session
from app.services.settings_manager import SettingsManager

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/runtime/health")
def runtime_health():
    from app.services.runtime.debug_service import debug_service
    return debug_service.collect_state()

@app.get("/system")
def get_system_info():
    import platform
    return {
        "os": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "architecture": platform.machine(),
    }

@app.get("/settings/{key}")
def get_setting(key: str, db: Session = Depends(get_db)):
    return {"key": key, "value": SettingsManager.get_setting(db, key)}

@app.post("/settings/{key}")
def set_setting(key: str, payload: dict, db: Session = Depends(get_db)):
    value = payload.get("value")
    SettingsManager.set_setting(db, key, value)
    return {"key": key, "value": value}

@app.get("/logs")
def get_logs():
    import os
    logs = []
    if os.path.exists("logs/app.log"):
        with open("logs/app.log", "r") as f:
            logs = f.readlines()
    return {"logs": logs[-100:]}


from app.api.endpoints.core import router as core_router
from app.api.endpoints.desktop import router as desktop_router
from app.api.endpoints.voice import router as voice_router
from app.api.endpoints.perception import router as perception_router
from app.api.endpoints.screen import router as screen_router
from app.api.endpoints.cognitive import router as cognitive_router
from app.api.endpoints.interaction import router as interaction_router
from app.api.endpoints.knowledge import router as knowledge_router
from app.api.endpoints.workflow import router as workflow_router
from app.api.endpoints.skills import router as skills_router
from app.api.endpoints.memory import router as memory_router
from app.api.endpoints.adaptive import router as adaptive_router
from app.api.endpoints.accessibility import router as accessibility_router
from app.api.endpoints.extensions import router as extensions_router
from app.services.cognitive.provider_config import router as provider_config_router

from app.core.engine import initialize_engine
from app.services.desktop import register_desktop_capabilities
from app.services.voice import register_voice_capabilities
from app.services.perception import register_perception_capabilities
from app.services.screen import register_screen_capabilities
from app.services.cognitive import register_cognitive_capabilities
from app.services.interaction import register_interaction_capabilities
from app.services.knowledge import register_knowledge_capabilities
from app.services.workflow import register_workflow_engine
from app.services.skills import register_skills_engine
from app.services.memory import register_memory_engine
from app.services.adaptive import register_adaptive_engine
from app.services.accessibility import register_accessibility_suite
from app.services.extensions import register_extension_sdk

app.include_router(core_router, prefix="/core", tags=["core"])
app.include_router(desktop_router, prefix="/desktop", tags=["desktop"])
app.include_router(voice_router, prefix="/voice", tags=["voice"])
app.include_router(perception_router, prefix="/perception", tags=["perception"])
app.include_router(screen_router, prefix="/screen", tags=["screen"])
app.include_router(cognitive_router, prefix="/cognitive", tags=["cognitive"])
app.include_router(interaction_router, prefix="/interaction", tags=["interaction"])
app.include_router(knowledge_router, prefix="/knowledge", tags=["knowledge"])
app.include_router(workflow_router, prefix="/workflow", tags=["workflow"])
app.include_router(skills_router, prefix="/skills", tags=["skills"])
app.include_router(memory_router, prefix="/memory", tags=["memory"])
app.include_router(adaptive_router, prefix="/adaptive", tags=["adaptive"])
app.include_router(accessibility_router, prefix="/accessibility", tags=["accessibility"])
app.include_router(extensions_router, prefix="/extensions", tags=["extensions"])
app.include_router(provider_config_router, prefix="/provider", tags=["provider"])

@app.on_event("startup")
async def startup_event():
    await initialize_engine(manager)
    register_desktop_capabilities()
    register_voice_capabilities()
    register_perception_capabilities()
    register_screen_capabilities()
    register_cognitive_capabilities()
    register_interaction_capabilities()
    register_knowledge_capabilities()
    register_workflow_engine()
    register_skills_engine()
    register_memory_engine()
    register_adaptive_engine()
    register_accessibility_suite()
    register_extension_sdk()

    # Register Runtime Controller
    from app.services.runtime.controller import runtime_controller
    from app.services.runtime.debug_service import debug_service
    from app.core.engine.supervisor import supervisor
    await supervisor.register_service("RuntimeController", runtime_controller.start, restart=True)
    await supervisor.register_service("DebugService", debug_service.start, restart=True)
    await supervisor.start_all()

    # Auto-start essential hardware/sensors for Debug Overlay & Living Runtime
    from app.services.perception.camera import camera_manager
    from app.services.perception.session import perception_session
    from app.services.screen.manager import screen_manager
    from app.services.cognitive.provider import provider_manager
    import asyncio
    
    camera_manager.start(0)
    for tracker in ["hands", "face", "body", "gestures"]:
        perception_session.set_tracker_state(tracker, True)
        
    screen_manager.start(1)
    
    asyncio.create_task(provider_manager.check_connection())

# We'll use this array to manage connected websocket clients
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                pass

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # In Phase 2, we just let event bus broadcast, but we can echo for debugging
            # await manager.broadcast(f"Echo: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

