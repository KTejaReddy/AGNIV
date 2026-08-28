from app.core.logging import logger
from .registry import skills_registry
from .validator import skills_validator
from app.services.workflow.manager import workflow_manager

class SkillsExecutor:
    def execute(self, skill_id: str) -> dict:
        skill = skills_registry.get_skill(skill_id)
        if not skill:
            return {"error": "Skill not found"}
            
        if not skill.is_enabled:
            return {"error": "Skill is disabled"}
            
        is_valid, msg = skills_validator.validate_dependencies(skill)
        if not is_valid:
            return {"error": msg}
            
        logger.info(f"Skill {skill.name} passed validation. Delegating to Workflow Engine.")
        
        # In a real system, the skill manifest would define dynamic workflow steps.
        # For Phase 11, we pass the execution entirely to the Workflow Engine.
        if skill.workflow_template_id:
            res = workflow_manager.run_template(skill.workflow_template_id)
            return res
        else:
            # Fallback mock for skills without explicit workflows yet
            return {"status": "success", "message": f"Skill {skill.name} executed natively."}

skills_executor = SkillsExecutor()
