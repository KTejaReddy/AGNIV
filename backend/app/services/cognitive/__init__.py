from app.core.engine.capability_manager import capability_manager
from app.core.logging import logger
from .pipeline import thinking_pipeline
from .session import cognitive_session
from .conversation import conversation_manager
from .provider import provider_manager

async def process_text_input_cap(params):
    text = params.get("text", "")
    if not text:
        return {"status": "error", "reason": "No text provided"}
        
    response = await thinking_pipeline.process_input(text)
    return {"status": "success", "response": response}

async def clear_conversation_cap(params):
    conversation_manager.clear()
    return {"status": "success"}

def register_cognitive_capabilities():
    logger.info("Registering Cognitive Capabilities...")
    capability_manager.register_capability("PROCESS_TEXT_INPUT", "1.0", "Send text through the thinking pipeline", process_text_input_cap)
    capability_manager.register_capability("CLEAR_CONVERSATION", "1.0", "Clears chat history", clear_conversation_cap)
    logger.info("Cognitive Capabilities registered successfully.")
