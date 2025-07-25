"""Tests for Memory Bridge integration."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime
import uuid

from integrations.memory_bridge import MemoryBridge, MemoryEnhancedAgent
from integrations.omi_connector import OMIConnector


@pytest.fixture
def mock_omi_connector():
    """Mock OMI connector."""
    connector = MagicMock(spec=OMIConnector)
    connector.api_url = "https://test.omi.me"
    return connector


@pytest.fixture
def mock_mem0_client():
    """Mock Mem0 client."""
    with patch('integrations.memory_bridge.MemoryClient') as mock_client:
        client_instance = MagicMock()
        mock_client.return_value = client_instance
        yield client_instance


@pytest.fixture
def memory_bridge(mock_omi_connector, mock_mem0_client):
    """Create memory bridge with mocks."""
    with patch('integrations.memory_bridge.MemoryClient', return_value=mock_mem0_client):
        bridge = MemoryBridge(mock_omi_connector, "test_api_key")
        return bridge


class TestMemoryBridge:
    """Test Memory Bridge functionality."""
    
    @pytest.mark.asyncio
    async def test_sync_omi_memory_to_mem0(self, memory_bridge, mock_mem0_client):
        """Test syncing a single OMI memory to Mem0."""
        # Arrange
        team_id = "test_team_123"
        omi_memory = {
            "id": "memory_123",
            "transcript": "Test conversation about AI",
            "created_at": "2024-01-25T10:00:00Z",
            "duration": 300,
            "participants": ["Alice", "Bob"],
            "emotions": ["excited", "focused"],
            "topics": ["AI", "project planning"],
            "action_items": ["Schedule meeting"],
            "location": {"lat": 42.3601, "lng": -71.0589}
        }
        
        mock_mem0_client.add.return_value = {"status": "success"}
        
        # Act
        result = await memory_bridge.sync_omi_memory_to_mem0(team_id, omi_memory)
        
        # Assert
        assert result == "memory_123"
        mock_mem0_client.add.assert_called_once()
        call_args = mock_mem0_client.add.call_args
        
        # Verify memory content
        messages = call_args[0][0]
        assert len(messages) == 1
        assert "Test conversation about AI" in messages[0]["content"]
        
        # Verify metadata
        kwargs = call_args[1]
        assert kwargs["user_id"] == f"neurohub_team_{team_id}"
        assert kwargs["metadata"]["team_id"] == team_id
        assert kwargs["metadata"]["memory_id"] == "memory_123"
        assert kwargs["metadata"]["participants"] == ["Alice", "Bob"]
    
    @pytest.mark.asyncio
    async def test_sync_team_memories(self, memory_bridge, mock_omi_connector):
        """Test syncing all team memories."""
        # Arrange
        team_id = "test_team_123"
        omi_api_key = "omi_test_key"
        
        # Mock OMI memories
        mock_memories = [
            {"id": "mem1", "transcript": "Meeting 1"},
            {"id": "mem2", "transcript": "Meeting 2"}
        ]
        
        # Create a mock team OMI connector
        mock_team_omi = MagicMock()
        mock_team_omi.get_user_memories = AsyncMock(return_value=mock_memories)
        
        with patch('integrations.memory_bridge.OMIConnector', return_value=mock_team_omi):
            # Act
            result = await memory_bridge.sync_team_memories(team_id, omi_api_key)
        
        # Assert
        assert result["status"] == "success"
        assert result["synced"] == 2
        assert result["failed"] == 0
        assert result["total"] == 2
    
    @pytest.mark.asyncio
    async def test_search_unified_memories(self, memory_bridge, mock_mem0_client):
        """Test searching memories."""
        # Arrange
        team_id = "test_team_123"
        query = "AI project"
        
        mock_mem0_client.search.return_value = [
            {
                "memory": "Discussion about AI project timeline",
                "metadata": {"team_id": team_id},
                "score": 0.95
            }
        ]
        
        # Act
        results = await memory_bridge.search_unified_memories(
            team_id=team_id,
            query=query,
            include_mem0=True,
            include_omi=False
        )
        
        # Assert
        assert len(results) == 1
        assert results[0]["source"] == "mem0"
        assert results[0]["score"] == 0.95
        assert "AI project timeline" in results[0]["content"]
    
    @pytest.mark.asyncio
    async def test_analyze_team_memories(self, memory_bridge, mock_mem0_client):
        """Test analyzing team memories."""
        # Arrange
        team_id = "test_team_123"
        
        mock_memories = [
            {
                "memory": "Meeting 1",
                "metadata": {
                    "duration": 600,
                    "topics": ["AI", "planning"],
                    "participants": ["Alice", "Bob"],
                    "emotions": ["excited"],
                    "action_items": ["Research AI tools"]
                }
            },
            {
                "memory": "Meeting 2",
                "metadata": {
                    "duration": 300,
                    "topics": ["AI", "implementation"],
                    "participants": ["Alice", "Charlie"],
                    "emotions": ["focused"],
                    "action_items": ["Build prototype"]
                }
            }
        ]
        
        mock_mem0_client.search.return_value = mock_memories
        
        # Act
        result = await memory_bridge.analyze_team_memories(team_id)
        
        # Assert
        assert result["total_memories"] == 2
        assert result["total_duration_minutes"] == 15.0  # (600 + 300) / 60
        assert set(result["unique_participants"]) == {"Alice", "Bob", "Charlie"}
        assert result["action_items_count"] == 2
        assert len(result["top_topics"]) > 0
        assert result["top_topics"][0][0] == "AI"  # Most frequent topic
        assert result["top_topics"][0][1] == 2  # Frequency
    
    @pytest.mark.asyncio
    async def test_create_memory_from_conversation(self, memory_bridge, mock_mem0_client):
        """Test creating memory from conversation analysis."""
        # Arrange
        team_id = "test_team_123"
        conversation = {
            "summary": "Discussed AI implementation strategy",
            "analysis": {
                "key_points": ["Use Python", "Deploy on cloud"],
                "sentiment": "positive"
            },
            "actions": [
                {"type": "task", "description": "Set up repository"}
            ]
        }
        
        mock_mem0_client.add.return_value = {"status": "success"}
        
        # Act
        result = await memory_bridge.create_memory_from_conversation(team_id, conversation)
        
        # Assert
        assert result is not None  # Returns timestamp
        mock_mem0_client.add.assert_called_once()
        
        call_args = mock_mem0_client.add.call_args
        messages = call_args[0][0]
        assert "Discussed AI implementation strategy" in messages[0]["content"]
        
        kwargs = call_args[1]
        assert kwargs["user_id"] == f"neurohub_team_{team_id}"
        assert kwargs["metadata"]["actions"] == conversation["actions"]


class TestMemoryEnhancedAgent:
    """Test Memory Enhanced Agent functionality."""
    
    @pytest.mark.asyncio
    async def test_get_relevant_context(self, memory_bridge):
        """Test getting relevant context for agent."""
        # Arrange
        agent = MemoryEnhancedAgent(memory_bridge)
        team_id = "test_team_123"
        query = "previous meeting decisions"
        
        # Mock the memory bridge method
        memory_bridge.get_contextual_memories = AsyncMock(return_value=[
            {
                "content": "Decided to use Python for backend",
                "timestamp": "2024-01-25T10:00:00Z",
                "relevance_score": 0.9,
                "context": {"meeting": "Tech planning"}
            }
        ])
        
        # Act
        context = await agent.get_relevant_context(team_id, query)
        
        # Assert
        assert len(context) == 1
        assert context[0]["relevance_score"] == 0.9
        assert "Python for backend" in context[0]["content"]
    
    @pytest.mark.asyncio
    async def test_store_insight(self, memory_bridge):
        """Test storing agent insights."""
        # Arrange
        agent = MemoryEnhancedAgent(memory_bridge)
        team_id = "test_team_123"
        insight = {
            "summary": "Team prefers agile methodology",
            "analysis": {"confidence": 0.85},
            "actions": []
        }
        
        # Mock the memory bridge method
        memory_bridge.create_memory_from_conversation = AsyncMock(return_value="timestamp_123")
        
        # Act
        result = await agent.store_insight(team_id, insight)
        
        # Assert
        assert result is True
        memory_bridge.create_memory_from_conversation.assert_called_once_with(
            team_id,
            {
                "summary": insight["summary"],
                "analysis": insight["analysis"],
                "actions": insight["actions"]
            }
        )