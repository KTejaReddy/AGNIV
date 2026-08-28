from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from app.services.extensions.manager import extension_manager
from app.services.extensions.validator import extension_validator
from app.services.extensions.models import ExtensionType

router = APIRouter()


@router.get("/")
def list_extensions():
    """List all installed extensions."""
    return [e.dict() for e in extension_manager.list_all()]


@router.get("/stats")
def get_stats():
    """Get extension ecosystem statistics."""
    return extension_manager.get_stats()


@router.get("/{ext_id}")
def get_extension(ext_id: str):
    ext = extension_manager.get(ext_id)
    if not ext:
        raise HTTPException(status_code=404, detail="Extension not found")
    return ext.dict()


@router.post("/{ext_id}/enable")
async def enable_extension(ext_id: str):
    ok, msg = await extension_manager.enable(ext_id)
    if not ok:
        raise HTTPException(status_code=400, detail=msg)
    return {"status": "success", "message": msg}


@router.post("/{ext_id}/disable")
async def disable_extension(ext_id: str):
    ok, msg = await extension_manager.disable(ext_id)
    if not ok:
        raise HTTPException(status_code=400, detail=msg)
    return {"status": "success", "message": msg}


@router.post("/{ext_id}/uninstall")
async def uninstall_extension(ext_id: str):
    ok, msg = await extension_manager.uninstall(ext_id)
    if not ok:
        raise HTTPException(status_code=400, detail=msg)
    return {"status": "success", "message": msg}


@router.post("/scan")
def rescan_extensions():
    """Trigger a rescan of the extensions/ directory for newly dropped packages."""
    count = extension_manager.rescan()
    return {"status": "success", "newly_loaded": count}


@router.post("/validate")
def validate_manifest(manifest: Dict[str, Any]):
    """Validate a manifest JSON without installing it."""
    from app.services.extensions.models import ExtensionManifest
    try:
        m = ExtensionManifest(**manifest)
    except Exception as e:
        return {"valid": False, "errors": [str(e)]}
    ok, errors = extension_validator.validate_manifest(m)
    return {"valid": ok, "errors": errors}
