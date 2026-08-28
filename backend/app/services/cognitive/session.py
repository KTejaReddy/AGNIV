from typing import Dict, Any, List

class CognitiveSessionManager:
    def __init__(self):
        self.active_provider = "groq"
        self.reasoning_latency = 0
        self.prompt_size = 0
        self.response_size = 0
        self.current_execution_path = None
        self.current_intent = None
        self.current_context = {}
        self.raw_llm_response = None
        self.parsed_intent = None
        self.validation_result = None
        self.latency_ms = 0

    def get_status(self) -> Dict[str, Any]:
        from .provider import provider_manager
        return {
            "provider": self.active_provider,
            "status": provider_manager.connection_status,
            "latency": self.reasoning_latency,
            "prompt_size": self.prompt_size,
            "response_size": self.response_size,
            "execution_path": self.current_execution_path,
            "intent": self.current_intent,
            "context_keys": list(self.current_context.keys())
        }
        
    def reset_turn(self):
        self.reasoning_latency = 0
        self.prompt_size = 0
        self.response_size = 0
        self.current_execution_path = None
        self.current_intent = None
        self.current_context = {}
        self.raw_llm_response = None
        self.parsed_intent = None
        self.validation_result = None
        self.latency_ms = 0

cognitive_session = CognitiveSessionManager()
