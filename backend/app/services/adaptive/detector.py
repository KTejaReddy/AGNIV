import time
from typing import Dict, List
from .models import Pattern
from app.core.engine.event_bus import event_bus
from app.core.logging import logger

class PatternDetector:
    def __init__(self):
        self.patterns: Dict[str, Pattern] = {}

    def observe(self, event_type: str, context: str):
        # We form a unique signature for this semantic event
        signature = f"{event_type}:{context}"
        now = time.time()
        
        if signature in self.patterns:
            self.patterns[signature].frequency += 1
            self.patterns[signature].last_seen = now
        else:
            self.patterns[signature] = Pattern(
                type=event_type,
                frequency=1,
                first_seen=now,
                last_seen=now,
                context_data={"raw_context": context}
            )
            
        # If pattern hits threshold, publish it
        if self.patterns[signature].frequency >= 3:
            logger.info(f"Pattern Detected: {signature} (freq: {self.patterns[signature].frequency})")
            # In a real app, we might debounce this
            self._notify_analyzer(self.patterns[signature])
            
    def _notify_analyzer(self, pattern: Pattern):
        from .analyzer import behavior_analyzer
        behavior_analyzer.analyze(pattern)

    def get_all(self) -> List[Pattern]:
        return list(self.patterns.values())

    async def start(self):
        # Listen to relevant semantic events
        event_bus.subscribe("WORKFLOW_COMPLETED", self._on_workflow)
        event_bus.subscribe("SKILL_COMPLETED", self._on_skill)
        logger.info("Pattern Detector started")

    def _on_workflow(self, event):
        self.observe("WORKFLOW", event.payload.get("template_id", "Unknown"))

    def _on_skill(self, event):
        self.observe("SKILL", event.payload.get("skill_id", "Unknown"))

pattern_detector = PatternDetector()
