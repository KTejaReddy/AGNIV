"""
Sample Capability Extension — System Info
=========================================
This extension demonstrates how to register a new CAPABILITY
into AGNIV's Capability Manager via the Extension SDK.

Usage pattern:
    from agniv_sdk import sdk  # Injected automatically at load time
"""
import time
import platform


def _get_uptime_handler(params: dict) -> dict:
    """Returns platform uptime info (simplified, OS-independent)."""
    return {
        "system": platform.system(),
        "node": platform.node(),
        "processor": platform.processor(),
        "python_version": platform.python_version(),
        "timestamp": time.time(),
    }


class Extension:
    def __init__(self, sdk):
        self.sdk = sdk

    def on_enable(self):
        # Register the new capability
        self.sdk.register_capability(
            name="GET_SYSTEM_INFO",
            version="1.0",
            description="Returns system platform and runtime information.",
            handler=_get_uptime_handler,
        )
        self.sdk.log("System Info capability registered.")

    def on_disable(self):
        self.sdk.log("System Info capability extension disabled.")

    def metadata(self) -> dict:
        return {
            "capabilities_added": ["sample-capability.GET_SYSTEM_INFO"],
            "author": "AGNIV SDK Team",
        }
