from typing import Dict, List, Optional
from .models import MemoryItem

class MemoryStore:
    def __init__(self):
        self.memories: Dict[str, MemoryItem] = {}

    def add(self, memory: MemoryItem):
        self.memories[memory.id] = memory

    def get(self, memory_id: str) -> Optional[MemoryItem]:
        return self.memories.get(memory_id)

    def get_all(self) -> List[MemoryItem]:
        return list(self.memories.values())

    def update(self, memory: MemoryItem):
        if memory.id in self.memories:
            self.memories[memory.id] = memory

    def delete(self, memory_id: str):
        if memory_id in self.memories:
            del self.memories[memory_id]

memory_store = MemoryStore()
