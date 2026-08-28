from fastapi import APIRouter, HTTPException
from typing import Any, Dict
from pydantic import BaseModel
from app.services.cognitive.session import cognitive_session
from app.services.cognitive.context import context_builder
from app.services.cognitive.conversation import conversation_manager
from app.services.cognitive.pipeline import thinking_pipeline
from app.services.cognitive.provider import provider_manager

router = APIRouter()

class InputPayload(BaseModel):
    text: str

class KeyPayload(BaseModel):
    api_key: str

@router.get("/status")
def get_cognitive_status():
    return cognitive_session.get_status()

@router.get("/context")
def get_current_context():
    # Only return the current snapshot built recently, or force a build
    return context_builder.build_unified_context()
    
@router.get("/history")
def get_history():
    return {"history": conversation_manager.get_recent(20)}

@router.post("/process")
async def process_input(payload: InputPayload):
    try:
        response = await thinking_pipeline.process_input(payload.text)
        return {"response": response, "status": cognitive_session.get_status()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
@router.post("/set_api_key")
def set_api_key(payload: KeyPayload):
    import os
    os.environ["GROQ_API_KEY"] = payload.api_key
    # Re-initialize provider
    from app.services.cognitive.provider import GroqClient
    global provider_manager
    # Dirty patch for demo purposes, in real app handle with dependency injection
    import app.services.cognitive.provider as p
    p.provider_manager = GroqClient()
    
    # We must patch it in pipeline too since it imported it
    import app.services.cognitive.pipeline as pip
    pip.provider_manager = p.provider_manager
    
    return {"status": "success", "message": "API Key updated and provider reinitialized."}
