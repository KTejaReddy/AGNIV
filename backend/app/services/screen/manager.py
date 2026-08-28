import mss
import threading
import time
import asyncio
import uuid
import cv2
import numpy as np
from app.core.logging import logger
from app.core.engine import event_bus, Event
from .session import screen_session
from .window import window_manager

class ScreenManager:
    def __init__(self):
        self.sct = mss.mss()
        self.is_running = False
        self._thread = None
        self.latest_frame = None
        self._loop = None

    def get_monitors(self):
        # mss.monitors[0] is the bounding box of all monitors combined.
        # monitors[1:] are the actual individual monitors.
        return self.sct.monitors[1:]

    def start(self, monitor_index: int = 1):
        if self.is_running:
            return
            
        try:
            logger.info(f"Monitor detected and attempting to capture: {monitor_index}")
            screen_session.active = True
            screen_session.current_monitor = monitor_index
            self.is_running = True
            
            logger.info("Screen capture initialized")
            
            self._loop = asyncio.get_running_loop()
            
            self._thread = threading.Thread(target=self._worker, daemon=True)
            self._thread.start()
            logger.info(f"Capture thread started for monitor {monitor_index}")
        except Exception as e:
            logger.error(f"Exact screen capture initialization exception: {e}", exc_info=True)
            self.is_running = False
            return
        
        event_bus.publish_threadsafe(Event(
                id=str(uuid.uuid4()),
                type="SCREEN_CAPTURE_STARTED",
                source="ScreenManager",
                payload={"monitor": monitor_index},
                timestamp=time.time()
            ))

    def stop(self):
        self.is_running = False
        screen_session.active = False
        if self._thread:
            self._thread.join(timeout=1.0)
            
        logger.info("Screen capture stopped")
        event_bus.publish_threadsafe(Event(
                id=str(uuid.uuid4()),
                type="SCREEN_CAPTURE_STOPPED",
                source="ScreenManager",
                payload={},
                timestamp=time.time()
            ))

    def capture_single(self, monitor_index: int = 1):
        monitor = self.sct.monitors[monitor_index]
        sct_img = self.sct.grab(monitor)
        # Convert to BGR format for cv2 consistency
        img = np.array(sct_img)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        return img

    def _worker(self):
        prev_time = time.time()
        # We use dxcam on Windows to completely avoid GDI and memory leaks associated with mss
        try:
            import dxcam
            camera = dxcam.create(output_color="BGRA")
            camera.start(target_fps=30)
            
            while self.is_running:
                try:
                    start_proc = time.time()
                    
                    # Check for active window changes periodically
                    window_manager.check_for_changes(self._loop)
                    
                    # Capture frame via Desktop Duplication API (GPU)
                    frame = camera.get_latest_frame()
                    if frame is not None:
                        # Convert BGRA to BGR directly
                        self.latest_frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                    else:
                        time.sleep(0.005) # Prevent 100% CPU lock when waiting for GPU frame
                        
                    # Calculate FPS & Latency
                    curr_time = time.time()
                    fps = 1.0 / (curr_time - prev_time + 1e-9)
                    prev_time = curr_time
                    
                    screen_session.fps = int(fps)
                    screen_session.latency = int((time.time() - start_proc) * 1000)
                    frame_count += 1
                    if frame_count % 30 == 0:
                        pass # avoid spamming logs
                    
                    # Sleep to throttle to ~30 fps to save CPU
                    time.sleep(1/30.0)
                    
                except Exception as e:
                    logger.error(f"Error in screen capture loop: {e}")
                    time.sleep(1.0)
            
            camera.stop()
            
        except Exception as startup_error:
            logger.warning(f"Failed to initialize dxcam (headless mode/no GPU?): {startup_error}")
            # Fallback for sandbox / headless environments
            while self.is_running:
                dummy = np.zeros((1080, 1920, 3), dtype=np.uint8)
                cv2.putText(dummy, f'DXCam Failed: Sandbox/Headless', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                self.latest_frame = dummy
                time.sleep(0.033)

screen_manager = ScreenManager()
