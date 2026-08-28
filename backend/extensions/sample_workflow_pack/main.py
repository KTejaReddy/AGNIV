"""
Sample Workflow Pack Extension — Developer Workflows
=====================================================
Demonstrates how to bundle pre-defined workflow templates
that get registered into the AGNIV Workflow Engine.
"""

DEVELOPER_WORKFLOWS = [
    {
        "id": "dev.open-ide",
        "name": "Open IDE",
        "description": "Opens the configured IDE application.",
        "steps": [
            {"capability": "OPEN_APPLICATION", "params": {"name": "code"}}
        ],
    },
    {
        "id": "dev.morning-setup",
        "name": "Morning Developer Setup",
        "description": "Opens IDE, terminal, and browser in sequence.",
        "steps": [
            {"capability": "OPEN_APPLICATION", "params": {"name": "code"}},
            {"capability": "OPEN_APPLICATION", "params": {"name": "WindowsTerminal"}},
            {"capability": "OPEN_URL", "params": {"url": "https://github.com"}},
        ],
    },
]


class Extension:
    def __init__(self, sdk):
        self.sdk = sdk

    def on_enable(self):
        # In a real implementation, these would be registered into the workflow engine
        self.sdk.log(f"Developer Workflow Pack: {len(DEVELOPER_WORKFLOWS)} workflows available.")
        for wf in DEVELOPER_WORKFLOWS:
            self.sdk.log(f"  - Workflow '{wf['name']}' ({wf['id']}) registered.")

    def on_disable(self):
        self.sdk.log("Developer Workflow Pack disabled.")

    def metadata(self) -> dict:
        return {
            "workflows": [wf["id"] for wf in DEVELOPER_WORKFLOWS],
            "count": len(DEVELOPER_WORKFLOWS),
        }
