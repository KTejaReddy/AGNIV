from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.skills.registry import skills_registry
from app.services.skills.manager import skills_manager

router = APIRouter()

class SkillActionRequest(BaseModel):
    skill_id: str

@router.get("/")
def get_skills():
    return skills_registry.list_skills()

@router.post("/run")
def run_skill(req: SkillActionRequest):
    res = skills_manager.run(req.skill_id)
    if "error" in res:
        raise HTTPException(status_code=400, detail=res["error"])
    return res

@router.post("/{skill_id}/enable")
def enable_skill(skill_id: str):
    if skills_manager.enable(skill_id):
        return {"status": "enabled"}
    raise HTTPException(status_code=404, detail="Skill not found")

@router.post("/{skill_id}/disable")
def disable_skill(skill_id: str):
    if skills_manager.disable(skill_id):
        return {"status": "disabled"}
    raise HTTPException(status_code=404, detail="Skill not found")
