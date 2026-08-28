import asyncio
import os
import sys
import time

# Ensure backend root is in PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.engine.event_bus import event_bus, Event
from app.services.runtime.living_runtime import living_runtime

# We will collect events emitted by LivingRuntime to verify it responds to our injected events
received_events = []

async def test_listener(event: Event):
    received_events.append(event)

async def verify_connection(name, event_type, payload):
    print(f"Triggering {name} ({event_type})...")
    received_events.clear()
    
    await event_bus.publish(Event(
        id=f"test_{time.time()}",
        type=event_type,
        source="RuntimeReport",
        payload=payload,
        timestamp=time.time()
    ))
    
    # Wait for processing
    await asyncio.sleep(0.5)
    
    # Check if LivingRuntime emitted state change or telemetry
    has_telemetry = any(e.type == "TELEMETRY_UPDATE" for e in received_events)
    has_state = any(e.type == "RUNTIME_STATE_CHANGE" for e in received_events)
    
    if has_telemetry or has_state:
        print(f"[PASS] {name} -> LivingRuntime Reacted (Telemetry: {has_telemetry}, State: {has_state})\n")
    else:
        print(f"[FAIL] {name} -> No reaction from LivingRuntime\n")
    
    return has_telemetry or has_state

async def main():
    print("=======================================")
    print("      LIVING RUNTIME EVENT REPORT      ")
    print("=======================================\n")
    
    # Initialize runtime
    await event_bus.start()
    asyncio.create_task(living_runtime.start())
    event_bus.subscribe("TELEMETRY_UPDATE", test_listener)
    event_bus.subscribe("RUNTIME_STATE_CHANGE", test_listener)
    
    await asyncio.sleep(0.5) # allow start
    
    results = []
    
    results.append(await verify_connection("Voice Detection", "VOICE_DETECTED", {}))
    results.append(await verify_connection("Voice Transcript", "VOICE_TRANSCRIPT", {"text": "hello agniv"}))
    results.append(await verify_connection("Perception Gesture", "PERCEPTION_GESTURE", {"gesture": "wave"}))
    results.append(await verify_connection("Workflow Start", "WORKFLOW_STARTED", {"id": "123"}))
    results.append(await verify_connection("Workflow Complete", "WORKFLOW_COMPLETED", {"id": "123"}))
    
    print("=======================================")
    if all(results):
        print("STATUS: ALL CONNECTIONS VERIFIED")
    else:
        print("STATUS: SOME CONNECTIONS FAILED")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
