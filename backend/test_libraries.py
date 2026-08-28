import time
import os
import psutil
import ctypes
import numpy as np
import cv2

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

def run_test(library, duration=60):
    pid = os.getpid()
    process = psutil.Process(pid)
    
    start_rss = process.memory_info().rss / (1024 * 1024)
    start_gdi, start_user = get_gui_resources(pid)
    start_handles = process.num_handles()
    start_threads = process.num_threads()
    
    print(f"\n--- Testing {library.upper()} for {duration} seconds ---")
    
    frame_count = 0
    start_time = time.time()
    last_print = start_time
    
    if library == 'mss':
        import mss
        sct = mss.mss()
        native_monitor = sct.monitors[1]
        monitor = {"top": native_monitor["top"], "left": native_monitor["left"], "width": native_monitor["width"], "height": native_monitor["height"]}
    elif library == 'dxcam':
        import dxcam
        camera = dxcam.create()
        camera.start(target_fps=60)
        
    try:
        while time.time() - start_time < duration:
            t0 = time.time()
            if library == 'mss':
                sct_img = sct.grab(monitor)
                img = np.array(sct_img)
                latest_frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
                del sct_img
                del img
            elif library == 'dxcam':
                frame = camera.get_latest_frame()
                if frame is not None:
                    latest_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                else:
                    time.sleep(0.001)
                    continue
            
            latency = (time.time() - t0) * 1000
            frame_count += 1
            
            # Print every minute (or 10s for short tests)
            if time.time() - last_print > 10:
                last_print = time.time()
                rss = process.memory_info().rss / (1024 * 1024)
                gdi, user = get_gui_resources(pid)
                handles = process.num_handles()
                fps = frame_count / (time.time() - start_time)
                
                print(f"[{time.time()-start_time:.0f}s] RSS: {rss:.1f}MB | GDI: {gdi} | USER: {user} | Handles: {handles} | FPS: {fps:.1f} | Latency: {latency:.1f}ms")
                
        # Final Stats
        rss = process.memory_info().rss / (1024 * 1024)
        gdi, user = get_gui_resources(pid)
        handles = process.num_handles()
        threads = process.num_threads()
        
        print("\n--- RESULTS ---")
        print(f"RSS Growth: {rss - start_rss:.2f} MB")
        print(f"GDI Delta: {gdi - start_gdi}")
        print(f"USER Delta: {user - start_user}")
        print(f"Handle Delta: {handles - start_handles}")
        print(f"Thread Delta: {threads - start_threads}")
        
    finally:
        if library == 'dxcam':
            camera.stop()

if __name__ == "__main__":
    import sys
    run_test(sys.argv[1], int(sys.argv[2]))
