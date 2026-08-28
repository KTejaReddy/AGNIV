import pytest
from app.services.workflow.manager import workflow_manager
from app.services.workflow.registry import workflow_registry
from app.services.workflow.models import WorkflowDefinition

def test_workflow_manager_initialization():
    assert workflow_manager is not None
    
def test_workflow_registration():
    wf_def = WorkflowDefinition(
        id="test.workflow",
        name="Test Workflow",
        description="A test workflow",
        goal="Test goal",
        steps=[
            {"id": "step1", "capability": "TEST_CAP", "params": {}}
        ]
    )
    workflow_registry.register(wf_def)
    assert workflow_registry.get_template("test.workflow") is not None

