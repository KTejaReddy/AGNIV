from fastapi import APIRouter
from typing import Any, Dict
from app.core.engine.input_manager import input_manager, InputType

router = APIRouter()

async def dispatch_desktop_action(capability: str, params: Dict[str, Any]):
    # Route via the core engine just as an AI would
    await input_manager.route_input(
        InputType.REST, 
        {"action": capability, "parameters": params}
    )
    return {"status": "dispatched", "capability": capability}

@router.post("/apps/{action}")
async def apps_endpoint(action: str, params: Dict[str, Any] = {}):
    capability_map = {
        "open": "OPEN_APPLICATION",
        "close": "CLOSE_APPLICATION",
        "restart": "RESTART_APPLICATION",
        "detect": "DETECT_APPLICATIONS"
    }
    return await dispatch_desktop_action(capability_map.get(action, action), params)

@router.post("/files/{action}")
async def files_endpoint(action: str, params: Dict[str, Any] = {}):
    capability_map = {
        "create_file": "CREATE_FILE",
        "create_folder": "CREATE_FOLDER",
        "rename": "RENAME_PATH",
        "copy": "COPY_PATH",
        "move": "MOVE_PATH",
        "delete": "DELETE_PATH",
        "read": "READ_TEXT_FILE",
        "search": "SEARCH_FILES",
        "open": "OPEN_FILE",
        "reveal": "REVEAL_IN_EXPLORER"
    }
    return await dispatch_desktop_action(capability_map.get(action, action), params)

@router.post("/system/{action}")
async def system_endpoint(action: str, params: Dict[str, Any] = {}):
    capability_map = {
        "volume": "VOLUME_SET",
        "mute": "VOLUME_MUTE",
        "brightness": "BRIGHTNESS_SET",
        "lock": "LOCK_WORKSTATION",
        "sleep": "SLEEP",
        "shutdown": "SHUTDOWN",
        "restart": "RESTART"
    }
    return await dispatch_desktop_action(capability_map.get(action, action), params)

@router.post("/windows/{action}")
async def windows_endpoint(action: str, params: Dict[str, Any] = {}):
    capability_map = {
        "list": "LIST_WINDOWS",
        "focus": "FOCUS_WINDOW",
        "minimize": "MINIMIZE_WINDOW",
        "maximize": "MAXIMIZE_WINDOW",
        "restore": "RESTORE_WINDOW",
        "close": "CLOSE_WINDOW"
    }
    return await dispatch_desktop_action(capability_map.get(action, action), params)

@router.post("/clipboard/{action}")
async def clipboard_endpoint(action: str, params: Dict[str, Any] = {}):
    capability_map = {
        "read": "READ_CLIPBOARD",
        "copy": "COPY_TEXT",
        "clear": "CLEAR_CLIPBOARD"
    }
    return await dispatch_desktop_action(capability_map.get(action, action), params)

@router.post("/screenshot")
async def screenshot_endpoint(params: Dict[str, Any] = {}):
    return await dispatch_desktop_action("SCREENSHOT", params)
