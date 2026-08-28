"""
Background Service Supervisor.
Monitors asyncio tasks, handles restarts on crashes, and checks for memory leaks.
"""
import asyncio
import time
import psutil
import os
from typing import Callable, Dict, Any, Coroutine
from app.core.logging import logger
from .event_bus import event_bus, Event


class Supervisor:
    def __init__(self):
        self.services: Dict[str, dict] = {}
        self.running = False
        self._monitor_task = None
        self.process = psutil.Process(os.getpid())

    async def register_service(self, name: str, coro_func: Callable[[], Coroutine[Any, Any, None]], restart: bool = True):
        """Register a background service to be supervised."""
        self.services[name] = {
            "coro_func": coro_func,
            "task": None,
            "restart": restart,
            "crash_count": 0,
            "last_crash": 0,
            "running": False
        }
        logger.info(f"[Supervisor] Registered service: {name}")

    async def start_service(self, name: str):
        if name not in self.services:
            logger.error(f"[Supervisor] Service {name} not found.")
            return

        service = self.services[name]
        if service["running"]:
            return

        async def _wrapper():
            try:
                await service["coro_func"]()
            except asyncio.CancelledError:
                logger.info(f"[Supervisor] Service {name} cancelled.")
                raise
            except Exception as e:
                logger.error(f"[Supervisor] Service {name} CRASHED: {e}")
                service["crash_count"] += 1
                service["last_crash"] = time.time()
                service["running"] = False
                
                await event_bus.publish(Event(
                    id=f"crash_{name}_{time.time()}",
                    type="SERVICE_CRASHED",
                    source="Supervisor",
                    payload={"service": name, "error": str(e), "crash_count": service["crash_count"]},
                    timestamp=time.time()
                ))

                if service["restart"] and service["crash_count"] < 5:
                    logger.info(f"[Supervisor] Restarting service {name} in 5 seconds...")
                    await asyncio.sleep(5)
                    await self.start_service(name)
                else:
                    logger.error(f"[Supervisor] Service {name} exceeded max retries. Giving up.")

        service["task"] = asyncio.create_task(_wrapper())
        service["running"] = True
        logger.info(f"[Supervisor] Started service: {name}")

    async def start_all(self):
        self.running = True
        for name in self.services:
            await self.start_service(name)
        
        self._monitor_task = asyncio.create_task(self._monitor_loop())
        logger.info("[Supervisor] All services started. Monitor loop active.")

    async def _monitor_loop(self):
        while self.running:
            await asyncio.sleep(60)
            
            # Check memory usage
            try:
                mem_info = self.process.memory_info()
                rss_mb = mem_info.rss / (1024 * 1024)
                
                if rss_mb > 1024:  # 1GB limit for warning
                    logger.warning(f"[Supervisor] HIGH MEMORY USAGE detected: {rss_mb:.2f} MB")
                    await event_bus.publish(Event(
                        id=f"mem_warn_{time.time()}",
                        type="SYSTEM_WARNING",
                        source="Supervisor",
                        payload={"warning": "High memory usage", "rss_mb": rss_mb},
                        timestamp=time.time()
                    ))
            except Exception as e:
                logger.error(f"[Supervisor] Monitor error: {e}")

    async def stop_all(self):
        self.running = False
        if self._monitor_task:
            self._monitor_task.cancel()
            
        for name, service in self.services.items():
            if service["task"] and not service["task"].done():
                service["task"].cancel()
                service["running"] = False
                logger.info(f"[Supervisor] Stopped service: {name}")


supervisor = Supervisor()
