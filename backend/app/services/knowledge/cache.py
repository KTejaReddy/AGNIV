class KnowledgeCache:
    def __init__(self):
        self.store = {}

    def get(self, key: str):
        return self.store.get(key)

    def set(self, key: str, value: dict):
        self.store[key] = value

    def clear(self):
        self.store.clear()

knowledge_cache = KnowledgeCache()
