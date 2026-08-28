"""Extension Loader — discovers and loads extensions from the extensions/ directory."""
import os
import json
from typing import List, Tuple
from .models import ExtensionManifest, ExtensionRecord, ExtensionStatus
from .validator import extension_validator
from .sandbox import ExtensionSandbox
from .registry import extension_registry
from app.core.logging import logger

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))  # backend/app/services/extensions
_BACKEND_DIR = os.path.abspath(os.path.join(_THIS_DIR, "../../../"))  # backend/
EXTENSIONS_DIR = os.path.join(_BACKEND_DIR, "extensions")
MANIFEST_FILENAME = "agniv-extension.json"

# Keep sandboxes alive for lifecycle management
_sandboxes: dict = {}


class ExtensionLoader:
    def __init__(self):
        self.extensions_dir = os.path.abspath(EXTENSIONS_DIR)
        if not os.path.exists(self.extensions_dir):
            os.makedirs(self.extensions_dir)

    def discover(self) -> List[str]:
        """Return list of extension directory names found in extensions/."""
        found = []
        if not os.path.isdir(self.extensions_dir):
            return found
        for item in os.listdir(self.extensions_dir):
            full = os.path.join(self.extensions_dir, item)
            manifest_path = os.path.join(full, MANIFEST_FILENAME)
            if os.path.isdir(full) and os.path.exists(manifest_path) and not item.startswith("_"):
                found.append(item)
        return found

    def load_extension(self, dir_name: str) -> Tuple[bool, str]:
        """Validate, sandbox, and register a single extension directory."""
        ext_path = os.path.join(self.extensions_dir, dir_name)
        manifest_path = os.path.join(ext_path, MANIFEST_FILENAME)

        # Validate manifest
        ok, errors = extension_validator.validate_manifest_file(manifest_path)
        if not ok:
            logger.error(f"[Loader] Extension '{dir_name}' manifest invalid: {errors}")
            return False, f"Manifest invalid: {'; '.join(errors)}"

        with open(manifest_path, "r", encoding="utf-8") as f:
            raw = json.load(f)
        manifest = ExtensionManifest(**raw)

        # Validate entry point
        ok, errors = extension_validator.validate_entry_point(ext_path, manifest.entry_point)
        if not ok:
            return False, errors[0]

        # Skip if already registered
        if extension_registry.get(manifest.id):
            return True, "Already loaded"

        # Create sandbox
        sandbox = ExtensionSandbox(manifest, ext_path)
        if not sandbox.load():
            record = ExtensionRecord(
                id=manifest.id, manifest=manifest,
                status=ExtensionStatus.ERROR, path=ext_path,
                error="Sandbox load failed"
            )
            extension_registry.register(record)
            return False, "Sandbox load failed"

        _sandboxes[manifest.id] = sandbox

        record = ExtensionRecord(
            id=manifest.id, manifest=manifest,
            status=ExtensionStatus.INSTALLED, path=ext_path
        )
        extension_registry.register(record)
        logger.info(f"[Loader] Extension '{manifest.name}' ({manifest.id}) loaded.")
        return True, "Loaded"

    def load_all(self) -> int:
        """Discover and load all extensions. Returns count of successfully loaded."""
        names = self.discover()
        loaded = 0
        for name in names:
            ok, _ = self.load_extension(name)
            if ok:
                loaded += 1
        return loaded

    def get_sandbox(self, ext_id: str) -> ExtensionSandbox:
        return _sandboxes.get(ext_id)


extension_loader = ExtensionLoader()
