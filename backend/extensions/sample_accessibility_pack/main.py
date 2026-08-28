"""
Sample Accessibility Pack Extension — Extended Sign Language
=============================================================
Demonstrates how an Accessibility Pack can extend the AGNIV
Sign Language recognizer vocabulary by subscribing to perception
events and mapping additional gesture patterns.
"""

# Extended vocabulary supplement
EXTENDED_VOCABULARY = {
    "one_finger": "One",
    "two_fingers": "Two",
    "three_fingers": "Three",
    "four_fingers": "Four",
    "ok_sign": "Okay",
    "heart_gesture": "Love",
    "pointing_up": "Up",
    "pointing_down": "Down",
    "pointing_left": "Left",
    "pointing_right": "Right",
}


def _on_gesture(event):
    gesture = event.payload.get("gesture")
    if gesture in EXTENDED_VOCABULARY:
        sign_name = EXTENDED_VOCABULARY[gesture]
        print(f"[ExtendedSignPack] Extended sign recognized: '{sign_name}' from gesture '{gesture}'")


class Extension:
    def __init__(self, sdk):
        self.sdk = sdk

    def on_enable(self):
        self.sdk.subscribe("PERCEPTION_GESTURE", _on_gesture)
        self.sdk.log(
            f"Extended Sign Language Pack enabled. "
            f"{len(EXTENDED_VOCABULARY)} additional signs registered."
        )

    def on_disable(self):
        self.sdk.log("Extended Sign Language Pack disabled.")

    def metadata(self) -> dict:
        return {
            "pack_type": "sign_language",
            "signs_added": len(EXTENDED_VOCABULARY),
            "vocabulary": list(EXTENDED_VOCABULARY.values()),
        }
