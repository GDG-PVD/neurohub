"""
Agent Builder Template for NeuroHub Workshop
This template provides everything teams need to build their own agents
with MCP (Model Context Protocol) and A2A integration
"""

import os
import asyncio
import json
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
from abc import ABC, abstractmethod
import logging

from core.a2a_wrappers import A2AAgent, A2ATask

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MCPProvider(ABC):
    """Base class for MCP (Model Context Protocol) providers"""
    
    @abstractmethod
    async def complete(self, prompt: str, **kwargs) -> str:
        """Complete a prompt using the LLM"""
        pass
    
    @abstractmethod
    async def analyze(self, text: str, analysis_type: str) -> dict:
        """Analyze text for specific insights"""
        pass


class OpenAIMCPProvider(MCPProvider):
    """OpenAI implementation of MCP"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        
    async def complete(self, prompt: str, **kwargs) -> str:
        """Complete using OpenAI GPT"""
        # In production: Use actual OpenAI API
        # For workshop: Simulated response
        if not self.api_key or self.api_key == "demo":
            return f"[Demo response for: {prompt[:50]}...]"
        
        # Real implementation would call OpenAI here
        import openai
        # response = await openai.ChatCompletion.acreate(...)
        return "OpenAI response"
    
    async def analyze(self, text: str, analysis_type: str) -> dict:
        """Analyze text using OpenAI"""
        prompt = f"Analyze the following text for {analysis_type}:\n\n{text}"
        response = await self.complete(prompt)
        
        # Parse response into structured format
        return {
            "analysis_type": analysis_type,
            "result": response,
            "confidence": 0.85
        }


class ClaudeMCPProvider(MCPProvider):
    """Claude implementation of MCP"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        
    async def complete(self, prompt: str, **kwargs) -> str:
        """Complete using Claude"""
        if not self.api_key or self.api_key == "demo":
            return f"[Claude demo response for: {prompt[:50]}...]"
        
        # Real implementation would call Anthropic API
        return "Claude response"
    
    async def analyze(self, text: str, analysis_type: str) -> dict:
        """Analyze text using Claude"""
        return {
            "analysis_type": analysis_type,
            "result": f"Claude analysis of {analysis_type}",
            "confidence": 0.90
        }


