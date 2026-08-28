class InteractionRules:
    def __init__(self):
        # Heuristic map of sensory events to logical interaction intents
        self.gesture_map = {
            "Thumb_Up": "CONFIRM_ACCEPT",
            "Thumb_Down": "CONFIRM_REJECT",
            "Open_Palm": "WAVE_GREETING",
            "Closed_Fist": "CANCEL_ACTION"
        }

    def evaluate_gesture(self, gesture_name: str) -> str:
        return self.gesture_map.get(gesture_name, "UNKNOWN")

interaction_rules = InteractionRules()
