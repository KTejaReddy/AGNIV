from .manager import accessibility_manager
from app.core.engine.event_bus import event_bus
from app.core.logging import logger

class GestureConfirmationManager:
    async def start(self):
        event_bus.subscribe("PERCEPTION_GESTURE", self._on_gesture)
        logger.info("Gesture Confirmation Manager started")

    def _on_gesture(self, event):
        if not accessibility_manager.get_settings().gesture_confirmations_enabled:
            return
            
        gesture = event.payload.get("gesture")
        # We hook into Interaction Engine conceptually.
        # Thumbs up = Confirm, Head Shake = Cancel
        if gesture in ["thumbs_up", "head_nod"]:
            logger.info("Accessibility: Auto-confirming action via gesture.")
            # Emit a semantic confirmation
        elif gesture in ["thumbs_down", "head_shake", "stop"]:
            logger.info("Accessibility: Auto-rejecting action via gesture.")

gesture_confirmations = GestureConfirmationManager()