class CustomAgent(A2AAgent):
    """
    Template for building custom agents for the workshop
    
    This template provides:
    1. MCP integration for LLM capabilities
    2. A2A protocol compliance
    3. OMI device integration
    4. External API integration patterns
    5. State management
    6. Error handling
    """
    
    def __init__(
        self,
        name: str,
        description: str,
        capabilities: List[str],
        mcp_provider: str = "openai",
        external_apis: Dict[str, Any] = None
    ):
        """
        Initialize your custom agent
        
        Args:
            name: Unique agent identifier
            description: What your agent does
            capabilities: List of capabilities (e.g., ["analyze", "summarize", "search"])
            mcp_provider: Which LLM to use ("openai", "claude", "local")
            external_apis: Dictionary of external API clients
        """
        super().__init__(name=name, capabilities=capabilities)
        
        self.description = description
        self.external_apis = external_apis or {}
        
        # Initialize MCP provider
        self.mcp = self._init_mcp_provider(mcp_provider)
        
        # Agent state
        self.state = {
            "processed_count": 0,
            "last_activity": None,
            "context_history": [],
            "user_preferences": {}
        }
        
        # Register task handlers
        self.task_handlers = {
            "analyze": self.handle_analyze,
            "process": self.handle_process,
            "query": self.handle_query,
            "integrate": self.handle_integrate
        }
        
        logger.info(f"Initialized {name} agent with {mcp_provider} MCP")
    
    def _init_mcp_provider(self, provider: str) -> MCPProvider:
        """Initialize the MCP provider"""
        if provider == "openai":
            return OpenAIMCPProvider()
        elif provider == "claude":
            return ClaudeMCPProvider()
        else:
            # Default to OpenAI
            return OpenAIMCPProvider()
    
    async def process_task(self, task: A2ATask) -> dict:
        """
        Main entry point for processing tasks
        
        This method routes tasks to appropriate handlers
        """
        logger.info(f"Processing task: {task.type} (ID: {task.id})")
        
        # Update state
        self.state["processed_count"] += 1
        self.state["last_activity"] = datetime.now().isoformat()
        
        # Route to handler
        handler = self.task_handlers.get(task.type, self.handle_unknown)
        
        try:
            result = await handler(task)
            result["agent"] = self.name
            result["task_id"] = task.id
            return result
            
        except Exception as e:
            logger.error(f"Error processing task: {e}")
            return {
                "status": "error",
                "error": str(e),
                "agent": self.name,
                "task_id": task.id
            }
    
    async def handle_analyze(self, task: A2ATask) -> dict:
        """
        Handle analysis tasks
        
        Override this method to implement your analysis logic
        """
        data = task.data
        text = data.get("text", "")
        analysis_type = data.get("analysis_type", "general")
        
        # Use MCP for analysis
        analysis = await self.mcp.analyze(text, analysis_type)
        
        # Add to context history
        self.state["context_history"].append({
            "timestamp": datetime.now().isoformat(),
            "type": "analysis",
            "summary": analysis["result"][:100]
        })
        
        return {
            "status": "success",
            "analysis": analysis,
            "metadata": {
                "text_length": len(text),
                "analysis_type": analysis_type
            }
        }
    
    async def handle_process(self, task: A2ATask) -> dict:
        """
        Handle processing tasks
        
        This is where you implement your main agent logic
        """
        # Extract data from task
        omi_memory = task.data.get("omi_memory")
        options = task.data.get("options", {})
        
        # Your processing logic here
        processed_result = await self.process_omi_memory(omi_memory, options)
        
        return {
            "status": "success",
            "result": processed_result
        }
    
    async def handle_query(self, task: A2ATask) -> dict:
        """
        Handle query tasks
        
        Use this for question-answering or search tasks
        """
        query = task.data.get("query", "")
        context = task.data.get("context", "")
        
        # Build prompt with context
        prompt = f"Context: {context}\n\nQuery: {query}\n\nAnswer:"
        
        # Get response from MCP
        response = await self.mcp.complete(prompt)
        
        return {
            "status": "success",
            "query": query,
            "answer": response
        }
    
    async def handle_integrate(self, task: A2ATask) -> dict:
        """
        Handle integration tasks with external APIs
        
        This shows how to integrate with external services
        """
        service = task.data.get("service")
        action = task.data.get("action")
        params = task.data.get("params", {})
        
        if service not in self.external_apis:
            return {
                "status": "error",
                "error": f"Service {service} not configured"
            }
        
        # Call external API
        api_client = self.external_apis[service]
        result = await self.call_external_api(api_client, action, params)
        
        return {
            "status": "success",
            "service": service,
            "action": action,
            "result": result
        }
    
    async def handle_unknown(self, task: A2ATask) -> dict:
        """Handle unknown task types"""
        return {
            "status": "error",
            "error": f"Unknown task type: {task.type}",
            "supported_types": list(self.task_handlers.keys())
        }
    
    async def process_omi_memory(self, omi_memory: dict, options: dict) -> dict:
        """
        Process OMI memory data
        
        Override this with your specific logic
        """
        # Example: Extract key information from OMI memory
        transcript = omi_memory.get("transcript", "")
        
        # Use MCP to process
        prompt = f"Extract key insights from: {transcript}"
        insights = await self.mcp.complete(prompt)
        
        return {
            "insights": insights,
            "word_count": len(transcript.split()),
            "processed_at": datetime.now().isoformat()
        }
    
    async def call_external_api(self, client: Any, action: str, 
                               params: dict) -> dict:
        """
        Call external API
        
        Implement your external API logic here
        """
        # Example implementation
        if hasattr(client, action):
            method = getattr(client, action)
            return await method(**params)
        else:
            return {"error": f"Action {action} not supported"}
    
    def get_state(self) -> dict:
        """Get current agent state"""
        return self.state.copy()
    
    def update_preferences(self, preferences: dict):
        """Update user preferences"""
        self.state["user_preferences"].update(preferences)


