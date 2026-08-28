import pygetwindow as gw
import asyncio
import uuid
import time
from app.core.engine import event_bus, Event
from app.core.logging import logger
from .session import screen_session

class WindowManager:
    def __init__(self):
        self.last_active_title = None

    def get_active_window(self):
        try:
            active = gw.getActiveWindow()
            if active:
                return {
                    "title": active.title,
                    "left": active.left,
                    "top": active.top,
                    "width": active.width,
                    "height": active.height,
                    "isActive": active.isActive,
                    "isMinimized": active.isMinimized,
                    "isMaximized": active.isMaximized
                }
        except Exception as e:
            logger.error(f"Failed to get active window: {e}")
        return None

    def list_windows(self):
        try:
            return [{"title": w.title} for w in gw.getAllWindows() if w.title]
        except Exception as e:
            logger.error(f"Failed to list windows: {e}")
            return []

    def check_for_changes(self, loop=None):
        active = self.get_active_window()
        if not active:
            return

        screen_session.update_state("active_window", active)

        if active["title"] != self.last_active_title:
            self.last_active_title = active["title"]
            now = time.time()
            
            if loop:
                event_bus.publish_threadsafe(Event(
                        id=str(uuid.uuid4()),
                        type="WINDOW_CHANGED",
                        source="WindowManager",
                        payload={"window": active},
                        timestamp=now
                    ))

window_manager = WindowManager()
