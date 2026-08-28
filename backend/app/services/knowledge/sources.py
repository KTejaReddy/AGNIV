from app.core.engine.capability_manager import capability_manager
from .manager import knowledge_manager

class KnowledgeSources:
    def seed_initial_knowledge(self):
        # 1. Root Nodes
        knowledge_manager.add_knowledge("AGNIV", "SYSTEM", {"description": "Core OS Companion"})
        knowledge_manager.add_knowledge("CAPABILITIES", "CATEGORY", {"description": "Registered Actions"})
        knowledge_manager.add_relationship("AGNIV", "CAPABILITIES", "contains")

        # 2. Extract capabilities dynamically
        for cap_name, cap_data in capability_manager.capabilities.items():
            desc = cap_data.get("description", "")
            knowledge_manager.add_knowledge(cap_name, "CAPABILITY", {"description": desc})
            knowledge_manager.add_relationship("CAPABILITIES", cap_name, "supports")

        # 3. Add some mocked App Knowledge
        knowledge_manager.add_knowledge("CHROME", "APPLICATION", {"description": "Web Browser"})
        knowledge_manager.add_knowledge("OPEN_URL", "CAPABILITY", {"description": "Open a web page"})
        knowledge_manager.add_relationship("CHROME", "OPEN_URL", "uses")

knowledge_sources = KnowledgeSources()
