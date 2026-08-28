# AGNIV V1.0 User Guide

Welcome to AGNIV, your desktop AI operating companion. This guide covers how to set up, configure, and use the core capabilities of AGNIV.

## 1. Getting Started
AGNIV is designed to sit quietly in the background and assist you when needed. Once installed, it will automatically start with your computer (if configured to do so) and place an icon in your system tray.

### Safe Mode
If AGNIV crashes repeatedly, it will boot into **Safe Mode**. In Safe Mode, extensions and complex workflows are disabled to allow you to diagnose the issue via the dashboard.

## 2. Core Engines
- **Screen Intelligence:** Understands your desktop, active windows, and UI elements.
- **Voice Engine:** Listens for wake words and handles Text-to-Speech (TTS).
- **Perception Engine:** If a camera is connected, understands hand gestures and body language.
- **Cognitive Engine:** The "brain" powered by Groq, providing reasoning for tasks.

## 3. Extensions
You can extend AGNIV using the **Extension SDK**. 
Simply drop `.agniv` packages or extension folders into the `backend/extensions` folder. You can manage them from the **Extensions SDK** panel in the UI.

## 4. Workflows & Skills
AGNIV can perform complex automated tasks using its Workflow Engine. You can define triggers (like a time of day or a specific voice command) to launch predefined workflows.

---
*For support, please check the [Troubleshooting Guide](troubleshooting.md).*
