from typing import Dict, Any
from app.core.engine.capability_manager import capability_manager
from app.core.engine import permission_manager

class ExecutionValidator:
    def __init__(self):
        pass

    def validate(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validates if an action is safe and allowed to execute.
        Checks existence, permissions, and ambiguous params.
        """
        # 1. Capability exists
        cap = capability_manager.get_capability(action)
        if not cap:
            return {"valid": False, "reason": f"Capability {action} does not exist."}
            
        # 2. Permissions (Assuming a basic permission hook for now)
        if not permission_manager.check_permission("cognitive", action):
            return {"valid": False, "reason": f"Permission denied for {action}."}
            
        # 3. Dangerous parameters (example: rm -rf /)
        if action == "DELETE_PATH":
            path = params.get("path", "")
            if path in ["C:\\", "/", "C:\\Windows"]:
                return {"valid": False, "reason": "Dangerous path specified for deletion."}
                
        return {"valid": True, "reason": "OK"}

execution_validator = ExecutionValidator()
