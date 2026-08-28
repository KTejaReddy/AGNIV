from .models import BehaviorSummary

class SuggestionEngine:
    def generate_suggestions(self, summary: BehaviorSummary):
        # We delegate the actual creation to the Recommendation Engine which builds the rich wrapper
        from .recommendation import recommendation_engine
        
        # Simple logical mapping
        title = "Optimize Workflow"
        if "SKILL" in summary.description:
            title = "Create Keyboard Shortcut for Skill"
            reason = "You use this skill frequently. A shortcut would save time."
        else:
            title = "Automate Workflow"
            reason = "You repeat this workflow often. Consider moving it to automation."
            
        recommendation_engine.create(title, summary, reason)

suggestion_engine = SuggestionEngine()
