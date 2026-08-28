import pytest
import asyncio
from app.core.engine.event_bus import event_bus, Event
from app.core.engine.recovery import recovery_manager
import time
import os

@pytest.mark.asyncio
async def test_event_bus():
    received = []
    
    def handler(event):
        received.append(event)
        
    event_bus.subscribe("TEST_EVENT", handler)
    
    # Event bus queue needs to be running to process events
    await event_bus.start()
    
    await event_bus.publish(Event(
        id="test_1",
        type="TEST_EVENT",
        source="pytest",
        payload={"msg": "hello"},
        timestamp=time.time()
    ))
    
    # Wait for processing
    await asyncio.sleep(0.1)
    await event_bus.stop()
    
    assert len(received) == 1
    assert received[0].payload["msg"] == "hello"

def test_recovery_manager():
    # Clear any previous state
    recovery_manager.clear_crash_state()
    assert recovery_manager.is_safe_mode() == False
    
    # Simulate crashes
    recovery_manager.record_crash("test crash 1")
    recovery_manager.record_crash("test crash 2")
    recovery_manager.record_crash("test crash 3")
    
    recovery_manager.check_boot_state()
    assert recovery_manager.is_safe_mode() == True
    
    recovery_manager.clear_crash_state()
    recovery_manager.check_boot_state()
    assert recovery_manager.is_safe_mode() == False
