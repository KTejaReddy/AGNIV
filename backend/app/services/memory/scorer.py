from .models import Importance, MemoryType

class MemoryImportanceScorer:
    def score(self, memory_type: MemoryType, source: str, outcome: str = None) -> Importance:
        if memory_type == MemoryType.PREFERENCE:
            return Importance.HIGH
        elif memory_type == MemoryType.HABIT:
            return Importance.HIGH
        elif memory_type == MemoryType.SUCCESSFUL_TASK:
            return Importance.MEDIUM
        elif memory_type == MemoryType.FAILED_TASK:
            return Importance.LOW
        elif memory_type == MemoryType.SKILL_USAGE or memory_type == MemoryType.WORKFLOW_HISTORY:
            if outcome == "success":
                return Importance.MEDIUM
            return Importance.LOW
        
        return Importance.MEDIUM

memory_scorer = MemoryImportanceScorer()
