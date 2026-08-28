import time
from typing import List, Dict
from .models import BehaviorSummary, Suggestion
from app.core.engine.event_bus import event_bus, Event
from app.core.logging import logger

class RecommendationEngine:
    def __init__(self):
        self.suggestions: Dict[str, Suggestion] = {}
        
    def create(self, title: str, summary: BehaviorSummary, reason: str):
        # We need to check if this conflicts with "NEVER_SUGGEST_AGAIN"
        from .feedback import feedback_manager
        if feedback_manager.is_blocked(title, summary.description):
            logger.info(f"Suggestion '{title}' blocked by feedback policy.")
            return

        suggestion = Suggestion(
            title=title,
            description=f"Based on your behavior: {summary.description}",
            reason=reason,
            evidence=[summary.description],
            confidence=summary.confidence,
            impact="High",
            estimated_time_saved="5 mins/day",
            required_permissions=["WORKFLOW_EXECUTE"]
        )
        self.suggestions[suggestion.id] = suggestion
        
        # Publish event
        # Use asyncio.create_task to safely call async method from sync context if needed
        # Since this path is triggered by the detector, which is driven by EventBus (async),
        # we can just emit an event back. Actually, publish is async. We will use a safe wrapper or queue it.
        # For simplicity in this mock, we just log and rely on the REST API for the frontend, but we'll try to use EventBus safely.
        import asyncio
        try:
            loop = asyncio.get_running_loop()
            loop.create_task(self._publish(suggestion))
        except RuntimeError:
            pass # No event loop
            
    async def _publish(self, suggestion: Suggestion):
        await event_bus.publish(Event(
            id=f"evt_{time.time()}",
            type="SUGGESTION_CREATED",
            source="RecommendationEngine",
            payload=suggestion.dict(),
            timestamp=time.time()
        ))

    def get_all(self) -> List[Suggestion]:
        return list(self.suggestions.values())

recommendation_engine = RecommendationEngine()
