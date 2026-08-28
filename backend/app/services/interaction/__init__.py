import asyncio
from app.core.engine.capability_manager import capability_manager
from app.core.engine import event_bus
from app.core.logging import logger
from .manager import interaction_manager
from .confirmation import confirmation_engine
from .notification import notification_manager

async def request_confirmation_cap(params):
    action = params.get("action", "")
    action_params = params.get("params", {})
    conf_id = await confirmation_engine.request_confirmation(action, action_params, "API")
    return {"status": "success", "confirmation_id": conf_id}

async def trigger_notification_cap(params):
    message = params.get("message", "")
    priority = params.get("priority", "NORMAL")
    await notification_manager.deliver(message, priority)
    return {"status": "success"}

def register_interaction_capabilities():
    logger.info("Registering Human Interaction Capabilities...")
    capability_manager.register_capability("REQUEST_CONFIRMATION", "1.0", "Request user confirmation before execution", request_confirmation_cap)
    capability_manager.register_capability("TRIGGER_NOTIFICATION", "1.0", "Deliver a notification contextually", trigger_notification_cap)
    
    # Start the manager
    asyncio.create_task(interaction_manager.start())
    logger.info("Human Interaction Capabilities registered successfully.")
