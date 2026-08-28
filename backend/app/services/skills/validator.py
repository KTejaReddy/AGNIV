from app.core.logging import logger
from .models import SkillManifest
from app.services.knowledge.search import knowledge_search
from app.services.workflow.registry import workflow_registry

class SkillsValidator:
    def validate_dependencies(self, skill: SkillManifest) -> tuple[bool, str]:
        # 1. Validate Required Capabilities via Knowledge Engine
        for cap in skill.required_capabilities:
            results = knowledge_search.search(cap)
            found = False
            for r in results:
                if r["id"] == cap and r["data"].get("type") == "CAPABILITY":
                    found = True
                    break
            if not found:
                msg = f"Skill {skill.id} missing required capability: {cap}"
                logger.error(msg)
                return False, msg
                
        # 2. Validate Required Workflows
        for wf in skill.required_workflows:
            if not workflow_registry.get_template(wf):
                msg = f"Skill {skill.id} missing required workflow: {wf}"
                logger.error(msg)
                return False, msg
                
        # 3. Validate Required Knowledge domains (Mock logic for Phase 11)
        for k in skill.required_knowledge:
            logger.info(f"Checking knowledge domain: {k}")
            
        return True, "Success"

skills_validator = SkillsValidator()
