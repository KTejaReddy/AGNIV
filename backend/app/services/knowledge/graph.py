import networkx as nx
from typing import Dict, List, Any

class KnowledgeGraph:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_node(self, node_id: str, node_type: str, metadata: dict):
        self.graph.add_node(node_id, type=node_type, **metadata)

    def add_edge(self, source_id: str, target_id: str, relation: str):
        self.graph.add_edge(source_id, target_id, relation=relation)

    def get_visualization_data(self) -> Dict[str, List[Any]]:
        """
        Converts to format expected by react-force-graph-2d
        """
        nodes = []
        for node_id, data in self.graph.nodes(data=True):
            node_data = {"id": node_id, "name": node_id}
            node_data.update(data)
            nodes.append(node_data)
            
        links = []
        for source, target, data in self.graph.edges(data=True):
            links.append({
                "source": source,
                "target": target,
                "label": data.get("relation", "")
            })
            
        return {"nodes": nodes, "links": links}

knowledge_graph = KnowledgeGraph()
