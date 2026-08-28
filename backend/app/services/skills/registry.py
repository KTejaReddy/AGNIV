from typing import Dict, List, Optional
from .models import SkillManifest

class SkillsRegistry:
    def __init__(self):
        self.skills: Dict[str, SkillManifest] = {}

    def register(self, skill: SkillManifest):
        self.skills[skill.id] = skill

    def get_skill(self, skill_id: str) -> Optional[SkillManifest]:
        return self.skills.get(skill_id)

    def list_skills(self) -> List[SkillManifest]:
        return list(self.skills.values())
        
    def remove(self, skill_id: str):
        if skill_id in self.skills:
            del self.skills[skill_id]

skills_registry = SkillsRegistry()
