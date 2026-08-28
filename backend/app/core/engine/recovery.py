"""
Crash Recovery and Safe Mode Management.
Handles boot flags to detect crash loops and boot into safe mode.
"""
import os
import json
from app.core.logging import logger

CRASH_LOG_PATH = "logs/crash_state.json"
MAX_CRASHES = 3


class RecoveryManager:
    def __init__(self):
        self.safe_mode = False
        self.developer_mode = os.environ.get("AGNIV_DEV_MODE", "false").lower() == "true"
        self._ensure_log_dir()

    def _ensure_log_dir(self):
        os.makedirs(os.path.dirname(CRASH_LOG_PATH) or ".", exist_ok=True)

    def _load_crash_state(self) -> dict:
        if os.path.exists(CRASH_LOG_PATH):
            try:
                with open(CRASH_LOG_PATH, "r") as f:
                    return json.load(f)
            except Exception:
                pass
        return {"consecutive_crashes": 0, "last_error": None}

    def _save_crash_state(self, state: dict):
        with open(CRASH_LOG_PATH, "w") as f:
            json.dump(state, f)

    def check_boot_state(self):
        """Check if we should boot into safe mode."""
        state = self._load_crash_state()
        if state["consecutive_crashes"] >= MAX_CRASHES:
            logger.warning(
                f"AGNIV crashed {state['consecutive_crashes']} times in a row! Booting into SAFE MODE."
            )
            self.safe_mode = True
        else:
            self.safe_mode = False
            if state["consecutive_crashes"] > 0:
                logger.info(f"Recovering from previous crash. Crash count: {state['consecutive_crashes']}")

    def record_crash(self, error_msg: str):
        """Called when a fatal error occurs before exiting."""
        state = self._load_crash_state()
        state["consecutive_crashes"] += 1
        state["last_error"] = error_msg
        self._save_crash_state(state)
        logger.error(f"FATAL CRASH recorded: {error_msg}")

    def clear_crash_state(self):
        """Called after a successful boot and stable runtime."""
        if os.path.exists(CRASH_LOG_PATH):
            os.remove(CRASH_LOG_PATH)
        self.safe_mode = False
        logger.info("Crash state cleared. System stable.")

    def is_safe_mode(self) -> bool:
        return self.safe_mode

    def is_developer_mode(self) -> bool:
        return self.developer_mode


recovery_manager = RecoveryManager()
