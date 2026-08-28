import time
import json
import asyncio
from app.core.logging import logger
from app.core.engine.capability_manager import capability_manager
from app.core.engine import event_bus, Event
from .session import cognitive_session
from .context import context_builder
from .conversation import conversation_manager
from .decision import decision_engine
from .validator import execution_validator
from .prompt import prompt_builder
from .provider import provider_manager
from .parser import response_parser
from .generator import response_generator

class ThinkingPipeline:
    def __init__(self):
        pass

    async def process_input(self, text: str):
        start_time = time.time()
        cognitive_session.reset_turn()
        
        # 1. Context Builder
        context = context_builder.build_unified_context()
        cognitive_session.current_context = context
        
        # 2. Decision Engine
        decision = await decision_engine.evaluate(text, context)
        execution_path = decision["path"]
        cognitive_session.current_execution_path = execution_path

        raw_intent = None
        
        if execution_path == "RULE" or execution_path == "KNOWLEDGE" or execution_path == "SKILL":
            raw_intent = decision["intent"]
        else:
            # 4. Prompt Builder
            messages = prompt_builder.build(text, context, conversation_manager.get_recent())
            cognitive_session.prompt_size = len(str(messages)) // 4  # rough token est
            
            # 5. Provider Inference
            raw_response = await provider_manager.generate(messages)
            cognitive_session.raw_llm_response = raw_response
            
            # 6. Parser
            raw_intent = response_parser.parse(raw_response)

        cognitive_session.parsed_intent = raw_intent

        # 7. Validator
        if raw_intent and raw_intent.get("type") == "ACTION":
            action = raw_intent.get("action")
            params = raw_intent.get("params", {})
            
            is_valid, reason = execution_validator.validate(action, params, context)
            cognitive_session.validation_result = {"is_valid": is_valid, "reason": reason}
            
            if is_valid:
                logger.info(f"Validator PASSED: {action}")
                # Dispatch execution
                await event_bus.publish(Event(
                    id=str(time.time()),
                    type="INTENT_EXECUTED",
                    source="CognitiveEngine",
                    payload={"action": action, "params": params},
                    timestamp=time.time()
                ))
            else:
                logger.warning(f"Validator BLOCKED: {reason}")
                
        elif raw_intent and raw_intent.get("type") == "SKILL":
            from app.services.skills.manager import skills_manager
            skill_id = raw_intent.get("skill_id")
            logger.info(f"Delegating to Skills Engine: {skill_id}")
            skills_manager.run(skill_id)
            cognitive_session.validation_result = {"is_valid": True, "reason": "Skill delegated"}

        # 8. Final Generation
        final_response = response_generator.generate(raw_intent, cognitive_session.validation_result)
        
        # 9. History
        conversation_manager.add_turn(text, final_response)
        
        cognitive_session.latency_ms = int((time.time() - start_time) * 1000)
        return final_response

thinking_pipeline = ThinkingPipeline()
