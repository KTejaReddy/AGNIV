import os
import subprocess
import psutil
from app.core.engine.capability_manager import capability_manager
from app.core.logging import logger

async def open_application(params):
    app_path = params.get("path")
    if not app_path:
        raise ValueError("Missing 'path' parameter")
    # Async execution using subprocess
    subprocess.Popen([app_path], shell=True)
    return {"status": "success", "message": f"Opened {app_path}"}

async def close_application(params):
    app_name = params.get("name")
    if not app_name:
        raise ValueError("Missing 'name' parameter")
    closed = 0
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] and app_name.lower() in proc.info['name'].lower():
            try:
                proc.kill()
                closed += 1
            except Exception:
                pass
    return {"status": "success", "closed_count": closed}

async def restart_application(params):
    await close_application(params)
    app_path = params.get("path")
    if app_path:
        await open_application({"path": app_path})
    return {"status": "success", "message": "Restarted application"}

async def detect_applications(params):
    apps = set()
    for proc in psutil.process_iter(['name']):
        if proc.info['name']:
            apps.add(proc.info['name'])
    return {"status": "success", "applications": list(apps)}

def register():
    capability_manager.register_capability("OPEN_APPLICATION", "1.0", "Opens an application by path", open_application)
    capability_manager.register_capability("CLOSE_APPLICATION", "1.0", "Closes an application by name", close_application)
    capability_manager.register_capability("RESTART_APPLICATION", "1.0", "Restarts an application", restart_application)
    capability_manager.register_capability("DETECT_APPLICATIONS", "1.0", "Lists running applications", detect_applications)
