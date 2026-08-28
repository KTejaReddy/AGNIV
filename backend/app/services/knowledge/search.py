from .manager import knowledge_manager
from .graph import knowledge_graph

class KnowledgeSearch:
    def __init__(self):
        pass

    def search(self, query: str) -> list:
        query = query.lower()
        results = []
        for node_id, data in knowledge_graph.graph.nodes(data=True):
            # Basic keyword match on ID and description
            if query in node_id.lower() or query in data.get("description", "").lower():
                results.append({"id": node_id, "data": data})
        return results

knowledge_search = KnowledgeSearch()
