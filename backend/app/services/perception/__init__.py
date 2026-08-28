from app.core.engine.capability_manager import capability_manager
from app.core.logging import logger
from .camera import camera_manager
from .session import perception_session

async def start_camera_cap(params):
    camera_id = int(params.get("camera_id", 0))
    camera_manager.start(camera_id)
    return {"status": "success"}

async def stop_camera_cap(params):
    camera_manager.stop()
    return {"status": "success"}

async def enable_hand_tracking_cap(params):
    enabled = params.get("enabled", True)
    perception_session.set_tracker_state("hands", enabled)
    return {"status": "success"}

async def enable_face_tracking_cap(params):
    enabled = params.get("enabled", True)
    perception_session.set_tracker_state("face", enabled)
    return {"status": "success"}

async def enable_body_tracking_cap(params):
    enabled = params.get("enabled", True)
    perception_session.set_tracker_state("body", enabled)
    return {"status": "success"}

async def enable_gesture_recognition_cap(params):
    enabled = params.get("enabled", True)
    perception_session.set_tracker_state("gestures", enabled)
    return {"status": "success"}

def register_perception_capabilities():
    logger.info("Registering Perception Capabilities...")
    capability_manager.register_capability("START_CAMERA", "1.0", "Starts camera feed", start_camera_cap)
    capability_manager.register_capability("STOP_CAMERA", "1.0", "Stops camera feed", stop_camera_cap)
    capability_manager.register_capability("ENABLE_HAND_TRACKING", "1.0", "Enables Hand tracking", enable_hand_tracking_cap)
    capability_manager.register_capability("ENABLE_FACE_TRACKING", "1.0", "Enables Face tracking", enable_face_tracking_cap)
    capability_manager.register_capability("ENABLE_BODY_TRACKING", "1.0", "Enables Body tracking", enable_body_tracking_cap)
    capability_manager.register_capability("ENABLE_GESTURE_RECOGNITION", "1.0", "Enables Gesture recognition", enable_gesture_recognition_cap)
    logger.info("Perception Capabilities registered successfully.")
