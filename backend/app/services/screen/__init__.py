from app.core.engine.capability_manager import capability_manager
from app.core.logging import logger
from .manager import screen_manager
from .session import screen_session
from .window import window_manager
from .ui_analyzer import ui_analyzer
from .ocr import ocr_engine
import asyncio
from app.core.engine import event_bus, Event
import uuid
import time

async def start_screen_capture_cap(params):
    monitor = int(params.get("monitor", 1))
    screen_manager.start(monitor)
    return {"status": "success"}

async def stop_screen_capture_cap(params):
    screen_manager.stop()
    return {"status": "success"}

async def read_ui_tree_cap(params):
    tree = ui_analyzer.extract_ui_tree()
    screen_session.update_state("ui_tree", tree)
    
    await event_bus.publish(Event(
        id=str(uuid.uuid4()),
        type="UI_UPDATED",
        source="ScreenEngine",
        payload={"tree": tree},
        timestamp=time.time()
    ))
    return {"status": "success", "tree": tree}

async def run_ocr_cap(params):
    monitor = int(params.get("monitor", 1))
    img = screen_manager.capture_single(monitor)
    results = ocr_engine.run_ocr_on_image(img)
    
    await event_bus.publish(Event(
        id=str(uuid.uuid4()),
        type="OCR_COMPLETED",
        source="ScreenEngine",
        payload={"results": results},
        timestamp=time.time()
    ))
    return {"status": "success", "results": results}

async def list_windows_cap(params):
    return {"windows": window_manager.list_windows()}

async def read_active_window_cap(params):
    return {"window": window_manager.get_active_window()}

def register_screen_capabilities():
    logger.info("Registering Screen Intelligence Capabilities...")
    capability_manager.register_capability("START_SCREEN_CAPTURE", "1.0", "Starts continuous screen capture", start_screen_capture_cap)
    capability_manager.register_capability("STOP_SCREEN_CAPTURE", "1.0", "Stops screen capture", stop_screen_capture_cap)
    capability_manager.register_capability("READ_UI_TREE", "1.0", "Extracts structured UIA tree of active window", read_ui_tree_cap)
    capability_manager.register_capability("RUN_OCR", "1.0", "Runs OCR on the current screen", run_ocr_cap)
    capability_manager.register_capability("LIST_WINDOWS", "1.0", "Lists all open windows", list_windows_cap)
    capability_manager.register_capability("READ_ACTIVE_WINDOW", "1.0", "Reads the current active window properties", read_active_window_cap)
    logger.info("Screen Intelligence Capabilities registered successfully.")
