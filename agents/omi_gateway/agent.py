"""OMI Gateway Agent

Main A2A agent that bridges OMI device with the multi-agent ecosystem.
"""

import asyncio
import os
from typing import Dict, Any, Optional
from datetime import datetime

import structlog
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from core.a2a_client import A2AAgent, AgentCapability, A2AOrchestrator, InteractionMode
from integrations.omi_connector import OMIConnector

logger = structlog.get_logger()


class OMIGatewayAgent(A2AAgent):
    """Gateway agent for OMI device integration."""
    
    def __init__(self):
        # Define agent capabilities
        capabilities = [
            AgentCapability(
                name="process_conversation",
                description="Process a conversation from OMI device",
                input_schema={
                    "type": "object",
                    "properties": {
                        "transcript": {"type": "string"},
                        "audio_url": {"type": "string"},
                        "metadata": {"type": "object"}
                    },
                    "required": ["transcript"]
                },
                output_schema={
                    "type": "object",
                    "properties": {
                        "analysis": {"type": "object"},
                        "actions": {"type": "array"},
                        "summary": {"type": "string"}
                    }
                }
            ),
            AgentCapability(
                name="get_status",
                description="Get current agent status",
                input_schema={"type": "object"},
                output_schema={
                    "type": "object",
                    "properties": {
                        "status": {"type": "string"},
                        "connected_devices": {"type": "integer"},
                        "processed_conversations": {"type": "integer"}
                    }
                }
            )
        ]
        
        super().__init__(
            agent_id="omi-gateway",
            name="OMI Conversation Gateway",
            port=int(os.getenv("GATEWAY_AGENT_PORT", 8001)),
            capabilities=capabilities
        )
        
        # Initialize components
        self.omi_connector = OMIConnector(
            api_url=os.getenv("OMI_API_URL"),
            api_key=os.getenv("OMI_API_KEY")
        )
        self.orchestrator = A2AOrchestrator(self)
        
        # Stats
        self.stats = {
            "connected_devices": 0,
            "processed_conversations": 0,
            "start_time": datetime.now()
        }
        
        # WebSocket connections
        self.websocket_clients = set()
        
        # Register handlers
        self.register_handler("process_conversation", self.handle_process_conversation)
        self.register_handler("get_status", self.handle_get_status)
    
    async def handle_process_conversation(
        self,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process a conversation through the multi-agent system."""
        transcript = data.get("transcript", "")
        metadata = data.get("metadata", {})
        
        logger.info("Processing conversation", length=len(transcript))
        
        # Define the multi-agent workflow
        workflow = [
            {
                "agent": "context-analysis",
                "task": "analyze_context",
                "data": {
                    "transcript": transcript,
                    "user_id": metadata.get("user_id")
                },
                "save_to_context": "context_analysis"
            },
            {
                "agent": "action-planning",
                "task": "extract_actions",
                "data": {"transcript": transcript},
                "use_context": True,
                "save_to_context": "actions"
            }
        ]
        
        # Execute workflow
        try:
            results = await self.orchestrator.execute_workflow(workflow)
            
            # Aggregate results
            context_result = results[0]
            action_result = results[1]
            
            # If actions were identified, trigger additional agents
            if action_result.get("actions"):
                parallel_tasks = []
                
                for action in action_result["actions"]:
                    if action["type"] == "send_email":
                        parallel_tasks.append({
                            "agent": "communication",
                            "task": "send_email",
                            "data": action["data"]
                        })
                    elif action["type"] == "search_knowledge":
                        parallel_tasks.append({
                            "agent": "knowledge",
                            "task": "search",
                            "data": {"query": action["data"]["query"]}
                        })
                
                if parallel_tasks:
                    await self.orchestrator.parallel_tasks(parallel_tasks)
            
            # Update stats
            self.stats["processed_conversations"] += 1
            
            # Notify WebSocket clients
            await self.broadcast_update({
                "type": "conversation_processed",
                "data": {
                    "summary": context_result.get("summary", ""),
                    "actions": action_result.get("actions", []),
                    "timestamp": datetime.now().isoformat()
                }
            })
            
            return {
                "analysis": context_result,
                "actions": action_result.get("actions", []),
                "summary": context_result.get("summary", "")
            }
            
        except Exception as e:
            logger.error("Failed to process conversation", error=str(e))
            return {
                "error": str(e),
                "analysis": {},
                "actions": [],
                "summary": ""
            }
    
    async def handle_get_status(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Get current agent status."""
        uptime = (datetime.now() - self.stats["start_time"]).total_seconds()
        
        return {
            "status": "active",
            "connected_devices": self.stats["connected_devices"],
            "processed_conversations": self.stats["processed_conversations"],
            "uptime_seconds": uptime,
            "websocket_clients": len(self.websocket_clients)
        }
    
    async def handle_omi_audio(self, audio_data: bytes, metadata: Dict[str, Any]):
        """Handle incoming audio from OMI device."""
        # Process through OMI connector
        result = await self.omi_connector.process_audio(audio_data, metadata)
        
        if result.get("transcript"):
            # Process the conversation
            conversation_result = await self.handle_process_conversation({
                "transcript": result["transcript"],
                "audio_url": result.get("audio_url"),
                "metadata": metadata
            })
            
            return conversation_result
    
    async def broadcast_update(self, message: Dict[str, Any]):
        """Broadcast update to all WebSocket clients."""
        disconnected = set()
        
        for websocket in self.websocket_clients:
            try:
                await websocket.send_json(message)
            except Exception as e:
                logger.warning("Failed to send update to websocket", error=str(e))
                disconnected.add(websocket)
        
        # Clean up disconnected clients
        self.websocket_clients -= disconnected


# FastAPI app for WebSocket and HTTP endpoints
app = FastAPI(title="OMI Gateway Agent")

# Configure CORS based on environment
allowed_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:3001").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins if os.getenv("ENV") == "production" else ["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Global agent instance
agent: Optional[OMIGatewayAgent] = None


@app.on_event("startup")
async def startup_event():
    global agent
    agent = OMIGatewayAgent()
    # Start A2A server in background
    asyncio.create_task(agent.start())
    # Refresh agent registry
    await agent.orchestrator.refresh_registry()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    agent.websocket_clients.add(websocket)
    agent.stats["connected_devices"] += 1
    
    try:
        while True:
            # Receive data from OMI device
            data = await websocket.receive_json()
            
            if data.get("type") == "audio":
                # Handle audio data
                audio_bytes = data.get("audio_bytes", b"")
                metadata = data.get("metadata", {})
                
                result = await agent.handle_omi_audio(audio_bytes, metadata)
                await websocket.send_json(result)
                
            elif data.get("type") == "transcript":
                # Handle transcript directly
                result = await agent.handle_process_conversation(data)
                await websocket.send_json(result)
                
    except WebSocketDisconnect:
        agent.websocket_clients.remove(websocket)
        agent.stats["connected_devices"] -= 1


@app.get("/health")
async def health_check():
    return await agent.handle_get_status({})


if __name__ == "__main__":
    uvicorn.run(
        "agent:app",
        host="0.0.0.0",
        port=int(os.getenv("GATEWAY_AGENT_PORT", 8001)),
        reload=os.getenv("ENV", "development") == "development"
    )