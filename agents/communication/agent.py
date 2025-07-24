"""Communication Agent - Handles external communications and notifications."""

import os
from typing import Dict, Any
from fastapi import FastAPI
import uvicorn

from core.a2a_client import A2AAgent, AgentCapability

app = FastAPI(title="Communication Agent")


class CommunicationAgent(A2AAgent):
    """Agent that handles external communications."""
    
    def __init__(self):
        capabilities = [
            AgentCapability(
                name="send_notification",
                description="Send notifications or messages",
                input_schema={
                    "type": "object",
                    "properties": {
                        "recipient": {"type": "string"},
                        "message": {"type": "string"},
                        "type": {"type": "string", "enum": ["email", "sms", "slack"]}
                    }
                },
                output_schema={
                    "type": "object",
                    "properties": {
                        "status": {"type": "string"},
                        "message_id": {"type": "string"}
                    }
                }
            )
        ]
        
        super().__init__(
            agent_id="communication",
            name="Communication Agent",
            port=int(os.getenv("A2A_AGENT_PORT", 8005)),
            capabilities=capabilities,
            description="Handles external communications and notifications"
        )
    
    async def handle_send_notification(
        self, 
        recipient: str, 
        message: str, 
        type: str
    ) -> Dict[str, Any]:
        """Send a notification."""
        # Placeholder implementation
        # In real implementation, this would integrate with email/SMS/Slack APIs
        return {
            "status": "sent",
            "message_id": f"msg_{type}_{recipient[:5]}_12345"
        }


# Global agent instance
agent = None


@app.on_event("startup")
async def startup_event():
    global agent
    agent = CommunicationAgent()
    await agent.start()


@app.get("/health")
async def health_check():
    return {"status": "healthy", "agent": "communication"}


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
    
    if task_type == "send_notification":
        result = await agent.handle_send_notification(
            data.get("recipient", ""),
            data.get("message", ""),
            data.get("type", "email")
        )
        return {"result": result}
    
    return {"error": "Unknown task type"}


if __name__ == "__main__":
    uvicorn.run(
        "agents.communication.agent:app",
        host="0.0.0.0",
        port=int(os.getenv("A2A_AGENT_PORT", 8005)),
        reload=False
    )