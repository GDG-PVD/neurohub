"""Mock A2A SDK implementation for demo purposes."""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import json


@dataclass
class AgentCard:
    """Mock Agent Card."""
    agent_id: str
    name: str
    description: str
    capabilities: List[str]
    endpoint: str


@dataclass
class Task:
    """Mock Task."""
    task_id: str
    type: str
    data: Dict[str, Any]
    source_agent: Optional[str] = None


@dataclass 
class Message:
    """Mock Message."""
    message_id: str
    content: Any
    metadata: Optional[Dict[str, Any]] = None


class A2AClient:
    """Mock A2A Client."""
    
    def __init__(self, agent_card: AgentCard):
        self.agent_card = agent_card
        self.registered = False
    
    async def register(self) -> bool:
        """Mock registration."""
        self.registered = True
        return True
    
    async def send_task(self, target_agent: str, task: Task) -> Message:
        """Mock task sending."""
        return Message(
            message_id=f"msg_{task.task_id}",
            content={"status": "received", "task_id": task.task_id}
        )
    
    async def receive_task(self) -> Optional[Task]:
        """Mock task receiving."""
        return None
    
    def get_status(self) -> Dict[str, Any]:
        """Get client status."""
        return {
            "registered": self.registered,
            "agent_id": self.agent_card.agent_id
        }
    
    async def discover_agents(self) -> List[AgentCard]:
        """Mock agent discovery."""
        # Return some mock agents for demo
        return [
            AgentCard(
                agent_id="context-analysis",
                name="Context Analysis Agent",
                description="Analyzes conversation context",
                capabilities=["analyze_conversation"],
                endpoint="http://localhost:8002"
            ),
            AgentCard(
                agent_id="action-planning",
                name="Action Planning Agent", 
                description="Extracts action items",
                capabilities=["extract_actions"],
                endpoint="http://localhost:8003"
            )
        ]
    
    def register_handler(self, handler_name: str, handler_func):
        """Mock handler registration."""
        # Store handlers internally
        if not hasattr(self, '_handlers'):
            self._handlers = {}
        self._handlers[handler_name] = handler_func