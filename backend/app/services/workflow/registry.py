from typing import Dict, List
from .models import WorkflowDefinition

class WorkflowRegistry:
    def __init__(self):
        self.templates: Dict[str, WorkflowDefinition] = {}

    def register(self, template: WorkflowDefinition):
        self.templates[template.id] = template

    def get_template(self, template_id: str) -> WorkflowDefinition:
        return self.templates.get(template_id)

    def list_templates(self) -> List[WorkflowDefinition]:
        return list(self.templates.values())

workflow_registry = WorkflowRegistry()
