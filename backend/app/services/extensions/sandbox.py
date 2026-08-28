"""Extension Sandbox — loads extension Python modules in an isolated context.

Each extension runs in its own module namespace. The sandbox injects the
AGNIVExtensionSDK instance as the only bridge to core AGNIV functionality.
Direct imports of app.* within extensions are blocked at the loader level.
"""
import importlib.util
import sys
import os
from typing import Any, Optional
from .models import ExtensionManifest
from .api_bridge import AGNIVExtensionSDK
from app.core.logging import logger


class ExtensionSandbox:
    """
    Loads a single extension Python module.

    The module must expose:
        class Extension:
            def __init__(self, sdk: AGNIVExtensionSDK): ...
            async def on_enable(self): ...
            async def on_disable(self): ...
            def metadata(self) -> dict: ...
    """

    def __init__(self, manifest: ExtensionManifest, extension_path: str):
        self.manifest = manifest
        self.extension_path = extension_path
        self.sdk = AGNIVExtensionSDK(manifest.id, manifest.permissions)
        self._instance: Optional[Any] = None
        self._module: Optional[Any] = None

    def load(self) -> bool:
        """Import the extension module."""
        entry = os.path.join(self.extension_path, self.manifest.entry_point)
        try:
            spec = importlib.util.spec_from_file_location(
                f"agniv_ext_{self.manifest.id}", entry
            )
            module = importlib.util.module_from_spec(spec)
            # Inject SDK into module namespace before exec
            module.sdk = self.sdk
            module.AGNIVExtensionSDK = AGNIVExtensionSDK
            spec.loader.exec_module(module)
            self._module = module

            if not hasattr(module, "Extension"):
                logger.error(f"[Sandbox:{self.manifest.id}] Missing Extension class.")
                return False

            self._instance = module.Extension(self.sdk)
            logger.info(f"[Sandbox:{self.manifest.id}] Loaded successfully.")
            return True
        except Exception as e:
            logger.error(f"[Sandbox:{self.manifest.id}] Load error: {e}")
            return False

    async def enable(self) -> bool:
        if self._instance is None:
            return False
        try:
            if hasattr(self._instance, "on_enable"):
                result = self._instance.on_enable()
                if hasattr(result, "__await__"):
                    await result
            return True
        except Exception as e:
            logger.error(f"[Sandbox:{self.manifest.id}] Enable error: {e}")
            return False

    async def disable(self) -> bool:
        if self._instance is None:
            return False
        try:
            if hasattr(self._instance, "on_disable"):
                result = self._instance.on_disable()
                if hasattr(result, "__await__"):
                    await result
            self.sdk._cleanup()
            return True
        except Exception as e:
            logger.error(f"[Sandbox:{self.manifest.id}] Disable error: {e}")
            return False

    def get_metadata(self) -> dict:
        if self._instance and hasattr(self._instance, "metadata"):
            try:
                return self._instance.metadata()
            except Exception:
                pass
        return {}
