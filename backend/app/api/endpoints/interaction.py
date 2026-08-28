from fastapi import APIRouter
from pydantic import BaseModel
from app.services.interaction.session import interaction_session
from app.services.interaction.confirmation import confirmation_engine

router = APIRouter()

class ConfirmPayload(BaseModel):
    accepted: bool

@router.get("/status")
def get_interaction_status():
    return interaction_session.get_status()

@router.post("/confirm")
async def manual_confirm(payload: ConfirmPayload):
    await confirmation_engine.resolve_confirmation(payload.accepted)
    return {"status": "success"}

@router.post("/simulate_gesture")
async def simulate_gesture(payload: dict):
    from app.services.interaction.manager import interaction_manager
    from app.core.engine import Event
    import time
    
    # Send a mock perception event directly into the manager for testing
    mock_event = Event(
        id="test",
        type="PERCEPTION_EVENT",
        source="API",
        payload={
            "faces": [{"id": 1}], # simulate presence
            "gestures": [{"name": payload.get("gesture")}]
        },
        timestamp=time.time()
    )
    await interaction_manager.handle_perception_event(mock_event)
    return {"status": "success"}
