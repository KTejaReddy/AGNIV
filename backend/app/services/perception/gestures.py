import asyncio
import uuid
import time
from app.core.engine import event_bus, Event
from app.core.logging import logger
from .session import perception_session

class GestureEngine:
    def __init__(self):
        self.last_gesture = None
        self.last_gesture_time = 0

    def process_hand_landmarks(self, landmarks_list, handedness_list):
        if not perception_session.active_trackers.get("gestures"):
            return
            
        for idx, hand_landmarks in enumerate(landmarks_list):
            # Simplistic heuristic for Thumbs Up / Open Palm
            # In a full production system, we'd calculate angles. 
            # For phase 5 demonstration, we use basic y-coordinate comparisons.
            
            thumb_tip = hand_landmarks.landmark[4]
            index_tip = hand_landmarks.landmark[8]
            middle_tip = hand_landmarks.landmark[12]
            ring_tip = hand_landmarks.landmark[16]
            pinky_tip = hand_landmarks.landmark[20]
            wrist = hand_landmarks.landmark[0]
            
            fingers_up = 0
            if index_tip.y < hand_landmarks.landmark[6].y: fingers_up += 1
            if middle_tip.y < hand_landmarks.landmark[10].y: fingers_up += 1
            if ring_tip.y < hand_landmarks.landmark[14].y: fingers_up += 1
            if pinky_tip.y < hand_landmarks.landmark[18].y: fingers_up += 1
            
            gesture = None
            if fingers_up == 4 and thumb_tip.y < hand_landmarks.landmark[3].y:
                gesture = "WAVE"
            elif fingers_up == 1:
                gesture = "POINT"
            elif fingers_up == 0 and thumb_tip.y < index_tip.y:
                gesture = "THUMBS_UP"
            elif fingers_up == 0 and thumb_tip.y > wrist.y:
                gesture = "THUMBS_DOWN"
            elif fingers_up == 0:
                gesture = "CLOSED_FIST"
                
            if gesture and gesture != self.last_gesture:
                now = time.time()
                if now - self.last_gesture_time > 1.0: # Debounce
                    self.last_gesture = gesture
                    self.last_gesture_time = now
                    perception_session.update_state("gesture", gesture)
                    
                    event_bus.publish_threadsafe(Event(
                            id=str(uuid.uuid4()),
                            type="GESTURE_DETECTED",
                            source="GestureEngine",
                            payload={"gesture": gesture, "confidence": 0.85},
                            timestamp=now
                        ))

gesture_engine = GestureEngine()
