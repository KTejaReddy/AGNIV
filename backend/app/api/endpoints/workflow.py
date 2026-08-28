from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.workflow.registry import workflow_registry
from app.services.workflow.queue_manager import workflow_queue
from app.services.workflow.manager import workflow_manager

router = APIRouter()

class RunTemplateRequest(BaseModel):
    template_id: str

@router.get("/")
def get_workflows():
    return workflow_queue.get_all()

@router.get("/templates")
def get_templates():
    return workflow_registry.list_templates()

@router.post("/run")
def run_workflow(req: RunTemplateRequest):
    res = workflow_manager.run_template(req.template_id)
    if not res:
        raise HTTPException(status_code=404, detail="Template not found")
    if "error" in res:
        raise HTTPException(status_code=400, detail=res["error"])
    return res

@router.post("/{instance_id}/pause")
def pause_workflow(instance_id: str):
    if workflow_manager.pause(instance_id):
        return {"status": "paused"}
    raise HTTPException(status_code=404, detail="Instance not found or not running")

@router.post("/{instance_id}/resume")
def resume_workflow(instance_id: str):
    if workflow_manager.resume(instance_id):
        return {"status": "resumed"}
    raise HTTPException(status_code=404, detail="Instance not found or not paused")

@router.post("/{instance_id}/cancel")
def cancel_workflow(instance_id: str):
    if workflow_manager.cancel(instance_id):
        return {"status": "cancelled"}
    raise HTTPException(status_code=404, detail="Instance not found")
