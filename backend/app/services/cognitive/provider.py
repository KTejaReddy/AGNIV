from typing import Dict, Any, List, AsyncGenerator, Optional
import os
import time
from app.core.logging import logger
from app.database.session import SessionLocal
from app.database.models import Setting

try:
    from groq import AsyncGroq
except ImportError:
    AsyncGroq = None

class LLMProvider:
    async def generate(self, messages: List[Dict[str, str]]) -> str:
        raise NotImplementedError
        
    async def generate_stream(self, messages: List[Dict[str, str]]) -> AsyncGenerator[str, None]:
        raise NotImplementedError

class GroqClient(LLMProvider):
    def __init__(self):
        self.api_key: Optional[str] = None
        self.client: Optional[AsyncGroq] = None
        self.model: str = "llama-3.1-8b-instant"
        self._last_key: Optional[str] = None
        self.connection_status: str = "Unknown"
        self.last_latency_ms: float = 0.0

    def _get_config(self):
        db = SessionLocal()
        from app.core.config import settings
        try:
            key_setting = db.query(Setting).filter(Setting.key == "GROQ_API_KEY").first()
            model_setting = db.query(Setting).filter(Setting.key == "GROQ_MODEL").first()
            
            # Fallback to env var if not in DB
            api_key = key_setting.value if key_setting and key_setting.value else settings.GROQ_API_KEY
            model = model_setting.value if model_setting and model_setting.value else "llama-3.1-8b-instant"
            
            return api_key, model
        finally:
            db.close()

    def _ensure_client(self):
        api_key, self.model = self._get_config()
        if not api_key:
            self.client = None
            return
            
        if api_key != self._last_key:
            if AsyncGroq:
                self.client = AsyncGroq(api_key=api_key)
                self._last_key = api_key
            else:
                self.client = None

    async def check_connection(self):
        logger.info("Provider initialized")
        self._ensure_client()
        logger.info(f"API key loaded: {'Yes' if self._last_key else 'No'}")
        
        if not self.client:
            self.connection_status = "Missing API Key"
            return
            
        try:
            logger.info("Connection test started")
            # Ping the API to verify authentication
            start_t = time.time()
            await self.client.models.list()
            latency = (time.time() - start_t) * 1000
            self.last_latency_ms = latency
            
            logger.info("Authentication successful")
            logger.info(f"Selected model: {self.model}")
            logger.info(f"Latency: {latency:.2f}ms")
            
            self.connection_status = "Connected"
        except Exception as e:
            logger.error(f"Exact Groq error: {e}", exc_info=True)
            err_str = str(e).lower()
            if "authentication" in err_str or "invalid api key" in err_str or "unauthorized" in err_str:
                self.connection_status = "Invalid API Key"
            else:
                self.connection_status = "Connection Failed"

    async def generate(self, messages: List[Dict[str, str]]) -> str:
        self._ensure_client()
        
        if not self.client:
            logger.error("Groq client not initialized (Missing API Key)")
            return '{"type": "ERROR", "text": "Groq client not initialized (Missing API Key)"}'
            
        try:
            start_t = time.time()
            chat_completion = await self.client.chat.completions.create(
                messages=messages,
                model=self.model,
                temperature=0.0,
            )
            latency = time.time() - start_t
            logger.info(f"Groq inference took {latency:.2f}s")
            return chat_completion.choices[0].message.content
        except Exception as e:
            err_str = str(e)
            logger.error(f"Groq Error: {err_str}")
            if "authentication" in err_str.lower() or "invalid api key" in err_str.lower():
                return '{"type": "ERROR", "text": "Groq Authentication Failed: Invalid API Key"}'
            if "rate limit" in err_str.lower():
                return '{"type": "ERROR", "text": "Groq Rate Limit Exceeded"}'
            return f'{{"type": "ERROR", "text": "Groq Error: {err_str}"}}'

provider_manager = GroqClient()
