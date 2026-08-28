import ctypes
from ctypes import wintypes
import psutil
import os

pid = os.getpid()

# Windows API Constants
GR_GDIOBJECTS = 0
GR_USEROBJECTS = 1

def get_gui_resources(process_id):
    try:
        # Get handle to process
        PROCESS_QUERY_INFORMATION = 0x0400
        handle = ctypes.windll.kernel32.OpenProcess(PROCESS_QUERY_INFORMATION, False, process_id)
        if not handle:
            return -1, -1
            
        gdi_count = ctypes.windll.user32.GetGuiResources(handle, GR_GDIOBJECTS)
        user_count = ctypes.windll.user32.GetGuiResources(handle, GR_USEROBJECTS)
        
        ctypes.windll.kernel32.CloseHandle(handle)
        return gdi_count, user_count
    except Exception as e:
        return -1, -1

p = psutil.Process(pid)
gdi, user = get_gui_resources(pid)
print(f"GDI Handles: {gdi}, USER Handles: {user}, Open Handles: {p.num_handles()}")
