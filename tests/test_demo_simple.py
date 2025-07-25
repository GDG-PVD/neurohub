"""Tests for the simplified demo."""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestDemoSimple:
    """Test the demo_simple.py functionality."""
    
    @pytest.mark.asyncio
    async def test_mock_context_analysis(self):
        """Test the context analysis simulation."""
        from demo_simple import mock_context_analysis
        
        transcript = "Let's discuss the Q4 roadmap"
        result = mock_context_analysis(transcript)
        
        assert "Topic" in result
        assert "Participants" in result
        assert "Sentiment" in result
        assert "roadmap" in result["Topic"].lower()
    
    @pytest.mark.asyncio
    async def test_mock_action_extraction(self):
        """Test the action extraction simulation."""
        from demo_simple import mock_action_extraction
        
        transcript = "John will send the report by Friday"
        result = mock_action_extraction(transcript)
        
        assert isinstance(result, list)
        assert len(result) > 0
        assert "John" in result[0]
        assert "report" in result[0]
    
    @pytest.mark.asyncio
    async def test_connection_with_mock_client(self):
        """Test the demo with a mocked MCP client."""
        with patch('demo_simple.MCPClient') as mock_client_class:
            # Create mock client instance
            mock_client = AsyncMock()
            mock_client_class.return_value.__aenter__.return_value = mock_client
            
            # Mock the process_transcript method
            mock_client.process_transcript = AsyncMock(return_value={
                "status": "success",
                "transcript": "Test conversation"
            })
            
            # Import and run the main function
            from demo_simple import main
            
            # Run main (it should complete without errors)
            try:
                await main()
            except SystemExit:
                # Expected - demo calls sys.exit()
                pass
            
            # Verify client was called
            assert mock_client.process_transcript.called


class TestIntegrations:
    """Test integration components."""
    
    def test_omi_client_initialization(self):
        """Test OMI client can be initialized."""
        from integrations.omi_connector import OMIClient
        
        client = OMIClient(
            api_url="http://localhost:8000",
            api_key="test_key"
        )
        
        assert client.api_url == "http://localhost:8000"
        assert client.api_key == "test_key"
    
    def test_a2a_client_initialization(self):
        """Test A2A client can be initialized."""
        from core.a2a_client import A2AClient
        
        client = A2AClient(
            agent_id="test_agent",
            name="Test Agent"
        )
        
        assert client.agent_id == "test_agent"
        assert client.name == "Test Agent"


class TestAgents:
    """Test agent implementations."""
    
    def test_context_agent_creation(self):
        """Test context analysis agent can be created."""
        from agents.context_analysis.agent import ContextAnalysisAgent
        
        agent = ContextAnalysisAgent()
        assert agent.agent_id == "context-analysis"
        assert agent.name == "Context Analysis Agent"
    
    def test_action_agent_creation(self):
        """Test action planning agent can be created."""
        from agents.action_planning.agent import ActionPlanningAgent
        
        agent = ActionPlanningAgent()
        assert agent.agent_id == "action-planning"
        assert agent.name == "Action Planning Agent"


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])