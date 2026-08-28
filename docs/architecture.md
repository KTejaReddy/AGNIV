# AGNIV Architecture

AGNIV is a desktop AI operating companion capable of understanding voice, vision, gestures, sign language, desktop context, and safely performing actions on the user's computer.

This document describes the Phase 1 architectural foundation.

## Core Philosophy

- **Modularity:** Every subsystem (plugins, settings, database, logging) must be cleanly separated to allow easy upgrades and future phase additions without breaking existing components.
- **Performance:** Avoid unnecessary polling. Use WebSockets for realtime updates. Optimize for low memory footprint.
- **Safety First:** Global exception handling, structured logging, and robust crash recovery.
- **Zero Placeholders:** Phase 1 implements foundation features (Settings, Logging, Plugins architecture, UI layout) which are fully functional in their domain. Future AI features are intentionally excluded to ensure a rock-solid base.

## Project Structure

```
AGNIV/
├── backend/                  # Python FastAPI Core
│   ├── app/
│   │   ├── api/              # REST & WebSocket Endpoints
│   │   ├── core/             # Configuration, Logging, Exceptions
│   │   ├── database/         # SQLite Models, Session Management
│   │   └── services/         # Settings Manager, Plugin Loader
│   ├── alembic/              # Database Migrations
│   ├── plugins/              # Directory for future plugin modules
│   └── logs/                 # Output directory for rotating logs
├── frontend/                 # Electron + React + Vite + TailwindCSS
│   ├── electron/             # Electron Main Process & Preload Scripts
│   ├── src/
│   │   ├── components/       # Layouts, UI Components
│   │   ├── pages/            # Feature Views (Settings, Logs, Plugins)
│   │   ├── services/         # API & WebSocket Clients
│   │   ├── store/            # Zustand State Management
│   │   └── styles/           # Tailwind / Custom Glassmorphism CSS
└── docs/                     # Documentation
```

## Backend Architecture

The backend acts as the central brain and hardware bridge for AGNIV.

### Modules

1. **`core/`**:
   - `config.py`: Centralized configuration (dev/prod).
   - `logging.py`: Structured rotating logs.
   - `exceptions.py`: Global exception handling.

2. **`database/`**:
   - Uses SQLite and SQLAlchemy.
   - Designed for easy migrations via Alembic.
   - Avoids heavy ORM layers where unnecessary, providing direct state persistence (e.g., Settings).

3. **`services/`**:
   - `settings_manager.py`: Retrieves and saves preferences to SQLite.
   - `plugin_loader.py`: A framework capable of discovering and loading plugin modules dynamically. It provides hooks for enabling, disabling, unloading, and fetching plugin metadata.

4. **`api/`**:
   - Exposes REST endpoints for configuration and state.
   - Central WebSocket hub for real-time frontend updates (e.g., system stats, plugin state changes).

## Frontend Architecture

The frontend is a premium desktop interface built with Electron, React, and TailwindCSS.

### Features
- **Glassmorphism & Dark Theme:** Implemented purely in CSS/Tailwind for max flexibility.
- **State Management:** Zustand, providing an ultra-lightweight store.
- **IPC (Inter-Process Communication):** Secure context bridge via Electron preload scripts to integrate tightly with the OS without sacrificing security.

## Future Phases

Future modules will plug into this architecture seamlessly:

1. **AI / Voice / Vision:** Will be implemented as isolated services running in the background or as plugins via the `plugin_loader`. They will emit events over the WebSocket hub to the frontend.
2. **Desktop Automation:** Will leverage Python OS-level libraries (e.g., `pyautogui`, `win32api`), exposed to the intelligence engine via internal service APIs, keeping the FastAPI frontend-facing layer clean.
3. **Cloud Sync:** Can be introduced by updating the `core/config.py` and adding a sync worker service that securely synchronizes the SQLite schema with the cloud.
