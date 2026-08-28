from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from typing import Any, Dict
from app.services.screen.session import screen_session
from app.services.screen.manager import screen_manager
from app.core.engine.input_manager import input_manager, InputType
import cv2
import time
import asyncio

router = APIRouter()

@router.get("/status")
def get_screen_status():
    return screen_session.get_status()

@router.get("/monitors")
def get_monitors():
    monitors = screen_manager.get_monitors()
    return {"monitors": [{"index": i+1, "width": m["width"], "height": m["height"]} for i, m in enumerate(monitors)]}

def generate_mjpeg():
    while True:
        if not screen_manager.is_running or screen_manager.latest_frame is None:
            time.sleep(0.1)
            continue
            
        # Scale down for fast streaming to frontend
        frame = cv2.resize(screen_manager.latest_frame, (1280, 720))
        ret, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 70])
        if not ret:
            continue
            
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        
        time.sleep(1/30.0)

@router.get("/video_feed")
def video_feed():
    return StreamingResponse(generate_mjpeg(), media_type="multipart/x-mixed-replace; boundary=frame")

@router.post("/action")
async def execute_screen_action(payload: Dict[str, Any]):
    action = payload.get("action")
    await input_manager.route_input(
        InputType.REST,
        {"action": action, "parameters": payload.get("parameters", {})}
    )
    return {"status": "dispatched"}
