from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from typing import Any, Dict
from app.services.perception.session import perception_session
from app.services.perception.camera import camera_manager
from app.core.engine.input_manager import input_manager, InputType
import cv2
import time
import asyncio

router = APIRouter()

@router.get("/status")
def get_perception_status():
    return perception_session.get_status()

@router.get("/devices")
def get_devices():
    return {
        "cameras": camera_manager.get_available_cameras()
    }

def generate_mjpeg():
    while True:
        if not camera_manager.is_running or camera_manager.latest_processed_frame is None:
            time.sleep(0.1)
            continue
            
        ret, buffer = cv2.imencode('.jpg', camera_manager.latest_processed_frame)
        if not ret:
            continue
            
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        
        # Limit to 30 FPS for stream transmission
        time.sleep(1/30.0)

@router.get("/video_feed")
def video_feed():
    return StreamingResponse(generate_mjpeg(), media_type="multipart/x-mixed-replace; boundary=frame")

@router.post("/action")
async def execute_perception_action(payload: Dict[str, Any]):
    action = payload.get("action")
    await input_manager.route_input(
        InputType.REST,
        {"action": action, "parameters": payload.get("parameters", {})}
    )
    return {"status": "dispatched"}
