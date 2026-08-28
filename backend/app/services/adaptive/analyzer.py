from .models import Pattern, BehaviorSummary, ConfidenceLevel

class BehaviorAnalyzer:
    def __init__(self):
        self.summaries = []

    def analyze(self, pattern: Pattern):
        # Heuristic rules to translate a raw pattern into a semantic behavior
        desc = f"User repeatedly triggers {pattern.type} '{pattern.context_data.get('raw_context', '')}'"
        
        # Calculate confidence based on frequency
        confidence = ConfidenceLevel.MEDIUM
        if pattern.frequency > 5:
            confidence = ConfidenceLevel.HIGH
        if pattern.frequency > 10:
            confidence = ConfidenceLevel.VERY_HIGH
            
        summary = BehaviorSummary(
            description=desc,
            related_patterns=[pattern.id],
            confidence=confidence
        )
        self.summaries.append(summary)
        
        # Forward to Suggestion Engine
        from .suggestion import suggestion_engine
        suggestion_engine.generate_suggestions(summary)
        
    def get_all(self):
        return self.summaries

behavior_analyzer = BehaviorAnalyzer()
