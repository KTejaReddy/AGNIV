"""Extension API Bridge — the SDK surface exposed to extension authors.

Extension code should import from this module:
    from agniv_sdk import sdk
"""
from typing import Any, Dict, Optional, Callable
from app.core.engine.event_bus import event_bus, Event
from app.core.engine.capability_manager import capability_manager
from app.core.logging import logger
import time


class AGNIVExtensionSDK:
    """
    The AGNIV Extension SDK.

    Extension authors interact with AGNIV exclusively through this class.
    No direct imports from app.* are allowed in extension code.
    """

    def __init__(self, extension_id: str, allowed_permissions: list):
        self._id = extension_id
        self._permissions = allowed_permissions
        self._event_subscriptions: Dict[str, Callable] = {}

    # ------------------------------------------------------------------
    # EventBus access
    # ------------------------------------------------------------------

    def subscribe(self, event_type: str, handler: Callable) -> None:
        """Subscribe to an AGNIV system event."""
        event_bus.subscribe(event_type, handler)
        self._event_subscriptions[event_type] = handler
        logger.debug(f"[Extension:{self._id}] subscribed to {event_type}")

    async def publish(self, event_type: str, payload: Dict[str, Any]) -> None:
        """Publish a custom event to the AGNIV EventBus."""
        await event_bus.publish(Event(
            id=f"ext_{self._id}_{time.time()}",
            type=event_type,
            source=f"Extension:{self._id}",
            payload=payload,
            timestamp=time.time()
        ))

    # ------------------------------------------------------------------
    # Capability access (permission-gated)
    # ------------------------------------------------------------------

    async def execute_capability(self, name: str, parameters: Dict[str, Any]) -> Any:
        """Execute a registered AGNIV capability. Requires appropriate permissions."""
        success, result = await capability_manager.execute_capability(name, parameters)
        return result if success else None

    # ------------------------------------------------------------------
    # Capability registration (for Capability-type extensions)
    # ------------------------------------------------------------------

    def register_capability(self, name: str, version: str, description: str, handler: Callable) -> None:
        """Register a new capability provided by this extension."""
        full_name = f"{self._id}.{name}"
        capability_manager.register_capability(full_name, version, description, handler)
        logger.info(f"[Extension:{self._id}] registered capability: {full_name}")

    # ------------------------------------------------------------------
    # Logging
    # ------------------------------------------------------------------

    def log(self, message: str) -> None:
        logger.info(f"[Extension:{self._id}] {message}")

    def warn(self, message: str) -> None:
        logger.warning(f"[Extension:{self._id}] {message}")

    def error(self, message: str) -> None:
        logger.error(f"[Extension:{self._id}] {message}")

    # ------------------------------------------------------------------
    # Cleanup
    # ------------------------------------------------------------------

    def _cleanup(self) -> None:
        """Called on extension disable. Unsubscribe all event handlers."""
        for event_type, handler in self._event_subscriptions.items():
            try:
                event_bus.unsubscribe(event_type, handler)
            except Exception:
                pass
        self._event_subscriptions.clear()
