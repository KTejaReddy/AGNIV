import cv2
import threading
import time
import asyncio
from app.core.logging import logger
from app.core.engine import event_bus, Event
import uuid
from .session import perception_session
from .hands import hand_tracker
from .face import face_tracker
from .body import body_tracker

class CameraManager:
    def __init__(self):
        self.cap = None
        self.is_running = False
        self._thread = None
        self.latest_frame = None
        self.latest_processed_frame = None
        self.current_camera_id = 0

    def get_available_cameras(self):
        # A quick check for cameras 0-4
        available = []
        for i in range(5):
            cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
            if cap.isOpened():
                available.append(i)
                cap.release()
        return available

    def start(self, camera_id: int = 0):
        if self.is_running:
            return
            
        self.current_camera_id = camera_id
        try:
            logger.info(f"Attempting to detect and select camera index: {camera_id}")
            self.cap = cv2.VideoCapture(camera_id, cv2.CAP_DSHOW)
            
            if not self.cap.isOpened():
                logger.error(f"Failed to open camera {camera_id}")
                return
                
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            
            width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            fps = self.cap.get(cv2.CAP_PROP_FPS)
            
            logger.info(f"Camera opened successfully")
            logger.info(f"Resolution: {width}x{height}, Target FPS: {fps}")
            
            self.is_running = True
            
            self._thread = threading.Thread(target=self._worker, daemon=True)
            self._thread.start()
            logger.info(f"Camera {camera_id} started. Tracking loop started.")
        except Exception as e:
            logger.error(f"Exact camera initialization exception: {e}", exc_info=True)
            self.is_running = False
            return
        
        event_bus.publish_threadsafe(Event(
                id=str(uuid.uuid4()),
                type="CAMERA_STARTED",
                source="CameraManager",
                payload={"camera_id": camera_id},
                timestamp=time.time()
            ))

    def stop(self):
        self.is_running = False
        if self._thread:
            self._thread.join(timeout=1.0)
        if self.cap:
            self.cap.release()
            
        logger.info("Camera stopped")
        event_bus.publish_threadsafe(Event(
                id=str(uuid.uuid4()),
                type="CAMERA_STOPPED",
                source="CameraManager",
                payload={},
                timestamp=time.time()
            ))

    def _worker(self):
        prev_time = time.time()
        mp_prev_time = time.time()
        first_frame = True
        while self.is_running and self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                time.sleep(0.1)
                continue
                
            if first_frame:
                logger.info("First camera frame read successfully. MediaPipe initialized.")
                first_frame = False
                
            self.latest_frame = frame.copy()
            
            # FPS Calculation (Capture)
            curr_time = time.time()
            capture_fps = 1.0 / (curr_time - prev_time + 1e-9)
            prev_time = curr_time
            perception_session.capture_fps = round(capture_fps, 2)
            
            # Process trackers sequentially
            start_proc = time.time()
            
            processed = frame.copy()
            processed = hand_tracker.process(processed)
            processed = face_tracker.process(processed)
            processed = body_tracker.process(processed)
            
            mp_curr_time = time.time()
            mediapipe_fps = 1.0 / (mp_curr_time - mp_prev_time + 1e-9)
            mp_prev_time = mp_curr_time
            
            perception_session.mediapipe_fps = round(mediapipe_fps, 2)
            perception_session.render_fps = 0.0 # No rendering loop in backend currently
            perception_session.latency = int((time.time() - start_proc) * 1000)
            self.latest_processed_frame = processed

camera_manager = CameraManager()
