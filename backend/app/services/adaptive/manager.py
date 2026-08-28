from typing import List, Dict
from .models import Suggestion, Pattern, AdaptivePolicies, FeedbackType
from .policies import policies_manager
from .detector import pattern_detector
from .analyzer import behavior_analyzer
from .recommendation import recommendation_engine
from .feedback import feedback_manager

class AdaptiveManager:
    def get_suggestions(self) -> List[Suggestion]:
        # Filter out anything blocked or already acted upon
        return [s for s in recommendation_engine.get_all() if s.status == "PENDING"]
        
    def get_patterns(self) -> List[Pattern]:
        return pattern_detector.get_all()
        
    def get_behavior_summaries(self):
        return behavior_analyzer.get_all()

    def get_history(self) -> List[Dict]:
        return feedback_manager.get_history()

    def submit_feedback(self, suggestion_id: str, feedback: FeedbackType):
        feedback_manager.submit_feedback(suggestion_id, feedback)

    def get_policies(self) -> AdaptivePolicies:
        return policies_manager.get_policies()

    def update_policies(self, **kwargs):
        policies_manager.update_policies(**kwargs)

adaptive_manager = AdaptiveManager()
