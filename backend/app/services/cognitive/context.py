import time
from typing import Dict, Any
# Import active sessions from other engines safely
from app.services.screen.session import screen_session
from app.services.perception.session import perception_session
from app.core.engine.task_manager import task_manager
from app.services.memory.retrieval import memory_retrieval

class ContextBuilder:
    def __init__(self):
        pass

    def build_unified_context(self, user_input: str = "") -> Dict[str, Any]:
        """
        Collects lightweight context from all AGNIV modules.
        Avoids passing massive image blobs, only structured metadata.
        """
        context = {
            "timestamp": time.time(),
            "screen": {
                "active_window": screen_session.state.get("active_window"),
                "ocr_count": len(screen_session.state.get("ocr_results", []) or []),
                "ui_tree_active": screen_session.state.get("ui_tree") is not None
            },
            "perception": {
                "gesture": perception_session.current_state.get("gesture"),
                "face_state": perception_session.current_state.get("face_state")
            },
            "system": {
                "running_tasks": [t["id"] for t in task_manager.list_tasks()]
            },
            "memory": []
        }
        
        # Inject retrieved memory if input provided
        if user_input:
            try:
                memories = memory_retrieval.search(user_input)
                if memories:
                    context["memory"] = [
                        {"title": m.title, "summary": m.summary, "type": m.type} 
                        for m in memories[:3]
                    ]
            except Exception as e:
                pass # safe fail
                
        return context

context_builder = ContextBuilder()
