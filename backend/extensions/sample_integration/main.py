"""
Sample Integration Extension — GitHub Integration
==================================================
Demonstrates how an Integration extension subscribes to AGNIV
system events and can forward data to external services.
(No actual network calls are made in this sample.)
"""


def _on_skill_completed(event):
    skill_name = event.payload.get("skill_name", "unknown")
    print(f"[GitHubIntegration] Would post to GitHub Gist: Skill '{skill_name}' completed.")


def _on_memory_stored(event):
    print(f"[GitHubIntegration] Would log memory event to GitHub Gist.")


class Extension:
    def __init__(self, sdk):
        self.sdk = sdk

    def on_enable(self):
        self.sdk.subscribe("SKILL_COMPLETED", _on_skill_completed)
        self.sdk.subscribe("MEMORY_STORED", _on_memory_stored)
        self.sdk.log("GitHub Integration enabled. Listening for skill and memory events.")

    def on_disable(self):
        self.sdk.log("GitHub Integration disabled.")

    def metadata(self) -> dict:
        return {
            "integration_type": "github",
            "events_monitored": ["SKILL_COMPLETED", "MEMORY_STORED"],
            "note": "This is a demonstration extension. Configure your GitHub token in extension settings.",
        }
