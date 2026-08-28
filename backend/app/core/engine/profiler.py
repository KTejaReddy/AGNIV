"""
Performance Profiler.
Middleware for FastAPI and utility functions to measure execution time, CPU, and RAM.
"""
import time
import psutil
import os
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.logging import logger
from typing import Callable, Any
from functools import wraps


class ProfilerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()
        process = psutil.Process(os.getpid())
        start_cpu = process.cpu_percent()
        
        response = await call_next(request)
        
        process_time = time.perf_counter() - start_time
        end_cpu = process.cpu_percent()
        
        # Only log slow requests or high CPU
        if process_time > 0.5:
            logger.warning(
                f"[Profiler] SLOW REQUEST: {request.method} {request.url.path} took {process_time:.4f}s"
            )
            
        if end_cpu > 80.0:
            logger.warning(
                f"[Profiler] HIGH CPU during {request.method} {request.url.path}: {end_cpu}%"
            )
            
        response.headers["X-Process-Time"] = str(process_time)
        return response


def profile_sync(func: Callable) -> Callable:
    """Decorator to profile synchronous functions for blocking operations."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        duration = time.perf_counter() - start
        
        if duration > 0.1:  # 100ms is considered blocking in async context
            logger.warning(f"[Profiler] BLOCKING OP DETECTED in {func.__name__}: {duration:.4f}s")
            
        return result
    return wrapper


def get_system_profile() -> dict:
    """Get current system performance profile."""
    process = psutil.Process(os.getpid())
    return {
        "cpu_percent": psutil.cpu_percent(interval=0.1),
        "ram_used_mb": process.memory_info().rss / (1024 * 1024),
        "threads": process.num_threads(),
        "open_files": len(process.open_files()),
        "connections": len(process.connections())
    }
