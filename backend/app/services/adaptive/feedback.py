import time
from typing import List, Dict
from .models import FeedbackType
from app.core.engine.event_bus import event_bus, Event
from app.core.logging import logger

class FeedbackManager:
    def __init__(self):
        self.history: List[Dict] = []
        self.blocked_signatures = set()

    def submit_feedback(self, suggestion_id: str, feedback: FeedbackType):
        from .recommendation import recommendation_engine
        
        suggestion = recommendation_engine.suggestions.get(suggestion_id)
        if not suggestion:
            return
            
        suggestion.status = feedback.value
        
        self.history.append({
            "suggestion_id": suggestion.id,
            "title": suggestion.title,
            "feedback": feedback.value,
            "timestamp": time.time()
        })
        
        if feedback == FeedbackType.NEVER_SUGGEST_AGAIN:
            signature = f"{suggestion.title}:{suggestion.description}"
            self.blocked_signatures.add(signature)
            
        logger.info(f"Feedback received for {suggestion_id}: {feedback.value}")
        
        import asyncio
        try:
            loop = asyncio.get_running_loop()
            loop.create_task(self._publish_feedback(suggestion_id, feedback.value))
        except RuntimeError:
            pass

    async def _publish_feedback(self, suggestion_id: str, status: str):
        await event_bus.publish(Event(
            id=f"evt_{time.time()}",
            type=f"SUGGESTION_{status}",
            source="FeedbackManager",
            payload={"suggestion_id": suggestion_id},
            timestamp=time.time()
        ))

    def is_blocked(self, title: str, description: str) -> bool:
        return f"{title}:{description}" in self.blocked_signatures

    def get_history(self) -> List[Dict]:
        return self.history

feedback_manager = FeedbackManager()
