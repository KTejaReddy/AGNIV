# AGNIV API Reference

This document outlines the core API capabilities provided by AGNIV.

## REST API (FastAPI)

- `GET /` - Health check.
- `GET /extensions/` - List all installed extensions.
- `GET /extensions/stats` - Extension metrics.
- `POST /extensions/{id}/enable` - Enable extension.
- `POST /extensions/{id}/disable` - Disable extension.
- `POST /extensions/scan` - Trigger a rescan of the extensions directory.

## EventBus Core Events

- `SYSTEM_STARTUP`: Fired when AGNIV is fully booted.
- `CAPABILITY_EXECUTED`: Fired when a capability successfully completes.
- `SERVICE_CRASHED`: Fired by the Supervisor when a background task crashes.
- `SYSTEM_WARNING`: High memory usage or other system warnings.
- `PERCEPTION_GESTURE`: A gesture is recognized by the camera.
- `VOICE_INPUT_RECEIVED`: Voice transcript parsed.

## Middleware
- **ProfilerMiddleware**: Automatically logs requests taking longer than 0.5s or consuming >80% CPU.
