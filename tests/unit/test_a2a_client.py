"""Unit tests for A2A client functionality."""

import pytest
from unittest.mock import Mock, AsyncMock, patch

from core.a2a_client import (
    A2AAgent,
    AgentCapability,
    InteractionMode,
    A2AOrchestrator,
)


class TestA2AAgent:
    """Tests for the A2AAgent base class."""
    
    @pytest.fixture
    def agent_capability(self):
        """Create a test capability."""
        return AgentCapability(
            name="test_capability",
            description="A test capability",
            input_schema={"type": "object"},
            output_schema={"type": "object"}
        )
    
    @pytest.fixture
    def test_agent(self, agent_capability):
        """Create a test agent."""
        return A2AAgent(
            agent_id="test-agent",
            name="Test Agent",
            port=8000,
            capabilities=[agent_capability]
        )
    
    def test_agent_initialization(self, test_agent, agent_capability):
        """Test agent is properly initialized."""
        assert test_agent.agent_id == "test-agent"
        assert test_agent.name == "Test Agent"
        assert test_agent.port == 8000
        assert len(test_agent.capabilities) == 1
        assert test_agent.capabilities[0] == agent_capability
    
    def test_create_agent_card(self, test_agent):
        """Test agent card creation."""
        card = test_agent._create_agent_card()
        
        assert card["agent_id"] == "test-agent"
        assert card["name"] == "Test Agent"
        assert len(card["capabilities"]) == 1
        assert card["interaction_modes"] == ["sync", "stream", "async"]
        assert card["data_types"] == ["text", "structured_json", "audio"]
        assert card["endpoint"] == "http://localhost:8000"
    
    def test_register_handler(self, test_agent):
        """Test handler registration."""
        mock_handler = Mock()
        test_agent.register_handler("test_capability", mock_handler)
        
        assert "test_capability" in test_agent._handlers
        assert test_agent._handlers["test_capability"] == mock_handler
    
    @pytest.mark.asyncio
    async def test_send_task(self, test_agent):
        """Test sending a task to another agent."""
        # Mock the client's send_task method
        with patch.object(test_agent.client, 'send_task', new_callable=AsyncMock) as mock_send:
            mock_send.return_value = {"result": "success"}
            
            response = await test_agent.send_task(
                target_agent="other-agent",
                task_type="process",
                data={"input": "test"},
                mode=InteractionMode.SYNC
            )
            
            assert response == {"result": "success"}
            mock_send.assert_called_once()


class TestA2AOrchestrator:
    """Tests for the A2AOrchestrator class."""
    
    @pytest.fixture
    def base_agent(self):
        """Create a base agent for orchestrator."""
        return A2AAgent(
            agent_id="orchestrator",
            name="Orchestrator",
            port=8001
        )
    
    @pytest.fixture
    def orchestrator(self, base_agent):
        """Create an orchestrator."""
        return A2AOrchestrator(base_agent)
    
    @pytest.mark.asyncio
    async def test_refresh_registry(self, orchestrator):
        """Test agent registry refresh."""
        # Mock discover_agents
        mock_agents = [
            {"agent_id": "agent1", "name": "Agent 1"},
            {"agent_id": "agent2", "name": "Agent 2"},
        ]
        
        with patch.object(
            orchestrator.base_agent,
            'discover_agents',
            new_callable=AsyncMock
        ) as mock_discover:
            mock_discover.return_value = mock_agents
            
            await orchestrator.refresh_registry()
            
            assert len(orchestrator.agent_registry) == 2
            assert "agent1" in orchestrator.agent_registry
            assert "agent2" in orchestrator.agent_registry
    
    @pytest.mark.asyncio
    async def test_execute_workflow(self, orchestrator):
        """Test workflow execution."""
        workflow = [
            {
                "agent": "agent1",
                "task": "task1",
                "data": {"input": "test1"},
            },
            {
                "agent": "agent2",
                "task": "task2",
                "data": {"input": "test2"},
                "use_context": True,
                "save_to_context": "result2"
            },
        ]
        
        # Mock send_task
        with patch.object(
            orchestrator.base_agent,
            'send_task',
            new_callable=AsyncMock
        ) as mock_send:
            mock_send.side_effect = [
                {"result": "result1"},
                {"result": "result2"},
            ]
            
            results = await orchestrator.execute_workflow(workflow)
            
            assert len(results) == 2
            assert results[0] == {"result": "result1"}
            assert results[1] == {"result": "result2"}
            assert mock_send.call_count == 2
    
    @pytest.mark.asyncio
    async def test_parallel_tasks(self, orchestrator):
        """Test parallel task execution."""
        tasks = [
            {"agent": "agent1", "task": "task1", "data": {}},
            {"agent": "agent2", "task": "task2", "data": {}},
            {"agent": "agent3", "task": "task3", "data": {}},
        ]
        
        # Mock send_task
        with patch.object(
            orchestrator.base_agent,
            'send_task',
            new_callable=AsyncMock
        ) as mock_send:
            mock_send.side_effect = [
                {"result": "r1"},
                {"result": "r2"},
                {"result": "r3"},
            ]
            
            results = await orchestrator.parallel_tasks(tasks)
            
            assert len(results) == 3
            assert mock_send.call_count == 3