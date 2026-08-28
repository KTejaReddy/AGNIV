from fastapi import APIRouter
from app.services.knowledge.manager import knowledge_manager
from app.services.knowledge.search import knowledge_search

router = APIRouter()

@router.get("/graph")
def get_graph():
    return knowledge_manager.get_graph_data()

@router.get("/search")
def search_knowledge(q: str = ""):
    if not q:
        return []
    return knowledge_search.search(q)
