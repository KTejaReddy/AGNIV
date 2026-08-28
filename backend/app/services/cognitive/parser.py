import json
from typing import Dict, Any
from app.core.logging import logger

class ResponseParser:
    def __init__(self):
        pass

    def parse(self, raw_response: str) -> Dict[str, Any]:
        """
        Safely parses LLM responses into structured Intents.
        """
        clean = raw_response.strip()
        
        # Strip markdown json blocks if the model hallucinates them
        if clean.startswith("```json"):
            clean = clean[7:]
        if clean.startswith("```"):
            clean = clean[3:]
        if clean.endswith("```"):
            clean = clean[:-3]
            
        clean = clean.strip()
        
        try:
            return json.loads(clean)
        except Exception as e:
            logger.error(f"Failed to parse LLM response: {raw_response}")
            return {
                "type": "ERROR",
                "text": "I could not understand the generated response."
            }

response_parser = ResponseParser()
