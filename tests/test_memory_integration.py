"""Integration tests for memory features."""

import pytest
from unittest.mock import MagicMock, patch
import json


class TestMemoryIntegration:
    """Test memory integration endpoints."""
    
    def test_memory_sync_endpoint_exists(self):
        """Test that memory sync endpoint is defined."""
        from workshop_server_enhanced import app
        
        # Check that the endpoint exists
        routes = [route.path for route in app.routes]
        assert "/memory/sync" in routes
    
    def test_memory_search_endpoint_exists(self):
        """Test that memory search endpoint is defined."""
        from workshop_server_enhanced import app
        
        # Check that the endpoint exists
        routes = [route.path for route in app.routes]
        assert "/memory/search" in routes
    
    def test_memory_analysis_endpoint_exists(self):
        """Test that memory analysis endpoint is defined."""
        from workshop_server_enhanced import app
        
        # Check that the endpoint exists
        routes = [route.path for route in app.routes]
        assert any("/memory/analysis" in route.path for route in app.routes)
    
    def test_health_endpoint_includes_memory_status(self):
        """Test that health endpoint reports memory features."""
        from workshop_server_enhanced import app
        from fastapi.testclient import TestClient
        
        client = TestClient(app)
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert "memory_bridge" in data
        assert "features" in data
    
    def test_team_registration_includes_memory_flag(self):
        """Test that team registration includes memory features flag."""
        from workshop_server_enhanced import app
        from fastapi.testclient import TestClient
        
        client = TestClient(app)
        
        # Register a team
        team_data = {
            "team_name": "Test Team Memory",
            "project_description": "Testing memory features",
            "omi_api_key": "test_key_123"
        }
        
        response = client.post("/register", json=team_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "memory_features_enabled" in data
    
    def test_demo_with_memory_context(self):
        """Test demo endpoint with memory context option."""
        from workshop_server_enhanced import app
        from fastapi.testclient import TestClient
        
        client = TestClient(app)
        
        # First register a team
        team_data = {
            "team_name": "Test Team Demo",
            "project_description": "Testing demo with memory",
            "omi_api_key": "test_key_456"
        }
        
        reg_response = client.post("/register", json=team_data)
        team_id = reg_response.json()["id"]
        
        # Run demo with memory context
        demo_data = {
            "team_id": team_id,
            "transcript": "Alice: Let's discuss the AI project. Bob: Yes, we need to plan the implementation.",
            "use_memory_context": True
        }
        
        response = client.post("/demo", json=demo_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "memory_context" in data
        assert isinstance(data["memory_context"], list)
    
    def test_stats_include_memory_metrics(self):
        """Test that stats endpoint includes memory metrics."""
        from workshop_server_enhanced import app
        from fastapi.testclient import TestClient
        
        client = TestClient(app)
        response = client.get("/stats")
        
        assert response.status_code == 200
        data = response.json()
        assert "total_memories_synced" in data
        assert "memory_features_enabled" in data