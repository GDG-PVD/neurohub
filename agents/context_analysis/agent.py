"""Context Analysis Agent

Analyzes conversation context, user intent, and provides personalized insights.
"""

import os
from typing import Dict, Any, List, Optional
from datetime import datetime

import structlog
from openai import AsyncOpenAI
import uvicorn

from core.a2a_client import A2AAgent, AgentCapability

logger = structlog.get_logger()


class ContextAnalysisAgent(A2AAgent):
    """Agent for analyzing conversation context and user intent."""
    
    def __init__(self):
        capabilities = [
            AgentCapability(
                name="analyze_context",
                description="Analyze conversation context and extract insights",
                input_schema={
                    "type": "object",
                    "properties": {
                        "transcript": {"type": "string"},
                        "user_id": {"type": "string"},
                        "historical_context": {"type": "object"}
                    },
                    "required": ["transcript"]
                },
                output_schema={
                    "type": "object",
                    "properties": {
                        "summary": {"type": "string"},
                        "topics": {"type": "array"},
                        "sentiment": {"type": "string"},
                        "intent": {"type": "object"},
                        "entities": {"type": "array"},
                        "key_points": {"type": "array"}
                    }
                }
            ),
            AgentCapability(
                name="extract_user_preferences",
                description="Extract user preferences from conversation",
                input_schema={
                    "type": "object",
                    "properties": {
                        "transcript": {"type": "string"},
                        "existing_preferences": {"type": "object"}
                    }
                },
                output_schema={
                    "type": "object",
                    "properties": {
                        "preferences": {"type": "object"},
                        "confidence_scores": {"type": "object"}
                    }
                }
            )
        ]
        
        super().__init__(
            agent_id="context-analysis",
            name="Context Analysis Agent",
            port=int(os.getenv("CONTEXT_AGENT_PORT", 8002)),
            capabilities=capabilities
        )
        
        # Initialize OpenAI client
        self.openai = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Register handlers
        self.register_handler("analyze_context", self.handle_analyze_context)
        self.register_handler("extract_user_preferences", self.handle_extract_preferences)
    
    async def handle_analyze_context(
        self,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze conversation context using LLM."""
        transcript = data.get("transcript", "")
        user_id = data.get("user_id")
        historical_context = data.get("historical_context", {})
        
        logger.info("Analyzing context", transcript_length=len(transcript))
        
        # Build context prompt
        system_prompt = """
        You are an expert conversation analyst. Analyze the given conversation and extract:
        1. A brief summary (2-3 sentences)
        2. Main topics discussed
        3. Overall sentiment (positive, neutral, negative)
        4. User intent (what they're trying to achieve)
        5. Key entities (people, places, organizations, dates)
        6. Key points or takeaways
        
        Provide the analysis in a structured JSON format.
        """
        
        user_prompt = f"""
        Conversation transcript:
        {transcript}
        
        {f"Previous context: {historical_context}" if historical_context else ""}
        
        Analyze this conversation and provide insights.
        """
        
        try:
            # Call OpenAI for analysis
            response = await self.openai.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.3
            )
            
            analysis = response.choices[0].message.content
            import json
            analysis_data = json.loads(analysis)
            
            # Ensure all expected fields are present
            result = {
                "summary": analysis_data.get("summary", ""),
                "topics": analysis_data.get("topics", []),
                "sentiment": analysis_data.get("sentiment", "neutral"),
                "intent": analysis_data.get("intent", {}),
                "entities": analysis_data.get("entities", []),
                "key_points": analysis_data.get("key_points", []),
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info(
                "Context analysis complete",
                topics=len(result["topics"]),
                entities=len(result["entities"])
            )
            
            return result
            
        except Exception as e:
            logger.error("Failed to analyze context", error=str(e))
            return {
                "summary": "Error analyzing conversation",
                "topics": [],
                "sentiment": "neutral",
                "intent": {},
                "entities": [],
                "key_points": [],
                "error": str(e)
            }
    
    async def handle_extract_preferences(
        self,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Extract user preferences from conversation."""
        transcript = data.get("transcript", "")
        existing_preferences = data.get("existing_preferences", {})
        
        system_prompt = """
        Extract user preferences from the conversation. Look for:
        - Communication preferences
        - Topic interests
        - Time preferences
        - Product/service preferences
        - Personal values or priorities
        
        Return preferences with confidence scores (0-1).
        """
        
        user_prompt = f"""
        Transcript: {transcript}
        
        Existing preferences: {existing_preferences}
        
        Extract any new or updated preferences.
        """
        
        try:
            response = await self.openai.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.3
            )
            
            import json
            preferences_data = json.loads(response.choices[0].message.content)
            
            return {
                "preferences": preferences_data.get("preferences", {}),
                "confidence_scores": preferences_data.get("confidence_scores", {})
            }
            
        except Exception as e:
            logger.error("Failed to extract preferences", error=str(e))
            return {
                "preferences": {},
                "confidence_scores": {},
                "error": str(e)
            }


if __name__ == "__main__":
    import asyncio
    
    async def main():
        agent = ContextAnalysisAgent()
        await agent.start()
    
    asyncio.run(main())