from typing import Optional
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.database.models import Permission
from app.core.logging import logger

SAFE_CAPABILITIES = {
    "OPEN_APPLICATION", "OPEN_URL", "COPY_TEXT", "PASTE_TEXT", 
    "SPEAK_TEXT", "READ_CLIPBOARD", "GET_SYSTEM_INFO", 
    "START_LISTENING", "STOP_LISTENING"
}

SENSITIVE_CAPABILITIES = {
    "DELETE_FILE", "DELETE_PATH", "SHUTDOWN", "FORMAT_DRIVE", "RUN_POWERSHELL"
}

class PermissionManager:
    def __init__(self):
        pass

    async def initialize(self):
        logger.info("Permission Manager initialized")

    def check_permission(self, capability_name: str) -> bool:
        with SessionLocal() as db:
            perm = db.query(Permission).filter(Permission.capability_name == capability_name).first()
            if not perm:
                # Default behavior if unmapped
                if capability_name in SAFE_CAPABILITIES:
                    logger.info(f"[PermissionManager] Capability: {capability_name} | Rule: ALWAYS_ALLOW | Source: Safe Defaults | Reason: No default record exists")
                    return True
                elif capability_name in SENSITIVE_CAPABILITIES:
                    logger.warning(f"[PermissionManager] Capability: {capability_name} | Rule: ASK | Source: Sensitive Defaults | Reason: No default record exists")
                    return True # Returning true as a mock for ASK phase
                else:
                    logger.info(f"[PermissionManager] Capability: {capability_name} | Rule: DENY | Source: Default Fallback | Reason: Unmapped and unknown")
                    return False
                
            rule = perm.rule
            if rule == "ALWAYS_ALLOW":
                logger.info(f"[PermissionManager] Capability: {capability_name} | Rule: ALWAYS_ALLOW | Source: permissions.db | Reason: Explicit mapping")
                return True
            elif rule == "NEVER_ALLOW":
                logger.info(f"[PermissionManager] Capability: {capability_name} | Rule: NEVER_ALLOW | Source: permissions.db | Reason: Explicit mapping")
                return False
            elif rule == "SESSION_ONLY":
                logger.info(f"[PermissionManager] Capability: {capability_name} | Rule: SESSION_ONLY | Source: permissions.db | Reason: Explicit mapping")
                return True
            elif rule == "ASK":
                logger.warning(f"[PermissionManager] Capability: {capability_name} | Rule: ASK | Source: permissions.db | Reason: Explicit mapping")
                # Mock: we return True for phase 2 since UI isn't intercepting asks
                return True
            
        logger.info(f"[PermissionManager] Capability: {capability_name} | Rule: DENY | Source: permissions.db | Reason: Unknown Rule Type")
        return False

permission_manager = PermissionManager()
