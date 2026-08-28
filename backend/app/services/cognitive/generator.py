from typing import Dict, Any

class ResponseGenerator:
    def __init__(self):
        pass

    def generate(self, intent: Dict[str, Any], execution_result: Dict[str, Any]) -> str:
        """
        Takes the parsed intent and the results of execution (if any)
        and formats a final conversational response string.
        """
        if intent.get("type") == "ERROR":
            return intent.get("text", "An error occurred.")
            
        if intent.get("type") == "REPLY":
            return intent.get("text", "")
            
        if intent.get("type") == "CLARIFY":
            return intent.get("text", "Could you clarify that?")
            
        if intent.get("type") == "ACTION":
            # Just acknowledging the action for now. 
            # Future expansion: send the execution_result back to LLM for summary
            action_name = intent.get("action", "action")
            status = execution_result.get("status", "completed")
            return f"The {action_name} action has {status}."
            
        return "I'm not sure how to respond."

response_generator = ResponseGenerator()
