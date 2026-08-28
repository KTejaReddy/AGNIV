from typing import List, Set
from .store import memory_store
from .index import memory_index
from .models import MemoryItem

class MemoryRetrieval:
    def search(self, query: str) -> List[MemoryItem]:
        query_words = set(query.lower().split())
        matched_ids: Set[str] = set()
        
        # Keyword matching across summary and title (Mock semantic search)
        for mem in memory_store.get_all():
            text = f"{mem.title} {mem.summary}".lower()
            if any(word in text for word in query_words):
                matched_ids.add(mem.id)
                
        # Tag matching
        for word in query_words:
            if word in memory_index.by_tag:
                matched_ids.update(memory_index.by_tag[word])
                
        results = [memory_store.get(mid) for mid in matched_ids if memory_store.get(mid)]
        # Sort by importance (highest first) and then timestamp (newest first)
        importance_weights = {"CRITICAL": 5, "HIGH": 4, "MEDIUM": 3, "LOW": 2, "TEMPORARY": 1}
        results.sort(key=lambda x: (importance_weights.get(x.importance, 0), x.timestamp), reverse=True)
        return results

memory_retrieval = MemoryRetrieval()
