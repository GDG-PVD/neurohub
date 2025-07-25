"""
Simple A2A wrappers for workshop agents
These wrappers provide the interface expected by our example agents
"""

from dataclasses import dataclass
from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod
import asyncio
import uuid


@dataclass
class A2ATask:
    """Simple task structure for agents"""
    id: str
    type: str
    data: Dict[str, Any]
    
    @classmethod
    def create(cls, task_type: str, data: Dict[str, Any]) -> 'A2ATask':
        """Create a new task with auto-generated ID"""
        return cls(
            id=str(uuid.uuid4()),
            type=task_type,
            data=data
        )


class A2AAgent(ABC):
    """Base class for workshop agents"""
    
    def __init__(self, name: str, capabilities: List[str] = None):
        self.name = name
        self.capabilities = capabilities or []
        self.running = False
        
    @abstractmethod
    async def process_task(self, task: A2ATask) -> Dict[str, Any]:
        """Process a task and return results"""
        pass
    
    async def run(self):
        """Run the agent (for standalone mode)"""
        self.running = True
        print(f"Agent {self.name} is running...")
        try:
            while self.running:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print(f"\nAgent {self.name} shutting down...")
            self.running = False


class A2AOrchestrator:
    """Simple orchestrator for multi-agent workflows"""
    
    def __init__(self):
        self.agents: Dict[str, A2AAgent] = {}
        
    def register_agent(self, agent: A2AAgent):
        """Register an agent with the orchestrator"""
        self.agents[agent.name] = agent
        
    async def execute_workflow(self, workflow: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Execute a workflow across multiple agents"""
        results = {}
        context = {}
        
        for step in workflow:
            agent_name = step.get("agent")
            task_type = step.get("task")
            task_data = step.get("data", {})
            
            # Include context from previous steps
            task_data["context"] = context
            
            if agent_name in self.agents:
                task = A2ATask.create(task_type, task_data)
                result = await self.agents[agent_name].process_task(task)
                
                # Store result
                results[agent_name] = result
                
                # Update context if specified
                if step.get("save_to_context"):
                    context[step["save_to_context"]] = result
        
        return results


# Re-export the original A2A client components if needed
try:
    from .a2a_client import A2AAgent as OriginalA2AAgent
    from .a2a_client import AgentCapability, InteractionMode
except ImportError:
    # Original imports not available, use our simple versions
    pass