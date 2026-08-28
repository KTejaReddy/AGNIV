import asyncio
import psutil
import os
import time
import sys
import logging
from app.core.engine.event_bus import event_bus

logging.basicConfig(level=logging.ERROR)

async def measure(duration=15, subsystem=""):
    process = psutil.Process(os.getpid())
    
    start_mem = process.memory_info().rss / (1024 * 1024)
    start_threads = process.num_threads()
    start_handles = process.num_handles() if hasattr(process, 'num_handles') else 0
    
    peak_mem = start_mem
    
    start_time = time.time()
    while time.time() - start_time < duration:
        mem = process.memory_info().rss / (1024 * 1024)
        peak_mem = max(peak_mem, mem)
        await asyncio.sleep(0.5)
        
    end_mem = process.memory_info().rss / (1024 * 1024)
    end_threads = process.num_threads()
    end_handles = process.num_handles() if hasattr(process, 'num_handles') else 0
    
    growth = end_mem - start_mem
    growth_per_min = growth / (duration / 60)
    
    print(f"Subsystem: {subsystem}")
    print(f"Initial RSS: {start_mem:.2f} MB")
    print(f"Peak RSS: {peak_mem:.2f} MB")
    print(f"Growth after {duration}s: {growth:.2f} MB")
    print(f"Growth per minute: {growth_per_min:.2f} MB")
    print(f"Handle count: {end_handles} (Delta: {end_handles - start_handles})")
    print(f"Thread count: {end_threads} (Delta: {end_threads - start_threads})")
    print("-" * 34)

async def test_subsystem(subsystem):
    await event_bus.start()
    
    if subsystem == "backend":
        pass
    elif subsystem == "voice":
        from app.services.voice.wake_word import wake_word_manager
        wake_word_manager.start_listening()
    elif subsystem == "camera":
        from app.services.perception.camera import camera_manager
        from app.services.perception.session import perception_session
        perception_session.set_tracker_state("hands", False)
        perception_session.set_tracker_state("face", False)
        perception_session.set_tracker_state("body", False)
        camera_manager.start(0)
    elif subsystem == "mediapipe":
        from app.services.perception.camera import camera_manager
        from app.services.perception.session import perception_session
        perception_session.set_tracker_state("hands", True)
        perception_session.set_tracker_state("face", True)
        perception_session.set_tracker_state("body", True)
        camera_manager.start(0)
    elif subsystem == "screen":
        from app.services.screen.manager import screen_manager
        screen_manager.start(1)
    elif subsystem == "easyocr":
        from app.services.screen.ocr import ocr_engine
        import numpy as np
        # Need to simulate OCR load
        async def run_ocr():
            while True:
                dummy_img = np.zeros((1080, 1920, 3), dtype=np.uint8)
                ocr_engine.extract_text(dummy_img)
                await asyncio.sleep(0.5)
        asyncio.create_task(run_ocr())
    elif subsystem == "inspector":
        from app.services.runtime.debug_service import debug_service
        asyncio.create_task(debug_service.start())
    elif subsystem == "all":
        from app.services.voice.wake_word import wake_word_manager
        from app.services.perception.camera import camera_manager
        from app.services.perception.session import perception_session
        from app.services.screen.manager import screen_manager
        from app.services.runtime.debug_service import debug_service
        wake_word_manager.start_listening()
        perception_session.set_tracker_state("hands", True)
        perception_session.set_tracker_state("face", True)
        perception_session.set_tracker_state("body", True)
        camera_manager.start(0)
        screen_manager.start(1)
        asyncio.create_task(debug_service.start())
        
    await measure(15, subsystem)
    
if __name__ == "__main__":
    asyncio.run(test_subsystem(sys.argv[1]))
