import mediapipe as mp
import cv2
from .gestures import gesture_engine
from .session import perception_session

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

class HandTracker:
    def __init__(self):
        self.hands = mp_hands.Hands(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
            max_num_hands=2
        )

    def process(self, frame):
        if not perception_session.active_trackers.get("hands"):
            return frame

        # Convert to RGB for MediaPipe
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS
                )
            # Pass to gesture engine
            gesture_engine.process_hand_landmarks(results.multi_hand_landmarks, results.multi_handedness)
            
        return frame

hand_tracker = HandTracker()
