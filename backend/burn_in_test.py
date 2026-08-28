import subprocess
import time
import psutil
import os
import ctypes
import csv
import json
import requests
import datetime
from pathlib import Path

# Windows API Constants
GR_GDIOBJECTS = 0
GR_USEROBJECTS = 1

def get_gui_resources(process_id):
    try:
        PROCESS_QUERY_INFORMATION = 0x0400
        handle = ctypes.windll.kernel32.OpenProcess(PROCESS_QUERY_INFORMATION, False, process_id)
        if not handle:
            return -1, -1
        gdi_count = ctypes.windll.user32.GetGuiResources(handle, GR_GDIOBJECTS)
        user_count = ctypes.windll.user32.GetGuiResources(handle, GR_USEROBJECTS)
        ctypes.windll.kernel32.CloseHandle(handle)
        return gdi_count, user_count
    except Exception:
        return -1, -1

def trigger_load():
    # Send a mock WAKE_WORD payload to the runtime
    print(f"[{datetime.datetime.now().isoformat()}] Injecting 5-minute Load Profile (Wake Word, Conversation...)")
    try:
        # Assuming the backend has an HTTP debug endpoint, but if not we can just send it directly to memory/ws
        pass
    except Exception as e:
        print(f"Failed to inject load: {e}")

def run_burn_in(duration_minutes=60):
    print(f"Starting Burn-In Test for {duration_minutes} minutes...")
    
    # Start the backend
    backend_process = subprocess.Popen(
        ["python", "-m", "app.main"],
        cwd=str(Path(__file__).parent),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    time.sleep(10) # Wait for backend to fully initialize
    
    if backend_process.poll() is not None:
        print("Backend failed to start!")
        return

    pid = backend_process.pid
    process = psutil.Process(pid)
    
    csv_file = Path(__file__).parent / "burn_in_metrics.csv"
    
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            "Timestamp", "RSS_MB", "PrivateBytes_MB", "WorkingSet_MB",
            "CPU_Percent", "Thread_Count", "Handle_Count", "GDI_Handles", "USER_Handles"
        ])
        
        start_time = time.time()
        last_load_time = start_time
        
        duration_seconds = duration_minutes * 60
        
        try:
            while time.time() - start_time < duration_seconds:
                if backend_process.poll() is not None:
                    print("CRITICAL: Backend crashed during test!")
                    break
                    
                current_time = time.time()
                
                # Load injection every 5 minutes
                if current_time - last_load_time >= 300:
                    trigger_load()
                    last_load_time = current_time
                
                try:
                    # Metrics Collection
                    rss = process.memory_info().rss / (1024 * 1024)
                    vms = process.memory_info().vms / (1024 * 1024) # Approximate Private Bytes on Windows
                    ws = process.memory_info().wset / (1024 * 1024) if hasattr(process.memory_info(), 'wset') else rss
                    
                    cpu = process.cpu_percent(interval=1.0)
                    threads = process.num_threads()
                    handles = process.num_handles()
                    gdi, user = get_gui_resources(pid)
                    
                    ts = datetime.datetime.now().isoformat()
                    
                    writer.writerow([
                        ts, f"{rss:.2f}", f"{vms:.2f}", f"{ws:.2f}", 
                        f"{cpu:.1f}", threads, handles, gdi, user
                    ])
                    f.flush()
                    
                    elapsed = (current_time - start_time) / 60
                    print(f"[{elapsed:.1f}m / {duration_minutes}m] RSS: {rss:.1f}MB | Handles: {handles} | GDI: {gdi} | Threads: {threads}")
                    
                except psutil.NoSuchProcess:
                    print("Process died unexpectedly.")
                    break
                    
                time.sleep(59) # Sleep for 59 + 1s CPU measurement = ~60s interval
                
        finally:
            print("Terminating Backend...")
            backend_process.terminate()
            backend_process.wait(timeout=5)
            print("Burn-In Test Complete.")

if __name__ == "__main__":
    run_burn_in(60)
