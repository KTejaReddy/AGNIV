import re
from app.core.logging import logger
from app.services.knowledge.search import knowledge_search
from app.services.skills.registry import skills_registry

class DecisionEngine:
    def __init__(self):
        # Heuristic rules to bypass LLM logic
        self.rules = {
            "increase volume": {"type": "RULE", "action": "VOLUME_SET", "params": {"level": "+10"}},
            "open chrome": {"type": "RULE", "action": "OPEN_APPLICATION", "params": {"name": "chrome"}},
            "stop listening": {"type": "RULE", "action": "STOP_LISTENING", "params": {}},
        }

    async def evaluate(self, user_input: str, context: dict = None) -> dict:
        user_input_lower = user_input.lower().strip()

        # 1. Check strict heuristic rules
        if user_input_lower in self.rules:
            logger.info(f"Decision Engine: Rule matched for action {self.rules[user_input_lower]['action']}")
            return {
                "path": "RULE",
                "intent": self.rules[user_input_lower]
            }
            
        # 1.5 Check Skills Engine (highest intelligence match without LLM)
        for skill in skills_registry.list_skills():
            if user_input_lower == skill.name.lower():
                logger.info(f"Decision Engine: Skill matched {skill.name}")
                return {
                    "path": "SKILL",
                    "intent": {"type": "SKILL", "skill_id": skill.id}
                }
                
        # 2. Check Knowledge Engine
        knowledge_results = knowledge_search.search(user_input_lower)
        if knowledge_results:
            # If we found an exact capability match, return it
            for res in knowledge_results:
                if res["data"].get("type") == "CAPABILITY" and res["id"].lower() == user_input_lower.replace(" ", "_"):
                    logger.info(f"Decision Engine: Knowledge Engine matched {res['id']}")
                    return {
                        "path": "KNOWLEDGE",
                        "intent": {"type": "ACTION", "action": res["id"], "params": {}}
                    }

        # 3. Fallback to Groq reasoning
        logger.info("Decision Engine: Falling back to GROQ")
        return {
            "path": "GROQ",
            "intent": None
        }

decision_engine = DecisionEngine()
