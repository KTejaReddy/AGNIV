import tracemalloc
import asyncio
import time
from app.services.perception.camera import camera_manager
from app.services.screen.manager import screen_manager
from app.core.engine.event_bus import event_bus, Event
import uuid
import logging

logging.basicConfig(level=logging.ERROR)

async def test_full_app():
    tracemalloc.start()
    print("Starting engine...")
    await event_bus.start()
    
    # Just start the camera and screen
    camera_manager.start(0)
    screen_manager.start(1)
    
    await asyncio.sleep(5)
    print("Taking snapshot 1...")
    s1 = tracemalloc.take_snapshot()
    
    # Wait to see background leaks
    await asyncio.sleep(10)
        
    print("Taking snapshot 2...")
    s2 = tracemalloc.take_snapshot()
    
    stats = s2.compare_to(s1, 'lineno')
    print('\n\n[TRACEMALLOC TOP 20]')
    for stat in stats[:20]:
        print(stat)
        
    camera_manager.stop()
    screen_manager.stop()

asyncio.run(test_full_app())
