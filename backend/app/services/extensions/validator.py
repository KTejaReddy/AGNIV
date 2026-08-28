"""Extension Validator — checks manifests for completeness, version compatibility, and permission safety."""
import json
import os
import re
from typing import Tuple, List
from .models import ExtensionManifest, Permission
from app.core.logging import logger

AGNIV_VERSION = "1.0.0"


def _parse_version(v: str) -> Tuple[int, int, int]:
    parts = re.sub(r"[^0-9.]", "", v).split(".")
    parts = (parts + ["0", "0", "0"])[:3]
    return tuple(int(p) for p in parts)


def _version_satisfies(constraint: str, actual: str) -> bool:
    """Simple constraint checker: >=x.y.z, <=x.y.z, ==x.y.z"""
    try:
        if constraint.startswith(">="):
            return _parse_version(actual) >= _parse_version(constraint[2:])
        elif constraint.startswith("<="):
            return _parse_version(actual) <= _parse_version(constraint[2:])
        elif constraint.startswith("=="):
            return _parse_version(actual) == _parse_version(constraint[2:])
        else:
            return _parse_version(actual) >= _parse_version(constraint)
    except Exception:
        return True  # Be permissive on parse errors


class ExtensionValidator:
    DANGEROUS_PERMISSIONS = {Permission.FILE_WRITE, Permission.NETWORK, Permission.DESKTOP}

    def validate_manifest_file(self, manifest_path: str) -> Tuple[bool, List[str]]:
        """Load and validate a manifest JSON file."""
        errors = []
        if not os.path.exists(manifest_path):
            return False, ["agniv-extension.json not found"]

        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                raw = json.load(f)
            manifest = ExtensionManifest(**raw)
        except Exception as e:
            return False, [f"Manifest parse error: {e}"]

        return self.validate_manifest(manifest)

    def validate_manifest(self, manifest: ExtensionManifest) -> Tuple[bool, List[str]]:
        errors = []

        # ID format
        if not re.match(r"^[a-z0-9_\-]+$", manifest.id):
            errors.append("Extension id must be lowercase alphanumeric with hyphens/underscores only.")

        # Version format
        if not re.match(r"^\d+\.\d+\.\d+$", manifest.version):
            errors.append(f"Version '{manifest.version}' must be in semver format (x.y.z).")

        # AGNIV compatibility
        if not _version_satisfies(manifest.agniv_version, AGNIV_VERSION):
            errors.append(
                f"Extension requires AGNIV {manifest.agniv_version}, but current version is {AGNIV_VERSION}."
            )

        # Warn about dangerous perms
        declared_dangerous = [p for p in manifest.permissions if p in self.DANGEROUS_PERMISSIONS]
        if declared_dangerous:
            logger.warning(
                f"Extension '{manifest.id}' declares elevated permissions: {[p.value for p in declared_dangerous]}"
            )

        return len(errors) == 0, errors

    def validate_entry_point(self, extension_path: str, entry_point: str) -> Tuple[bool, List[str]]:
        full_path = os.path.join(extension_path, entry_point)
        if not os.path.exists(full_path):
            return False, [f"Entry point '{entry_point}' not found in extension directory."]
        return True, []


extension_validator = ExtensionValidator()
