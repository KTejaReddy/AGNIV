from .models import SkillManifest, SkillCategory
from .registry import skills_registry

def load_builtins():
    builtins = [
        SkillManifest(
            id="skill_explain_screen",
            name="Explain Screen",
            description="Captures the screen and uses cognitive reasoning to explain what is happening.",
            category=SkillCategory.RESEARCH,
            tags=["vision", "screen", "explain"],
            icon="monitor",
            required_capabilities=["SCREENSHOT"],
            required_workflows=[]
        ),
        SkillManifest(
            id="skill_research_topic",
            name="Research Topic",
            description="Opens a browser and searches the web for a given topic.",
            category=SkillCategory.RESEARCH,
            tags=["web", "browser", "search"],
            icon="globe",
            required_capabilities=["OPEN_GOOGLE_SEARCH"]
        ),
        SkillManifest(
            id="skill_system_info",
            name="System Information",
            description="Gathers comprehensive system information.",
            category=SkillCategory.SYSTEM,
            tags=["diagnostics", "info"],
            icon="cpu",
            required_workflows=[],
            # In Phase 11, we will mock execution mapping to a workflow
            workflow_template_id="tpl_coding" # Reusing a known workflow for demo purposes
        ),
        SkillManifest(
            id="skill_project_setup",
            name="Project Setup",
            description="Scaffolds a standard project folder structure.",
            category=SkillCategory.PRODUCTIVITY,
            tags=["files", "setup"],
            icon="folder"
        ),
        SkillManifest(
            id="skill_clipboard_assist",
            name="Clipboard Assistant",
            description="Reads clipboard and performs NLP processing.",
            category=SkillCategory.UTILITIES,
            tags=["clipboard", "text"],
            icon="clipboard"
        )
    ]
    
    for skill in builtins:
        skills_registry.register(skill)
