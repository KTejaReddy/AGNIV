from .models import WorkflowDefinition, WorkflowStep
from .registry import workflow_registry

def load_default_templates():
    presentation_mode = WorkflowDefinition(
        id="tpl_presentation",
        name="Presentation Mode",
        description="Prepares the system for a presentation.",
        goal="Mute volume, maximize specific window, disable sleep.",
        steps=[
            WorkflowStep(
                id="step1",
                capability="VOLUME_MUTE",
                parameters={"mute": True}
            ),
            WorkflowStep(
                id="step2",
                capability="OPEN_URL",
                parameters={"url": "https://slides.google.com"},
                depends_on=["step1"]
            )
        ]
    )
    
    coding_session = WorkflowDefinition(
        id="tpl_coding",
        name="Coding Session",
        description="Sets up environment for coding.",
        goal="Open IDE, browser, and start focus music.",
        steps=[
            WorkflowStep(
                id="step1",
                capability="OPEN_APPLICATION",
                parameters={"name": "VS Code"}
            ),
            WorkflowStep(
                id="step2",
                capability="OPEN_URL",
                parameters={"url": "https://github.com"},
                depends_on=["step1"]
            )
        ]
    )

    workflow_registry.register(presentation_mode)
    workflow_registry.register(coding_session)
