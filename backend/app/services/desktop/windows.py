import pygetwindow as gw
from app.core.engine.capability_manager import capability_manager

async def list_open_windows(params):
    windows = [w.title for w in gw.getAllWindows() if w.title]
    return {"status": "success", "windows": windows}

async def focus_window(params):
    title = params.get("title")
    windows = gw.getWindowsWithTitle(title)
    if windows:
        windows[0].activate()
        return {"status": "success", "title": title}
    return {"status": "failed", "reason": "Window not found"}

async def minimize_window(params):
    title = params.get("title")
    windows = gw.getWindowsWithTitle(title)
    if windows:
        windows[0].minimize()
        return {"status": "success"}
    return {"status": "failed", "reason": "Window not found"}

async def maximize_window(params):
    title = params.get("title")
    windows = gw.getWindowsWithTitle(title)
    if windows:
        windows[0].maximize()
        return {"status": "success"}
    return {"status": "failed", "reason": "Window not found"}

async def restore_window(params):
    title = params.get("title")
    windows = gw.getWindowsWithTitle(title)
    if windows:
        windows[0].restore()
        return {"status": "success"}
    return {"status": "failed", "reason": "Window not found"}

async def close_window(params):
    title = params.get("title")
    windows = gw.getWindowsWithTitle(title)
    if windows:
        windows[0].close()
        return {"status": "success"}
    return {"status": "failed", "reason": "Window not found"}

def register():
    capability_manager.register_capability("LIST_WINDOWS", "1.0", "Lists open window titles", list_open_windows)
    capability_manager.register_capability("FOCUS_WINDOW", "1.0", "Brings a window to front", focus_window)
    capability_manager.register_capability("MINIMIZE_WINDOW", "1.0", "Minimizes a window", minimize_window)
    capability_manager.register_capability("MAXIMIZE_WINDOW", "1.0", "Maximizes a window", maximize_window)
    capability_manager.register_capability("RESTORE_WINDOW", "1.0", "Restores a window", restore_window)
    capability_manager.register_capability("CLOSE_WINDOW", "1.0", "Closes a window", close_window)
