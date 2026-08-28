from typing import List, Dict, Set
from .models import MemoryItem, MemoryType

class MemoryIndex:
    def __init__(self):
        self.by_type: Dict[MemoryType, Set[str]] = {t: set() for t in MemoryType}
        self.by_tag: Dict[str, Set[str]] = {}

    def index(self, memory: MemoryItem):
        self.by_type[memory.type].add(memory.id)
        for tag in memory.tags:
            tag = tag.lower()
            if tag not in self.by_tag:
                self.by_tag[tag] = set()
            self.by_tag[tag].add(memory.id)

    def remove(self, memory: MemoryItem):
        if memory.id in self.by_type[memory.type]:
            self.by_type[memory.type].remove(memory.id)
        for tag in memory.tags:
            tag = tag.lower()
            if tag in self.by_tag and memory.id in self.by_tag[tag]:
                self.by_tag[tag].remove(memory.id)

memory_index = MemoryIndex()
