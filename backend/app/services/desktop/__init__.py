from app.core.logging import logger
from . import applications, files, system, browser, clipboard, screen, windows

def register_desktop_capabilities():
    logger.info("Registering Desktop Capabilities...")
    applications.register()
    files.register()
    system.register()
    browser.register()
    clipboard.register()
    screen.register()
    windows.register()
    logger.info("Desktop Capabilities registered successfully.")
