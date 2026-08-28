"""Extension Manager — top-level orchestrator."""
from typing import List, Dict, Any
from .registry import extension_registry
from .loader import extension_loader
from .lifecycle import extension_lifecycle
from .models import ExtensionRecord, ExtensionType
from app.core.logging import logger


class ExtensionManager:

    def boot(self) -> int:
        """Load all extensions from the extensions/ directory on startup."""
        count = extension_loader.load_all()
        logger.info(f"[ExtensionManager] Booted {count} extension(s).")
        return count

    def list_all(self) -> List[ExtensionRecord]:
        return extension_registry.all()

    def list_by_type(self, ext_type: ExtensionType) -> List[ExtensionRecord]:
        return extension_registry.by_type(ext_type)

    def get(self, ext_id: str) -> ExtensionRecord:
        return extension_registry.get(ext_id)

    async def enable(self, ext_id: str):
        return await extension_lifecycle.enable(ext_id)

    async def disable(self, ext_id: str):
        return await extension_lifecycle.disable(ext_id)

    def install(self, dir_name: str):
        return extension_lifecycle.install(dir_name)

    async def uninstall(self, ext_id: str):
        return await extension_lifecycle.uninstall(ext_id)

    def rescan(self) -> int:
        """Re-scan extensions/ for newly dropped extensions."""
        discovered = extension_loader.discover()
        loaded = 0
        for name in discovered:
            ok, _ = extension_loader.load_extension(name)
            if ok:
                loaded += 1
        return loaded

    def get_stats(self) -> Dict[str, Any]:
        all_ext = extension_registry.all()
        return {
            "total": len(all_ext),
            "enabled": len([e for e in all_ext if e.status.value == "enabled"]),
            "disabled": len([e for e in all_ext if e.status.value == "disabled"]),
            "error": len([e for e in all_ext if e.status.value == "error"]),
            "by_type": {
                t.value: len(extension_registry.by_type(t)) for t in ExtensionType
            }
        }


extension_manager = ExtensionManager()
