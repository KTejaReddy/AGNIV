import pytest
from app.services.extensions.validator import extension_validator
from app.services.extensions.models import ExtensionManifest, ExtensionType
from app.core.engine.permission_manager import permission_manager

def test_manifest_validation():
    valid_manifest = ExtensionManifest(
        id="test-ext",
        name="Test Extension",
        version="1.0.0",
        type=ExtensionType.CAPABILITY,
        description="A test",
        author={"name": "Tester"},
        agniv_version=">=1.0.0",
        entry_point="main.py",
        permissions=["desktop"]
    )
    
    ok, errors = extension_validator.validate_manifest(valid_manifest)
    assert ok == True
    assert len(errors) == 0

def test_manifest_invalid_version():
    invalid_manifest = ExtensionManifest(
        id="test-ext",
        name="Test Extension",
        version="1.0", # invalid semver
        type=ExtensionType.CAPABILITY,
        description="A test",
        author={"name": "Tester"},
        agniv_version=">=1.0.0",
        entry_point="main.py"
    )
    
    ok, errors = extension_validator.validate_manifest(invalid_manifest)
    assert ok == False
    assert len(errors) > 0


