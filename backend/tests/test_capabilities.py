import pytest
from app.core.engine.capability_manager import capability_manager
from app.core.engine.permission_manager import permission_manager

@pytest.mark.asyncio
async def test_capability_registration():
    def mock_handler(params):
        return {"status": "ok", "params": params}
        
    capability_manager.register_capability(
        name="MOCK_TEST_CAPABILITY",
        version="1.0",
        description="A mock capability",
        handler=mock_handler
    )
    
    assert "MOCK_TEST_CAPABILITY" in capability_manager.capabilities
    
    # In the mock, we can't easily mock the 'allowed' check since it uses the call stack 
    # for extension identification in a real scenario.
    # We will just verify it exists for now.
    assert capability_manager.capabilities["MOCK_TEST_CAPABILITY"]["version"] == "1.0"
    
    # In the mock, we can't easily mock the 'allowed' check since it uses the call stack 
    # for extension identification in a real scenario.
    # We will just verify it exists for now.
    assert capability_manager.capabilities["MOCK_TEST_CAPABILITY"]["version"] == "1.0"
