"""
Sample UI Panel Extension — Focus Timer
========================================
Demonstrates how a UI Panel extension registers its configuration
metadata so the AGNIV frontend can render the panel. The actual
UI rendering happens in the frontend (React component), while this
backend module handles state, events, and notifications.
"""
import time


class Extension:
    def __init__(self, sdk):
        self.sdk = sdk
        self._timer_active = False
        self._session_count = 0

    def on_enable(self):
        self.sdk.subscribe("FOCUS_TIMER_START", self._on_start)
        self.sdk.subscribe("FOCUS_TIMER_STOP", self._on_stop)
        self.sdk.log("Focus Timer Panel enabled.")

    def on_disable(self):
        self._timer_active = False
        self.sdk.log("Focus Timer Panel disabled.")

    def _on_start(self, event):
        self._timer_active = True
        self._session_count += 1
        self.sdk.log(f"Focus session #{self._session_count} started.")

    def _on_stop(self, event):
        self._timer_active = False
        self.sdk.log(f"Focus session ended. Total sessions: {self._session_count}")

    def metadata(self) -> dict:
        return {
            "panel_id": "focus_timer",
            "panel_title": "Focus Timer",
            "panel_icon": "Timer",
            "panel_position": "sidebar",
            "timer_active": self._timer_active,
            "session_count": self._session_count,
            "ui_component": "FocusTimerPanel",  # Frontend React component name
        }
