import asyncio
from app.core.logging import logger
from .graph import knowledge_graph
from .cache import knowledge_cache

class KnowledgeManager:
    def __init__(self):
        pass

    def add_knowledge(self, node_id: str, node_type: str, metadata: dict):
        knowledge_graph.add_node(node_id, node_type, metadata)
        knowledge_cache.set(node_id, {"type": node_type, "metadata": metadata})

    def add_relationship(self, source: str, target: str, relation: str):
        knowledge_graph.add_edge(source, target, relation)

    def get_graph_data(self):
        return knowledge_graph.get_visualization_data()

knowledge_manager = KnowledgeManager()
