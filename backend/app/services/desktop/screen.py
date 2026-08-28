import os
import time
from mss import mss
from app.core.engine.capability_manager import capability_manager

async def screenshot(params):
    path = params.get("path", f"screenshot_{int(time.time())}.png")
    with mss() as sct:
        sct.shot(output=path)
    return {"status": "success", "path": path}

async def list_displays(params):
    with mss() as sct:
        monitors = sct.monitors
    return {"status": "success", "displays": monitors}

async def screen_resolution(params):
    with mss() as sct:
        primary = sct.monitors[1] # Monitor 1 is primary
        res = {"width": primary["width"], "height": primary["height"]}
    return {"status": "success", "resolution": res}

def register():
    capability_manager.register_capability("SCREENSHOT", "1.0", "Takes a screenshot", screenshot)
    capability_manager.register_capability("LIST_DISPLAYS", "1.0", "Lists connected displays", list_displays)
    capability_manager.register_capability("SCREEN_RESOLUTION", "1.0", "Gets primary screen resolution", screen_resolution)
