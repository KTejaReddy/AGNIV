from fastapi import APIRouter, HTTPException
from app.services.memory.manager import memory_manager
from app.services.memory.retrieval import memory_retrieval

router = APIRouter()

@router.get("/")
def get_memories():
    return memory_manager.get_all()

@router.get("/search")
def search_memories(q: str):
    return memory_retrieval.search(q)

@router.delete("/{memory_id}")
def delete_memory(memory_id: str):
    memory_manager.delete_memory(memory_id)
    return {"status": "deleted"}
