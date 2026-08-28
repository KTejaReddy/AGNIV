"""Extension Registry — in-memory store of all known extensions."""
from typing import Dict, List, Optional
from .models import ExtensionRecord, ExtensionStatus, ExtensionType


class ExtensionRegistry:
    def __init__(self):
        self._extensions: Dict[str, ExtensionRecord] = {}

    def register(self, record: ExtensionRecord) -> None:
        self._extensions[record.id] = record

    def unregister(self, ext_id: str) -> bool:
        if ext_id in self._extensions:
            del self._extensions[ext_id]
            return True
        return False

    def get(self, ext_id: str) -> Optional[ExtensionRecord]:
        return self._extensions.get(ext_id)

    def all(self) -> List[ExtensionRecord]:
        return list(self._extensions.values())

    def by_type(self, ext_type: ExtensionType) -> List[ExtensionRecord]:
        return [e for e in self._extensions.values() if e.manifest.type == ext_type]

    def enabled(self) -> List[ExtensionRecord]:
        return [e for e in self._extensions.values() if e.status == ExtensionStatus.ENABLED]

    def set_status(self, ext_id: str, status: ExtensionStatus, error: str = None) -> None:
        if ext_id in self._extensions:
            self._extensions[ext_id].status = status
            if error:
                self._extensions[ext_id].error = error

    def set_metadata(self, ext_id: str, metadata: dict) -> None:
        if ext_id in self._extensions:
            self._extensions[ext_id].metadata = metadata


extension_registry = ExtensionRegistry()
