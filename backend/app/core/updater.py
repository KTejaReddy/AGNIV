"""
Auto-Update Architecture.
Periodically checks for a new version and prompts the user.
"""
import aiohttp
import asyncio
from app.core.logging import logger
from app.core.engine.event_bus import event_bus, Event
import time
import uuid

UPDATE_MANIFEST_URL = "https://raw.githubusercontent.com/agniv-ai/agniv/main/version.json"
CURRENT_VERSION = "1.0.0"

class AutoUpdater:
    def __init__(self):
        self.running = False
        self._task = None

    async def start(self):
        self.running = True
        self._task = asyncio.create_task(self._update_loop())
        logger.info("[Updater] Auto-updater started.")

    async def stop(self):
        self.running = False
        if self._task:
            self._task.cancel()
        logger.info("[Updater] Auto-updater stopped.")

    async def check_for_updates(self) -> dict:
        """Check the manifest URL for a newer version."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(UPDATE_MANIFEST_URL, timeout=5) as response:
                    if response.status == 200:
                        manifest = await response.json()
                        latest = manifest.get("latest_version", "1.0.0")
                        download_url = manifest.get("download_url", "")
                        
                        if latest > CURRENT_VERSION:
                            logger.info(f"[Updater] New version found: {latest}")
                            return {"update_available": True, "version": latest, "url": download_url}
        except Exception as e:
            logger.warning(f"[Updater] Failed to check for updates: {e}")
            
        return {"update_available": False}

    async def _update_loop(self):
        while self.running:
            # Check every 24 hours
            await asyncio.sleep(86400)
            
            result = await self.check_for_updates()
            if result.get("update_available"):
                await event_bus.publish(Event(
                    id=str(uuid.uuid4()),
                    type="SYSTEM_NOTIFICATION",
                    source="Updater",
                    payload={
                        "title": "AGNIV Update Available",
                        "message": f"Version {result['version']} is available. Would you like to update?",
                        "action_url": result["url"]
                    },
                    timestamp=time.time()
                ))

auto_updater = AutoUpdater()
