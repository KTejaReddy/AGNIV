"""
Sample Skill Extension — Daily Briefing
=======================================
Demonstrates how a Skill extension subscribes to events and
optionally triggers AGNIV capabilities to deliver a daily briefing.
"""
import time
import datetime


def _on_day_start(event):
    # In a real extension, this could call sdk.execute_capability("SPEAK_TEXT", ...)
    print(f"[DailyBriefing] Good morning! Today is {datetime.date.today()}")


class Extension:
    def __init__(self, sdk):
        self.sdk = sdk

    def on_enable(self):
        self.sdk.subscribe("SYSTEM_DAY_START", _on_day_start)
        self.sdk.log("Daily Briefing skill enabled and listening for SYSTEM_DAY_START events.")

    def on_disable(self):
        self.sdk.log("Daily Briefing skill disabled.")

    def metadata(self) -> dict:
        return {
            "skill_name": "Daily Briefing",
            "triggers": ["SYSTEM_DAY_START"],
            "description": "Speaks a briefing each morning.",
        }
