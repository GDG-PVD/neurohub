"""Knowledge Agent - Retrieves relevant information for conversations."""

import os
from typing import Dict, Any
from fastapi import FastAPI
import uvicorn

from core.a2a_client import A2AAgent, AgentCapability

app = FastAPI(title="Knowledge Agent")


class KnowledgeAgent(A2AAgent):
    """Agent that retrieves relevant knowledge and context."""
    
    def __init__(self):
        capabilities = [
            AgentCapability(
                name="retrieve_knowledge",
                description="Retrieve relevant information for a topic",
                input_schema={
                    "type": "object",
                    "properties": {
                        "query": {"type": "string"},
                        "context": {"type": "string"}
                    }
                },
                output_schema={
                    "type": "object",
                    "properties": {
                        "relevant_info": {"type": "array", "items": {"type": "string"}},
                        "sources": {"type": "array", "items": {"type": "string"}}
                    }
                }
            )
        ]
        
        super().__init__(
            agent_id="knowledge",
            name="Knowledge Agent",
            port=int(os.getenv("A2A_AGENT_PORT", 8004)),
            capabilities=capabilities,
            description="Retrieves relevant information and context"
        )
    
    async def handle_retrieve_knowledge(self, query: str, context: str) -> Dict[str, Any]:
        """Retrieve relevant knowledge."""
        # Placeholder implementation
        # In real implementation, this would search knowledge bases
        return {
            "relevant_info": [
                "Previous API discussion was 2 weeks ago",
                "Edge cases were identified in testing phase"
            ],
            "sources": [
                "Meeting notes from 2024-01-10",
                "Testing documentation"
            ]
        }


# Global agent instance
agent = None


@app.on_event("startup")
async def startup_event():
    global agent
    agent = KnowledgeAgent()
    await agent.start()


@app.get("/health")
async def health_check():
    return {"status": "healthy", "agent": "knowledge"}


@app.get("/.well-known/agent.json")
async def get_agent_card():
    """Return A2A agent card."""
    return {
        "agent_id": agent.agent_id,
        "name": agent.name,
        "description": agent.description,
        "capabilities": [
            {
                "name": cap.name,
                "description": cap.description
            }
            for cap in agent.capabilities
        ]
    }


@app.post("/process")
async def process_task(request: Dict[str, Any]):
    """Process A2A task."""
    task_type = request.get("type")
    data = request.get("data", {})
    
    if task_type == "retrieve_knowledge":
        result = await agent.handle_retrieve_knowledge(
            data.get("query", ""),
            data.get("context", "")
        )
        return {"result": result}
    
    return {"error": "Unknown task type"}


if __name__ == "__main__":
    uvicorn.run(
        "agents.knowledge.agent:app",
        host="0.0.0.0",
        port=int(os.getenv("A2A_AGENT_PORT", 8004)),
        reload=False
    )