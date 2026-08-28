# AGNIV Extension SDK Documentation

## Overview

The AGNIV Extension SDK allows third-party developers to extend AGNIV without modifying the core source code. Extensions are self-contained Python packages that are installed by dropping them into the `extensions/` directory.

---

## Extension Types

| Type | Description |
|------|-------------|
| `capability` | Registers new capabilities into the AGNIV Capability Manager |
| `skill` | Adds a reusable intelligent skill unit |
| `workflow_pack` | Bundles pre-built workflow templates |
| `integration` | Connects AGNIV to external services (e.g. GitHub, Slack) |
| `ui_panel` | Provides metadata for custom dashboard panels |
| `accessibility_pack` | Extends the Accessibility Suite with new signs, voices, or gestures |

---

## Quick Start

### 1. Scaffold a new extension

```bash
cd backend
python -m agniv_sdk.cli create "My Cool Extension" capability
```

This creates:
```
my-cool-extension/
├── agniv-extension.json   ← manifest
├── main.py                ← your code
└── README.md
```

### 2. Implement the Extension class

Every extension must define a class called `Extension` in `main.py`:

```python
class Extension:
    def __init__(self, sdk):
        """Receives the AGNIVExtensionSDK instance."""
        self.sdk = sdk

    def on_enable(self):
        """Called when the extension is enabled."""
        self.sdk.log("My extension is running!")

    def on_disable(self):
        """Called when the extension is disabled or uninstalled."""
        pass

    def metadata(self) -> dict:
        """Optional: return runtime metadata for the dashboard."""
        return {"status": "active"}
```

### 3. Write the manifest (`agniv-extension.json`)

```json
{
  "id": "my-cool-extension",
  "name": "My Cool Extension",
  "version": "1.0.0",
  "type": "capability",
  "description": "Does something cool.",
  "author": {
    "name": "Your Name",
    "email": "you@example.com"
  },
  "agniv_version": ">=1.0.0",
  "entry_point": "main.py",
  "permissions": ["desktop"],
  "tags": ["cool", "sample"],
  "license": "MIT"
}
```

### 4. Install

**Option A — Drop and Scan:**
1. Copy your extension folder into `backend/extensions/`
2. In the AGNIV dashboard, click **Extensions SDK → Rescan**
3. Your extension appears in the list. Click **Enable**.

**Option B — CLI Install:**
```bash
python -m agniv_sdk.cli install ./my-cool-extension --target ./extensions
```

### 5. Package for distribution

```bash
python -m agniv_sdk.cli package ./my-cool-extension
# Creates: my-cool-extension-1.0.0.agniv
```

---

## SDK API Reference (`sdk`)

The `sdk` object injected into your `Extension.__init__` provides the following methods:

### EventBus

```python
# Subscribe to any AGNIV system event
sdk.subscribe("SKILL_COMPLETED", handler_function)

# Publish a custom event
await sdk.publish("MY_EXTENSION_EVENT", {"key": "value"})
```

### Capabilities

```python
# Execute an existing AGNIV capability
result = await sdk.execute_capability("OPEN_APPLICATION", {"name": "code"})

# Register a new capability (Capability-type extensions)
sdk.register_capability("MY_CAPABILITY", "1.0", "Description", my_handler)
```

Registered capabilities get the prefix `<extension-id>.<capability-name>` to avoid collisions.

### Logging

```python
sdk.log("Info message")
sdk.warn("Warning message")
sdk.error("Error message")
```

---

## Available System Events

| Event | Source | Payload |
|-------|--------|---------|
| `SKILL_COMPLETED` | Skills Engine | `{ skill_id, result }` |
| `WORKFLOW_COMPLETED` | Workflow Engine | `{ workflow_id, status }` |
| `MEMORY_STORED` | Memory Engine | `{ memory_id, type }` |
| `PERCEPTION_GESTURE` | Perception Engine | `{ gesture, confidence }` |
| `VOICE_INPUT_RECEIVED` | Voice Engine | `{ text }` |
| `SPEECH_GENERATED` | Voice Engine | `{ text }` |
| `SIGN_RECOGNIZED` | Accessibility Suite | `{ sign_name, confidence }` |
| `CAPTION_UPDATED` | Accessibility Suite | `{ text, speaker }` |
| `CAPABILITY_EXECUTED` | Core Engine | `{ capability, parameters }` |
| `EXTENSION_ENABLED` | Extension SDK | `{ extension_id }` |
| `EXTENSION_DISABLED` | Extension SDK | `{ extension_id }` |

---

## Permission Declarations

Declare permissions your extension needs. Users can see all requested permissions before enabling.

| Permission | Description |
|------------|-------------|
| `file.read` | Read files from disk |
| `file.write` | Write files to disk |
| `network` | Make outbound network requests |
| `desktop` | Control desktop applications |
| `voice` | Access voice/TTS capabilities |
| `screen` | Access screen intelligence data |
| `perception` | Access camera/gesture events |
| `memory` | Read/write AGNIV Memory |
| `workflow` | Trigger/register workflows |
| `skills` | Trigger/register skills |
| `knowledge` | Access knowledge base |
| `cognitive` | Access Groq reasoning layer |

---

## Extension Isolation

Each extension is loaded in its own Python module namespace via `importlib`. The `Extension` class receives an `AGNIVExtensionSDK` instance as its only bridge to core AGNIV functionality. Direct imports of `app.*` within extension code should be avoided — use the SDK instead.

On disable, the SDK automatically **unsubscribes all event handlers** registered by that extension.

---

## Version Compatibility

The `agniv_version` field in the manifest is checked against the running AGNIV version. Supported constraint formats:
- `>=1.0.0` — requires at least version 1.0.0
- `<=2.0.0` — compatible up to version 2.0.0
- `==1.0.0` — exact version match

---

## CLI Reference

```bash
# Scaffold a new extension
python -m agniv_sdk.cli create <name> <type> [--output ./]

# Validate an extension
python -m agniv_sdk.cli validate <path>

# Package into a .agniv file
python -m agniv_sdk.cli package <path> [--output ./]

# Install a directory or .agniv file
python -m agniv_sdk.cli install <path> [--target extensions/]
```

---

## REST API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/extensions/` | List all extensions |
| GET | `/extensions/stats` | Get extension stats |
| GET | `/extensions/{id}` | Get extension details |
| POST | `/extensions/{id}/enable` | Enable an extension |
| POST | `/extensions/{id}/disable` | Disable an extension |
| POST | `/extensions/{id}/uninstall` | Uninstall an extension |
| POST | `/extensions/scan` | Rescan extensions/ directory |
| POST | `/extensions/validate` | Validate a manifest JSON body |

---

## Sample Extensions

Six sample extensions ship with AGNIV in `backend/extensions/`:

| Directory | Type | Demonstrates |
|-----------|------|--------------|
| `sample_capability/` | capability | Registering a new GET_SYSTEM_INFO capability |
| `sample_skill/` | skill | Subscribing to system events for a daily briefing |
| `sample_workflow_pack/` | workflow_pack | Bundling pre-built workflow templates |
| `sample_integration/` | integration | Connecting to external services (GitHub Gist) |
| `sample_ui_panel/` | ui_panel | Publishing panel metadata for frontend rendering |
| `sample_accessibility_pack/` | accessibility_pack | Extending sign language vocabulary |
