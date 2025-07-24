"""Action Planning Agent - Extracts actionable items from conversations."""

import os
from typing import Dict, Any
from fastapi import FastAPI
import uvicorn

from core.a2a_client import A2AAgent, AgentCapability

app = FastAPI(title="Action Planning Agent")


class ActionPlanningAgent(A2AAgent):
    """Agent that extracts action items from conversations."""
    
    def __init__(self):
        capabilities = [
            AgentCapability(
                name="extract_actions",
                description="Extract action items from conversation",
                input_schema={
                    "type": "object",
                    "properties": {
                        "transcript": {"type": "string"}
                    }
                },
                output_schema={
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "task": {"type": "string"},
                            "assignee": {"type": "string"},
                            "deadline": {"type": "string"}
                        }
                    }
                }
            )
        ]
        
        super().__init__(
            agent_id="action-planning",
            name="Action Planning Agent",
            port=int(os.getenv("A2A_AGENT_PORT", 8003)),
            capabilities=capabilities,
            description="Extracts action items and tasks from conversations"
        )
    
    async def handle_extract_actions(self, transcript: str) -> Dict[str, Any]:
        """Extract action items from transcript."""
        # Placeholder implementation
        # In real implementation, this would use an LLM
        return {
            "actions": [
                {
                    "task": "Send project summary",
                    "assignee": "John",
                    "deadline": "5 PM today"
                }
            ]
        }


# Global agent instance
agent = None


@app.on_event("startup")
async def startup_event():
    global agent
    agent = ActionPlanningAgent()
    await agent.start()


@app.get("/health")
async def health_check():
    return {"status": "healthy", "agent": "action-planning"}


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
    
    if task_type == "extract_actions":
        result = await agent.handle_extract_actions(data.get("transcript", ""))
        return {"result": result}
    
    return {"error": "Unknown task type"}


if __name__ == "__main__":
    uvicorn.run(
        "agents.action_planning.agent:app",
        host="0.0.0.0",
        port=int(os.getenv("A2A_AGENT_PORT", 8003)),
        reload=False
    )