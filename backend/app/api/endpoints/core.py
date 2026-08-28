from fastapi import APIRouter, Depends
from typing import Any, Dict
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.database.models import Permission, Session as SessionModel
from app.core.engine import (
    event_bus, input_manager, capability_manager,
    action_planner, permission_manager, task_manager, context_manager,
    session_manager, diagnostics_engine
)

router = APIRouter()

@router.get("/status")
def get_engine_status():
    return {
        "event_bus": event_bus._running,
        "task_manager": task_manager._running,
        "diagnostics": diagnostics_engine.get_metrics()
    }

@router.post("/diagnostics/verify")
async def verify_diagnostics():
    return await diagnostics_engine.verify_all()

@router.get("/modules")
def get_modules():
    return {
        "input_manager": "active",
        "intent_router": "active",
        "capability_manager": "active",
        "action_planner": "active",
        "permission_manager": "active",
        "context_manager": "active",
        "session_manager": "active"
    }

@router.get("/tasks")
def get_tasks():
    return [task.to_dict() for task in task_manager.tasks.values()]

@router.get("/events")
def get_events():
    return [event.dict() for event in event_bus.history]

@router.get("/capabilities")
def get_capabilities():
    return capability_manager.capabilities

@router.get("/permissions")
def get_permissions(db: Session = Depends(get_db)):
    perms = db.query(Permission).all()
    return [{"id": p.id, "capability": p.capability_name, "rule": p.rule} for p in perms]

@router.get("/sessions")
def get_sessions(db: Session = Depends(get_db)):
    sessions = db.query(SessionModel).all()
    return [{"id": s.id, "active": s.active, "created_at": s.created_at} for s in sessions]

@router.post("/simulate_input")
async def simulate_input(payload: Dict[str, Any]):
    from app.core.engine.input_manager import InputType
    input_type_str = payload.get("type", "REST").upper()
    try:
        input_type = InputType(input_type_str)
    except ValueError:
        input_type = InputType.REST
        
    await input_manager.route_input(input_type, payload)
    return {"status": "dispatched"}
