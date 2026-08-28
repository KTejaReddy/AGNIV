import json
from typing import Dict, Any, List

class PromptBuilder:
    def __init__(self):
        self.system_template = """You are AGNIV, an AI desktop operating companion.
You have access to the following context regarding the user's desktop state:
{context}

You must respond ONLY with a JSON object representing your intended action.
Do not include markdown blocks or conversational text.

Valid JSON formats:
1. To execute a capability:
{"type": "ACTION", "action": "<capability_name>", "params": {"<key>": "<value>"}}

2. To speak/reply to the user:
{"type": "REPLY", "text": "<your response>"}

3. To ask for clarification:
{"type": "CLARIFY", "text": "<your question>"}
"""

    def build(self, user_input: str, context: Dict[str, Any], history: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """
        Builds the minimal list of messages required for the LLM.
        """
        # Trim context down to just a string summary to save tokens
        context_str = json.dumps(context, indent=2)
        
        messages = [
            {"role": "system", "content": self.system_template.replace("{context}", context_str)}
        ]
        
        for msg in history:
            messages.append({"role": msg["role"], "content": msg["content"]})
            
        messages.append({"role": "user", "content": user_input})
        
        return messages

prompt_builder = PromptBuilder()
