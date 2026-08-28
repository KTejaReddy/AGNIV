from .models import AccessibilitySettings, AccessibilityProfile
from app.core.engine.event_bus import event_bus, Event
import time

class AccessibilityManager:
    def __init__(self):
        self.settings = AccessibilitySettings()

    def get_profile(self) -> AccessibilityProfile:
        return self.settings.profile

    def update_profile(self, profile: AccessibilityProfile):
        self.settings.profile = profile
        # Auto-configure based on profile
        if profile == AccessibilityProfile.DEAF:
            self.settings.sign_recognition_enabled = True
            self.settings.live_captions_enabled = True
            self.settings.screen_reader_enabled = False
        elif profile == AccessibilityProfile.BLIND:
            self.settings.screen_reader_enabled = True
            self.settings.sign_recognition_enabled = False
            self.settings.live_captions_enabled = False
        elif profile == AccessibilityProfile.MOTOR:
            self.settings.gesture_confirmations_enabled = True
            
        import asyncio
        try:
            loop = asyncio.get_running_loop()
            loop.create_task(self._publish_profile_change())
        except RuntimeError:
            pass

    async def _publish_profile_change(self):
        await event_bus.publish(Event(
            id=f"evt_{time.time()}",
            type="ACCESSIBILITY_PROFILE_CHANGED",
            source="AccessibilityManager",
            payload={"profile": self.settings.profile.value},
            timestamp=time.time()
        ))

    def get_settings(self) -> AccessibilitySettings:
        return self.settings

    def update_settings(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self.settings, key):
                setattr(self.settings, key, value)

accessibility_manager = AccessibilityManager()
