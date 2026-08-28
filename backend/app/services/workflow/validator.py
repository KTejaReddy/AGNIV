from app.core.logging import logger
from app.services.knowledge.search import knowledge_search
from .models import WorkflowInstance

class WorkflowValidator:
    def validate(self, instance: WorkflowInstance) -> tuple[bool, str]:
        logger.info(f"Validating workflow {instance.instance_id}")
        
        for step in instance.steps:
            # Check capability in Knowledge Engine
            results = knowledge_search.search(step.capability)
            found = False
            for r in results:
                if r["id"] == step.capability and r["data"].get("type") == "CAPABILITY":
                    found = True
                    break
            
            if not found:
                msg = f"Validation Failed: Capability '{step.capability}' not found in Knowledge Graph."
                logger.error(msg)
                return False, msg
                
        return True, "Success"

workflow_validator = WorkflowValidator()
