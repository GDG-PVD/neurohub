"""A2A Protocol Client Wrapper

Provides a simplified interface for A2A agent communication.
"""

import asyncio
import json
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum

from a2a_sdk import A2AClient, AgentCard, Task, Message
import structlog

logger = structlog.get_logger()


class InteractionMode(Enum):
    SYNC = "sync"
    STREAM = "stream"
    ASYNC = "async"


@dataclass
class AgentCapability:
    name: str
    description: str
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]


class A2AAgent:
    """Base class for A2A-enabled agents."""
    
    def __init__(
        self,
        agent_id: str,
        name: str,
        port: int = 8000,
        capabilities: List[AgentCapability] = None,
        description: str = None
    ):
        self.agent_id = agent_id
        self.name = name
        self.description = description or f"{name} - A2A Agent"
        self.port = port
        self.capabilities = capabilities or []
        # Create agent card for A2A SDK
        from a2a_sdk import AgentCard as SDKAgentCard
        sdk_card = SDKAgentCard(
            agent_id=self.agent_id,
            name=self.name,
            description=self.description,
            capabilities=[cap.name for cap in self.capabilities],
            endpoint=f"http://localhost:{self.port}"
        )
        self.client = A2AClient(sdk_card)
        self._handlers = {}
        
    async def start(self):
        """Start the A2A agent server."""
        # Create agent card
        agent_card = self._create_agent_card()
        
        # Register handlers
        for capability in self.capabilities:
            self.client.register_handler(
                capability.name,
                self._handlers.get(capability.name)
            )
        
        # Start server
        await self.client.start_server(port=self.port, agent_card=agent_card)
        logger.info(f"Started A2A agent", agent_id=self.agent_id, port=self.port)
    
    def _create_agent_card(self) -> Dict[str, Any]:
        """Create the agent discovery card."""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "capabilities": [
                {
                    "name": cap.name,
                    "description": cap.description,
                    "input_schema": cap.input_schema,
                    "output_schema": cap.output_schema
                }
                for cap in self.capabilities
            ],
            "interaction_modes": [mode.value for mode in InteractionMode],
            "data_types": ["text", "structured_json", "audio"],
            "endpoint": f"http://localhost:{self.port}"
        }
    
    def register_handler(self, capability: str, handler):
        """Register a handler for a capability."""
        self._handlers[capability] = handler
    
    async def send_task(
        self,
        target_agent: str,
        task_type: str,
        data: Dict[str, Any],
        mode: InteractionMode = InteractionMode.SYNC
    ) -> Any:
        """Send a task to another agent."""
        task = Task(
            type=task_type,
            data=data,
            metadata={"source": self.agent_id}
        )
        
        response = await self.client.send_task(
            agent_id=target_agent,
            task=task,
            mode=mode.value
        )
        
        logger.info(
            "Sent task to agent",
            source=self.agent_id,
            target=target_agent,
            task_type=task_type
        )
        
        return response
    
    async def discover_agents(self) -> List[Dict[str, Any]]:
        """Discover available agents in the network."""
        agents = await self.client.discover_agents()
        logger.info(f"Discovered {len(agents)} agents")
        return agents
    
    async def get_agent_card(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get the agent card for a specific agent."""
        try:
            card = await self.client.get_agent_card(agent_id)
            return card
        except Exception as e:
            logger.error(f"Failed to get agent card", agent_id=agent_id, error=str(e))
            return None


class A2AOrchestrator:
    """Orchestrates multi-agent workflows."""
    
    def __init__(self, base_agent: A2AAgent):
        self.base_agent = base_agent
        self.agent_registry = {}
        
    async def refresh_registry(self):
        """Refresh the registry of available agents."""
        agents = await self.base_agent.discover_agents()
        self.agent_registry = {agent['agent_id']: agent for agent in agents}
        logger.info(f"Registry refreshed with {len(self.agent_registry)} agents")
    
    async def execute_workflow(
        self,
        workflow: List[Dict[str, Any]]
    ) -> List[Any]:
        """Execute a multi-agent workflow."""
        results = []
        context = {}
        
        for step in workflow:
            agent_id = step['agent']
            task_type = step['task']
            
            # Prepare data with context from previous steps
            data = step.get('data', {})
            if step.get('use_context'):
                data['context'] = context
            
            # Send task
            result = await self.base_agent.send_task(
                target_agent=agent_id,
                task_type=task_type,
                data=data
            )
            
            results.append(result)
            
            # Update context for next steps
            if step.get('save_to_context'):
                context[step['save_to_context']] = result
        
        return results
    
    async def parallel_tasks(
        self,
        tasks: List[Dict[str, Any]]
    ) -> List[Any]:
        """Execute multiple tasks in parallel."""
        coroutines = [
            self.base_agent.send_task(
                target_agent=task['agent'],
                task_type=task['task'],
                data=task.get('data', {})
            )
            for task in tasks
        ]
        
        results = await asyncio.gather(*coroutines)
        return results