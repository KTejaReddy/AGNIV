import asyncio
from datetime import datetime
from typing import Callable, Any, Dict
from pydantic import BaseModel
from app.core.logging import logger
import json

class Event(BaseModel):
    id: str
    type: str
    source: str
    payload: Dict[str, Any]
    priority: int = 0
    timestamp: float

    def __lt__(self, other):
        return self.timestamp < other.timestamp

class EventBus:
    def __init__(self):
        self.subscribers: Dict[str, list[Callable]] = {}
        self.history: list[Event] = []
        self._queue = asyncio.PriorityQueue()
        self._running = False
        self._task = None
        self._ws_manager = None # Injected

    def set_ws_manager(self, manager):
        self._ws_manager = manager

    def subscribe(self, event_type: str, callback: Callable):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)

    def unsubscribe(self, event_type: str, callback: Callable):
        if event_type in self.subscribers:
            try:
                self.subscribers[event_type].remove(callback)
            except ValueError:
                pass

    async def publish(self, event: Event):
        self.history.append(event)
        if len(self.history) > 1000:
            self.history.pop(0)
        
        # Priority Queue inversion (lower number = higher priority in python's PriorityQueue, so we negate priority)
        await self._queue.put((-event.priority, event))
        
        # Broadcast to UI immediately
        if self._ws_manager:
            try:
                await self._ws_manager.broadcast(json.dumps({
                    "type": "CORE_EVENT",
                    "event": event.dict()
                }))
            except Exception as e:
                logger.error(f"Event bus broadcast failed: {e}")

    def publish_threadsafe(self, event: Event):
        if hasattr(self, '_loop') and self._loop:
            asyncio.run_coroutine_threadsafe(self.publish(event), self._loop)
        else:
            logger.error("EventBus publish_threadsafe called before EventBus started!")

    async def start(self):
        self._loop = asyncio.get_running_loop()
        self._running = True
        self._task = asyncio.create_task(self._process_events())
        logger.info("Event Bus started")

    async def stop(self):
        self._running = False
        if self._task:
            self._task.cancel()
        logger.info("Event Bus stopped")

    async def _process_events(self):
        while self._running:
            try:
                priority, event = await self._queue.get()
                # Get callbacks for this specific event type and wildcard '*'
                callbacks = []
                if event.type in self.subscribers:
                    callbacks.extend(self.subscribers[event.type])
                if "*" in self.subscribers:
                    callbacks.extend(self.subscribers["*"])
                    
                for callback in callbacks:
                    try:
                        if asyncio.iscoroutinefunction(callback):
                            await callback(event)
                        else:
                            callback(event)
                    except Exception as e:
                        logger.error(f"Error in event subscriber for {event.type}: {e}")
                self._queue.task_done()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Event bus processing error: {e}")

event_bus = EventBus()
