from app.core.logging import logger
from .registry import skills_registry
from .executor import skills_executor

class SkillsManager:
    def enable(self, skill_id: str) -> bool:
        skill = skills_registry.get_skill(skill_id)
        if skill:
            skill.is_enabled = True
            return True
        return False

    def disable(self, skill_id: str) -> bool:
        skill = skills_registry.get_skill(skill_id)
        if skill:
            skill.is_enabled = False
            return True
        return False

    def run(self, skill_id: str):
        return skills_executor.execute(skill_id)

skills_manager = SkillsManager()
