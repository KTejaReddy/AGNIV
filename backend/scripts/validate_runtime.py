import asyncio
import os
import sys
import uuid

# Ensure backend root is in PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.engine.event_bus import event_bus, Event
from app.core.engine.supervisor import supervisor
from app.services.cognitive.pipeline import thinking_pipeline
from app.services.memory.manager import memory_manager
from app.services.memory.models import MemoryItem
from app.services.runtime.living_runtime import living_runtime

async def test_cognitive_engine():
    print("Testing Cognitive Engine...")
    response = await thinking_pipeline.process_input("What is 2 + 2? Please just say '4'.")
    print(f"Cognitive Engine Response: {response}")
    assert "4" in response.lower(), "Cognitive Engine failed basic inference."

async def test_memory_engine():
    print("Testing Memory Engine...")
    memory = MemoryItem(
        id=str(uuid.uuid4()),
        type="SUCCESSFUL_TASK",
        title="AGNIV Validation",
        content="AGNIV is being validated",
        summary="Testing memory engine validation",
        source="system",
        outcome="success"
    )
    memory_manager.create_memory(memory)
    memories = memory_manager.get_all()
    print(f"Memory Engine Retrieved: {len(memories)} items")
    assert len(memories) > 0, "Memory Engine failed retrieval."

async def test_desktop_controller():
    print("Testing Desktop Controller...")
    from app.services.desktop import register_desktop_capabilities
    from app.core.engine.capability_manager import capability_manager
    register_desktop_capabilities()
    caps = capability_manager.capabilities
    print(f"Desktop Controller Capabilities registered: {len(caps)}")
    assert len(caps) > 0, "Desktop controller failed to register capabilities."

async def main():
    print("=======================================")
    print("Starting AGNIV Runtime Validation Suite")
    print("=======================================\n")
    
    try:
        await test_cognitive_engine()
        print("[PASS] Cognitive Engine\n")
        
        await test_memory_engine()
        print("[PASS] Memory Engine\n")
        
        await test_desktop_controller()
        print("[PASS] Desktop Controller\n")
        
        print("\nAll integration tests passed successfully.")
    except Exception as e:
        print(f"\n[FAIL] Validation suite failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