# Example: Building a Custom Research Assistant
class ResearchAssistantAgent(CustomAgent):
    """
    Example of extending the CustomAgent template
    This agent specializes in research tasks
    """
    
    def __init__(self):
        # Initialize with specific configuration
        super().__init__(
            name="research-assistant",
            description="Helps with research and fact-finding",
            capabilities=["research", "summarize", "fact_check"],
            mcp_provider="claude",  # Use Claude for research
            external_apis={
                "wikipedia": WikipediaClient(),
                "arxiv": ArxivClient(),
                "pubmed": PubMedClient()
            }
        )
        
        # Add research-specific state
        self.state["research_history"] = []
        self.state["saved_papers"] = []
    
    async def process_omi_memory(self, omi_memory: dict, options: dict) -> dict:
        """
        Override to add research-specific processing
        """
        transcript = omi_memory.get("transcript", "")
        
        # Extract research questions
        questions = await self.extract_research_questions(transcript)
        
        # Research each question
        results = []
        for question in questions:
            # Search multiple sources
            wiki_results = await self.search_wikipedia(question)
            arxiv_results = await self.search_arxiv(question)
            
            # Synthesize findings
            synthesis = await self.mcp.complete(
                f"Synthesize these research findings:\n"
                f"Wikipedia: {wiki_results}\n"
                f"ArXiv: {arxiv_results}\n"
                f"Question: {question}"
            )
            
            results.append({
                "question": question,
                "synthesis": synthesis,
                "sources": ["wikipedia", "arxiv"]
            })
        
        # Save to history
        self.state["research_history"].append({
            "timestamp": datetime.now().isoformat(),
            "questions": questions,
            "results": results
        })
        
        return {
            "research_count": len(questions),
            "findings": results,
            "session_id": datetime.now().isoformat()
        }
    
    async def extract_research_questions(self, transcript: str) -> List[str]:
        """Extract research questions from transcript"""
        prompt = (
            "Extract all research questions from this conversation. "
            "Return as a JSON list of questions:\n\n"
            f"{transcript}"
        )
        
        response = await self.mcp.complete(prompt)
        
        # Parse response (in production, use proper JSON parsing)
        questions = ["What is machine learning?", "How does AI work?"]  # Demo
        
        return questions
    
    async def search_wikipedia(self, query: str) -> str:
        """Search Wikipedia"""
        if "wikipedia" in self.external_apis:
            return await self.external_apis["wikipedia"].search(query)
        return "Wikipedia search not available"
    
    async def search_arxiv(self, query: str) -> str:
        """Search ArXiv"""
        if "arxiv" in self.external_apis:
            return await self.external_apis["arxiv"].search(query)
        return "ArXiv search not available"


# Stub implementations for demo
class WikipediaClient:
    async def search(self, query: str) -> str:
        return f"Wikipedia results for: {query}"

class ArxivClient:
    async def search(self, query: str) -> str:
        return f"ArXiv papers about: {query}"

class PubMedClient:
    async def search(self, query: str) -> str:
        return f"PubMed articles on: {query}"


# Workshop helper functions
async def test_custom_agent():
    """Test function for workshop participants"""
    
    print("🤖 Custom Agent Builder Demo\n")
    
    # Create a custom agent
    agent = CustomAgent(
        name="my-workshop-agent",
        description="My awesome workshop agent",
        capabilities=["analyze", "summarize"],
        mcp_provider="openai"
    )
    
    # Test with a simple task
    task = A2ATask(
        id="test-1",
        type="analyze",
        data={
            "text": "The workshop is going great! We're learning about AI agents.",
            "analysis_type": "sentiment"
        }
    )
    
    result = await agent.process_task(task)
    print(f"Result: {json.dumps(result, indent=2)}")
    
    # Test the research assistant
    print("\n🔬 Research Assistant Demo\n")
    
    research_agent = ResearchAssistantAgent()
    
    research_task = A2ATask(
        id="research-1",
        type="process",
        data={
            "omi_memory": {
                "transcript": "I'm curious about how machine learning works "
                             "and what are the latest developments in AI."
            },
            "options": {}
        }
    )
    
    research_result = await research_agent.process_task(research_task)
    print(f"Research Result: {json.dumps(research_result, indent=2)}")


if __name__ == "__main__":
    # Run the demo
    asyncio.run(test_custom_agent())