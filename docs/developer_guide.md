# AGNIV Developer Guide

This guide is for developers contributing to the core AGNIV repository.

## Architecture Principles
1. **Event-Driven**: All communication between engines happens via the `EventBus`. Modules should rarely call each other directly.
2. **Modularity**: New capabilities should be added as independent services or via the Extension SDK.
3. **No Direct Groq Control**: The Cognitive Engine parses intents and uses Groq for reasoning, but Groq must NEVER directly control the desktop environment.

## Background Services & Supervisor
Background tasks (like voice listening, screen capture) are managed by the `Supervisor`.
To register a new background service:
```python
from app.core.engine.supervisor import supervisor

async def my_service():
    while True:
        # do work
        await asyncio.sleep(1)

await supervisor.register_service("my_service", my_service)
```

## Security
Always run `scripts/security_audit.py` before committing changes to ensure you haven't introduced any sandbox bypasses or permission gaps.

## Running Tests
AGNIV uses `pytest`. Run the test suite:
```bash
python -m pytest tests/
```
