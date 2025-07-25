"""
Tests for workshop agent framework
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch

from core.a2a_wrappers import A2ATask, A2AAgent, A2AOrchestrator
from agents.templates.agent_builder import CustomAgent, MCPProvider


class TestA2AWrappers:
    """Test the A2A wrapper classes"""
    
    def test_task_creation(self):
        """Test creating A2A tasks"""
        task = A2ATask.create("test_type", {"key": "value"})
        
        assert task.id is not None
        assert task.type == "test_type"
        assert task.data == {"key": "value"}
    
    def test_task_with_id(self):
        """Test creating task with explicit ID"""
        task = A2ATask(id="test-123", type="analyze", data={})
        
        assert task.id == "test-123"
        assert task.type == "analyze"


class TestCustomAgent:
    """Test the CustomAgent template"""
    
    @pytest.fixture
    def mock_mcp(self):
        """Mock MCP provider"""
        mcp = Mock(spec=MCPProvider)
        mcp.complete = AsyncMock(return_value="Test response")
        mcp.analyze = AsyncMock(return_value={
            "analysis_type": "test",
            "result": "Test analysis",
            "confidence": 0.9
        })
        return mcp
    
    @pytest.fixture
    def agent(self, mock_mcp):
        """Create test agent with mocked MCP"""
        agent = CustomAgent(
            name="test-agent",
            description="Test agent",
            capabilities=["analyze", "process"],
            mcp_provider="openai"
        )
        agent.mcp = mock_mcp
        return agent
    
    @pytest.mark.asyncio
    async def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = CustomAgent(
            name="workshop-agent",
            description="Workshop test agent",
            capabilities=["test", "demo"]
        )
        
        assert agent.name == "workshop-agent"
        assert agent.description == "Workshop test agent"
        assert "test" in agent.capabilities
        assert agent.state["processed_count"] == 0
    
    @pytest.mark.asyncio
    async def test_process_analyze_task(self, agent, mock_mcp):
        """Test processing an analyze task"""
        task = A2ATask.create("analyze", {
            "text": "Test text",
            "analysis_type": "sentiment"
        })
        
        result = await agent.process_task(task)
        
        assert result["status"] == "success"
        assert result["agent"] == "test-agent"
        assert "analysis" in result
        mock_mcp.analyze.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_process_query_task(self, agent, mock_mcp):
        """Test processing a query task"""
        task = A2ATask.create("query", {
            "query": "What is AI?",
            "context": "Educational workshop"
        })
        
        result = await agent.process_task(task)
        
        assert result["status"] == "success"
        assert result["query"] == "What is AI?"
        assert result["answer"] == "Test response"
        mock_mcp.complete.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_unknown_task_type(self, agent):
        """Test handling unknown task type"""
        task = A2ATask.create("unknown_type", {})
        
        result = await agent.process_task(task)
        
        assert result["status"] == "error"
        assert "Unknown task type" in result["error"]
        assert "supported_types" in result
    
    @pytest.mark.asyncio
    async def test_task_error_handling(self, agent, mock_mcp):
        """Test error handling in task processing"""
        mock_mcp.analyze.side_effect = Exception("Test error")
        
        task = A2ATask.create("analyze", {"text": "Test"})
        result = await agent.process_task(task)
        
        assert result["status"] == "error"
        assert "Test error" in result["error"]
        assert result["agent"] == "test-agent"
    
    @pytest.mark.asyncio
    async def test_state_tracking(self, agent):
        """Test agent state tracking"""
        initial_count = agent.state["processed_count"]
        
        task = A2ATask.create("analyze", {"text": "Test"})
        await agent.process_task(task)
        
        assert agent.state["processed_count"] == initial_count + 1
        assert agent.state["last_activity"] is not None
        assert len(agent.state["context_history"]) > 0


class TestOrchestrator:
    """Test the A2A Orchestrator"""
    
    @pytest.fixture
    def orchestrator(self):
        """Create test orchestrator"""
        return A2AOrchestrator()
    
    @pytest.fixture
    def mock_agent(self):
        """Create mock agent"""
        agent = Mock(spec=A2AAgent)
        agent.name = "test-agent"
        agent.process_task = AsyncMock(return_value={
            "status": "success",
            "result": "Test result"
        })
        return agent
    
    @pytest.mark.asyncio
    async def test_register_agent(self, orchestrator, mock_agent):
        """Test registering agents"""
        orchestrator.register_agent(mock_agent)
        
        assert "test-agent" in orchestrator.agents
        assert orchestrator.agents["test-agent"] == mock_agent
    
    @pytest.mark.asyncio
    async def test_execute_workflow(self, orchestrator, mock_agent):
        """Test executing a workflow"""
        orchestrator.register_agent(mock_agent)
        
        workflow = [
            {
                "agent": "test-agent",
                "task": "process",
                "data": {"input": "test"},
                "save_to_context": "step1"
            }
        ]
        
        results = await orchestrator.execute_workflow(workflow)
        
        assert "test-agent" in results
        assert results["test-agent"]["status"] == "success"
        mock_agent.process_task.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_workflow_context_passing(self, orchestrator):
        """Test context passing between workflow steps"""
        # Create two mock agents
        agent1 = Mock(spec=A2AAgent)
        agent1.name = "agent1"
        agent1.process_task = AsyncMock(return_value={
            "status": "success",
            "data": "from_agent1"
        })
        
        agent2 = Mock(spec=A2AAgent)
        agent2.name = "agent2"
        agent2.process_task = AsyncMock(return_value={
            "status": "success",
            "processed": "data"
        })
        
        orchestrator.register_agent(agent1)
        orchestrator.register_agent(agent2)
        
        workflow = [
            {
                "agent": "agent1",
                "task": "process",
                "data": {},
                "save_to_context": "result1"
            },
            {
                "agent": "agent2",
                "task": "analyze",
                "data": {"needs_context": True}
            }
        ]
        
        results = await orchestrator.execute_workflow(workflow)
        
        # Check that agent2 received context from agent1
        call_args = agent2.process_task.call_args[0][0]
        assert "context" in call_args.data
        assert "result1" in call_args.data["context"]


class TestWorkshopIntegration:
    """Integration tests for workshop scenarios"""
    
    @pytest.mark.asyncio
    async def test_research_agent_workflow(self):
        """Test research agent workflow"""
        from agents.examples.research_agent import ScientificResearchAgent
        
        agent = ScientificResearchAgent()
        
        task = A2ATask.create("analyze_conversation", {
            "transcript": "I wonder how machine learning works"
        })
        
        result = await agent.process_task(task)
        
        assert result["status"] == "success"
        assert "questions_found" in result
        assert result["questions_found"] >= 1
    
    @pytest.mark.asyncio
    async def test_collaboration_agent_workflow(self):
        """Test collaboration agent workflow"""
        from agents.examples.collaboration_agent import TeamCollaborationAgent
        
        agent = TeamCollaborationAgent()
        
        task = A2ATask.create("analyze_meeting", {
            "transcript": "John will handle the API integration by tomorrow",
            "meeting_type": "standup"
        })
        
        result = await agent.process_task(task)
        
        assert result["status"] == "success"
        assert "action_items" in result
        assert len(result["action_items"]) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])