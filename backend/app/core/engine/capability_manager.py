from typing import Dict, Any, Callable
from app.core.logging import logger
from .event_bus import event_bus, Event
import time
import uuid

class CapabilityManager:
    def __init__(self):
        self.capabilities: Dict[str, Dict[str, Any]] = {}
        
    async def initialize(self):
        logger.info("Capability Manager initialized")

    def register_capability(self, name: str, version: str, description: str, handler: Callable):
        self.capabilities[name] = {
            "version": version,
            "description": description,
            "handler": handler
        }
        logger.info(f"Capability registered: {name} (v{version})")

    def get_registered_capabilities_metadata(self) -> str:
        if not self.capabilities:
            return "No capabilities currently registered."
        lines = []
        for name, data in self.capabilities.items():
            lines.append(f"- {name}: {data['description']}")
        return "\n".join(lines)

    async def execute_capability(self, name: str, parameters: Dict[str, Any]):
        if name not in self.capabilities:
            logger.error(f"Capability not found: {name}")
            return False, "Not found"
            
        # In a real system, PermissionManager is checked right before execution
        from .permission_manager import permission_manager
        
        allowed = permission_manager.check_permission(name)
        if not allowed:
            logger.warning(f"Permission denied for capability: {name}")
            await event_bus.publish(Event(
                id=str(uuid.uuid4()),
                type="CAPABILITY_DENIED",
                source="CapabilityManager",
                payload={"capability": name, "reason": "Permission Denied"},
                timestamp=time.time()
            ))
            return False, "Permission Denied"
            
        try:
            logger.info(f"Executing capability: {name}")
            
            # Execute the actual capability handler
            handler = self.capabilities[name]["handler"]
            import inspect
            if inspect.iscoroutinefunction(handler):
                result = await handler(parameters)
            else:
                result = handler(parameters)
                
            await event_bus.publish(Event(
                id=str(uuid.uuid4()),
                type="CAPABILITY_EXECUTED",
                source="CapabilityManager",
                payload={"capability": name, "parameters": parameters, "success": True},
                timestamp=time.time()
            ))
            return True, result
        except Exception as e:
            logger.error(f"Error executing capability {name}: {e}")
            return False, str(e)

capability_manager = CapabilityManager()
