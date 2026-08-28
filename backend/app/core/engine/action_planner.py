import json
from typing import Dict, Any, List
from pydantic import BaseModel
from app.core.logging import logger
from .event_bus import event_bus, Event
from app.services.cognitive.provider import provider_manager
import uuid
import time

class Plan(BaseModel):
    id: str
    mode: str
    goal: str
    reply: str
    steps: List[Dict[str, Any]]
    priority: int = 0
    timestamp: float

class ActionPlanner:
    def __init__(self):
        self.conversation_history = []

    async def initialize(self):
        event_bus.subscribe("INPUT_RECEIVED", self.handle_input_event)
        logger.info("Action Planner initialized")

    async def handle_input_event(self, event: Event):
        payload = event.payload.get("payload", {})
        input_type = event.payload.get("type")
        from app.services.voice.session import voice_session
        
        if input_type == "VOICE":
            text = payload.get("text", "")
            if not text:
                return
                
            voice_session.log(f"Groq request for parsing intent")
            
            # Format context window
            history_str = "\n".join([f"{msg['role']}: {msg['content']}" for msg in self.conversation_history[-8:]])
            if history_str:
                history_str = f"Previous conversation context:\n{history_str}\n\n"
                
            from app.core.engine.capability_manager import capability_manager
            capabilities_list = capability_manager.get_registered_capabilities_metadata()
            
            prompt = f"""{history_str}You are AGNIV, an AI assistant continuous voice companion. 
The user just said: '{text}'.

You have access to the following capabilities:
{capabilities_list}

Generate a structured execution plan. 
If multiple actions are required, generate multiple ordered steps.
If the request is conversational and requires no capabilities, output an empty steps array and just use the 'reply' field.
If a capability fails or doesn't exist, explain why in the 'reply' field.

Return ONLY valid JSON with no markdown formatting. Schema:
{{
  "mode": "conversation | desktop | screen | browser | workflow | memory | coding | reasoning | clarification | refusal",
  "goal": "A short summary of what the user wants to achieve",
  "reply": "The spoken response AGNIV should say out loud.",
  "steps": [
    {{
      "capability": "CAPABILITY_NAME",
      "params": {{
        "param1": "value1"
      }}
    }}
  ]
}}"""

            messages = [{"role": "system", "content": prompt}]
            
            await event_bus.publish(Event(
                id=str(uuid.uuid4()),
                type="LLM_STARTED",
                source="ActionPlanner",
                payload={"goal": "Parsing Intent"},
                timestamp=time.time()
            ))
            
            response_str = await provider_manager.generate(messages)
            
            await event_bus.publish(Event(
                id=str(uuid.uuid4()),
                type="LLM_FINISHED",
                source="ActionPlanner",
                payload={"response": response_str},
                timestamp=time.time()
            ))
            
            try:
                if response_str.startswith("```json"):
                    response_str = response_str[7:-3]
                elif response_str.startswith("```"):
                    response_str = response_str[3:-3]
                    
                parsed = json.loads(response_str)
                mode = parsed.get("mode", "conversation")
                goal = parsed.get("goal", "")
                reply = parsed.get("reply", "")
                steps = parsed.get("steps", [])
                
                self.conversation_history.append({"role": "user", "content": text})
                if reply:
                    self.conversation_history.append({"role": "assistant", "content": reply})
                    
                # Cap the history size to prevent memory leaks (Bug 4)
                if len(self.conversation_history) > 50:
                    self.conversation_history = self.conversation_history[-50:]
                    
                    
            except json.JSONDecodeError:
                voice_session.log(f"Error: Failed to parse JSON from Groq: {response_str}")
                mode = "error"
                goal = "Fallback"
                reply = "I'm sorry, my language model produced an invalid response."
                steps = []
                
        else:
            mode = "system"
            goal = payload.get("action", "UNKNOWN")
            steps = [{"capability": payload.get("action", "UNKNOWN"), "params": payload.get("parameters", {})}]
            reply = ""
            
        plan = Plan(
            id=str(uuid.uuid4()),
            mode=mode,
            goal=goal,
            reply=reply,
            steps=steps,
            priority=event.payload.get("priority", 0),
            timestamp=time.time()
        )
        
        voice_session.log(f"Execution Plan: {plan.goal} with {len(plan.steps)} steps.")
        
        await event_bus.publish(Event(
            id=str(uuid.uuid4()),
            type="PLAN_CREATED",
            source="ActionPlanner",
            payload=plan.dict(),
            timestamp=time.time()
        ))

action_planner = ActionPlanner()
