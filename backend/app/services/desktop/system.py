import os
import ctypes
import screen_brightness_control as sbc
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from app.core.engine.capability_manager import capability_manager

async def set_volume(params):
    level = params.get("level", 50)
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    # Pycaw takes a scalar from 0.0 to 1.0 for volume level, but set_volume uses scalar
    volume.SetMasterVolumeLevelScalar(level / 100.0, None)
    return {"status": "success", "level": level}

async def mute_volume(params):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMute(1, None)
    return {"status": "success"}

async def set_brightness(params):
    level = params.get("level", 50)
    try:
        sbc.set_brightness(level)
        return {"status": "success", "level": level}
    except Exception as e:
        return {"status": "failed", "reason": str(e)}

async def lock_workstation(params):
    ctypes.windll.user32.LockWorkStation()
    return {"status": "success"}

async def sleep_system(params):
    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
    return {"status": "success"}

async def shutdown_system(params):
    os.system("shutdown /s /t 1")
    return {"status": "success"}

async def restart_system(params):
    os.system("shutdown /r /t 1")
    return {"status": "success"}

def register():
    capability_manager.register_capability("VOLUME_SET", "1.0", "Sets system volume (0-100)", set_volume)
    capability_manager.register_capability("VOLUME_MUTE", "1.0", "Mutes system volume", mute_volume)
    capability_manager.register_capability("BRIGHTNESS_SET", "1.0", "Sets screen brightness (0-100)", set_brightness)
    capability_manager.register_capability("LOCK_WORKSTATION", "1.0", "Locks the workstation", lock_workstation)
    capability_manager.register_capability("SLEEP", "1.0", "Puts the system to sleep", sleep_system)
    capability_manager.register_capability("SHUTDOWN", "1.0", "Shuts down the system", shutdown_system)
    capability_manager.register_capability("RESTART", "1.0", "Restarts the system", restart_system)
