"""Extension Lifecycle — enable, disable, install, and uninstall extensions."""
from typing import Tuple
from .registry import extension_registry
from .loader import extension_loader
from .models import ExtensionStatus
from app.core.engine.event_bus import event_bus, Event
from app.core.logging import logger
import time


class ExtensionLifecycle:

    async def enable(self, ext_id: str) -> Tuple[bool, str]:
        record = extension_registry.get(ext_id)
        if not record:
            return False, f"Extension '{ext_id}' not found."
        if record.status == ExtensionStatus.ENABLED:
            return True, "Already enabled."

        sandbox = extension_loader.get_sandbox(ext_id)
        if not sandbox:
            return False, "Sandbox not available."

        ok = await sandbox.enable()
        if ok:
            extension_registry.set_status(ext_id, ExtensionStatus.ENABLED)
            meta = sandbox.get_metadata()
            extension_registry.set_metadata(ext_id, meta)
            await self._publish("EXTENSION_ENABLED", ext_id)
            logger.info(f"[Lifecycle] Extension '{ext_id}' enabled.")
            return True, "Enabled."
        else:
            extension_registry.set_status(ext_id, ExtensionStatus.ERROR, "Enable failed")
            return False, "Enable failed."

    async def disable(self, ext_id: str) -> Tuple[bool, str]:
        record = extension_registry.get(ext_id)
        if not record:
            return False, f"Extension '{ext_id}' not found."
        if record.status == ExtensionStatus.DISABLED:
            return True, "Already disabled."

        sandbox = extension_loader.get_sandbox(ext_id)
        if sandbox:
            await sandbox.disable()

        extension_registry.set_status(ext_id, ExtensionStatus.DISABLED)
        await self._publish("EXTENSION_DISABLED", ext_id)
        logger.info(f"[Lifecycle] Extension '{ext_id}' disabled.")
        return True, "Disabled."

    def install(self, dir_name: str) -> Tuple[bool, str]:
        """Load a newly dropped extension from the extensions/ directory."""
        ok, msg = extension_loader.load_extension(dir_name)
        return ok, msg

    async def uninstall(self, ext_id: str) -> Tuple[bool, str]:
        record = extension_registry.get(ext_id)
        if not record:
            return False, "Not found."
        await self.disable(ext_id)
        extension_registry.unregister(ext_id)
        await self._publish("EXTENSION_UNINSTALLED", ext_id)
        logger.info(f"[Lifecycle] Extension '{ext_id}' uninstalled.")
        return True, "Uninstalled."

    async def _publish(self, event_type: str, ext_id: str):
        await event_bus.publish(Event(
            id=f"evt_{time.time()}",
            type=event_type,
            source="ExtensionLifecycle",
            payload={"extension_id": ext_id},
            timestamp=time.time()
        ))


extension_lifecycle = ExtensionLifecycle()
