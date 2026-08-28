from .models import MemoryItem
from .store import memory_store
from .index import memory_index
from .scorer import memory_scorer
from app.core.logging import logger

class MemoryManager:
    def create_memory(self, memory: MemoryItem) -> MemoryItem:
        if not memory.importance:
            memory.importance = memory_scorer.score(memory.type, memory.source, memory.outcome)
        
        memory_store.add(memory)
        memory_index.index(memory)
        logger.info(f"Memory Created: [{memory.type}] {memory.title}")
        return memory

    def delete_memory(self, memory_id: str):
        memory = memory_store.get(memory_id)
        if memory:
            memory_index.remove(memory)
            memory_store.delete(memory_id)
            logger.info(f"Memory Deleted: {memory_id}")

    def get_all(self):
        return memory_store.get_all()

memory_manager = MemoryManager()
