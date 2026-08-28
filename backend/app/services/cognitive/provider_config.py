import time
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.database.session import get_db
from app.database.models import Setting
from sqlalchemy.orm import Session
from .provider import provider_manager
import os

router = APIRouter()

class ProviderConfigModel(BaseModel):
    api_key: Optional[str] = None
    model: str = "llama3-8b-8192"

class ConfigResponse(BaseModel):
    has_key: bool
    masked_key: Optional[str]
    model: str

def mask_api_key(key: str) -> str:
    if not key or len(key) < 8:
        return ""
    return f"{key[:4]}{'*' * 28}{key[-4:]}"

@router.get("/config", response_model=ConfigResponse)
async def get_provider_config(db: Session = Depends(get_db)):
    key_setting = db.query(Setting).filter(Setting.key == "GROQ_API_KEY").first()
    model_setting = db.query(Setting).filter(Setting.key == "GROQ_MODEL").first()
    
    raw_key = key_setting.value if key_setting and key_setting.value else os.environ.get("GROQ_API_KEY", "")
    model = model_setting.value if model_setting and model_setting.value else "llama-3.1-8b-instant"
    
    return ConfigResponse(
        has_key=bool(raw_key),
        masked_key=mask_api_key(raw_key) if raw_key else None,
        model=model
    )

@router.post("/config")
async def save_provider_config(config: ProviderConfigModel, db: Session = Depends(get_db)):
    # Update API Key
    if config.api_key is not None:
        key_setting = db.query(Setting).filter(Setting.key == "GROQ_API_KEY").first()
        if not key_setting:
            key_setting = Setting(key="GROQ_API_KEY", value=config.api_key)
            db.add(key_setting)
        else:
            key_setting.value = config.api_key
            
    # Update Model
    model_setting = db.query(Setting).filter(Setting.key == "GROQ_MODEL").first()
    if not model_setting:
        model_setting = Setting(key="GROQ_MODEL", value=config.model)
        db.add(model_setting)
    else:
        model_setting.value = config.model
        
    db.commit()
    
    # Force provider to reload client on next call
    provider_manager.client = None
    provider_manager._last_key = None
    
    return {"status": "success"}

@router.post("/test")
async def test_connection():
    # Force client initialization if needed
    provider_manager._ensure_client()
    
    if not provider_manager.client:
        raise HTTPException(status_code=400, detail="Groq API key not configured")
        
    start_time = time.time()
    try:
        # A lightweight prompt to verify connection
        response = await provider_manager.client.chat.completions.create(
            messages=[{"role": "user", "content": "ping"}],
            model=provider_manager.model,
            temperature=0.0,
            max_tokens=5
        )
        latency = time.time() - start_time
        return {
            "status": "connected",
            "latency_ms": int(latency * 1000),
            "model": provider_manager.model
        }
    except Exception as e:
        err_str = str(e)
        if "authentication" in err_str.lower() or "invalid api key" in err_str.lower():
            raise HTTPException(status_code=401, detail="Authentication Failed: Invalid API Key")
        elif "rate limit" in err_str.lower():
            raise HTTPException(status_code=429, detail="Rate Limit Exceeded")
        else:
            raise HTTPException(status_code=500, detail=f"Connection Error: {err_str}")
