"""Mem0 storage backend for workshop persistence."""

import os
import json
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
from mem0 import MemoryClient
import uuid


class Mem0Storage:
    """Mem0-based storage for workshop data."""
    
    def __init__(self, api_key: str):
        self.client = MemoryClient(api_key=api_key)
        self.workshop_user_id = "neurohub_workshop"
        
    def _serialize_team(self, team_data: Dict[str, Any]) -> str:
        """Serialize team data for storage."""
        return json.dumps(team_data)
    
    def _deserialize_team(self, memory_content: str) -> Dict[str, Any]:
        """Deserialize team data from storage."""
        try:
            return json.loads(memory_content)
        except json.JSONDecodeError:
            return None
    
    async def register_team(self, team_data: Dict[str, Any]) -> Dict[str, Any]:
        """Register a new team in Mem0."""
        team_id = str(uuid.uuid4())
        team_data["id"] = team_id
        team_data["registered_at"] = datetime.utcnow().isoformat()
        team_data["demos_run"] = 0
        
        # Store team as memory with metadata
        message = f"Team registration: {self._serialize_team(team_data)}"
        metadata = {
            "type": "team_registration",
            "team_id": team_id,
            "team_name": team_data["team_name"]
        }
        
        # Use sync method in async context
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            lambda: self.client.add(
                [{"role": "system", "content": message}],
                user_id=self.workshop_user_id,
                metadata=metadata
            )
        )
        
        return {
            "id": team_id,
            "team_name": team_data["team_name"],
            "project_description": team_data["project_description"],
            "registered_at": team_data["registered_at"]
        }
    
    async def get_teams(self) -> List[Dict[str, Any]]:
        """Get all registered teams."""
        # Search for all team registrations
        loop = asyncio.get_event_loop()
        memories = await loop.run_in_executor(
            None,
            lambda: self.client.search(
                "Team registration",
                user_id=self.workshop_user_id,
                limit=100
            )
        )
        
        teams = []
        # Handle both list and dict responses from Mem0
        memory_list = memories if isinstance(memories, list) else memories.get("results", [])
        for memory in memory_list:
            if memory.get("metadata", {}).get("type") == "team_registration":
                # Extract team data from memory content
                content = memory.get("memory", "")
                if "Team registration: " in content:
                    json_str = content.replace("Team registration: ", "")
                    team_data = self._deserialize_team(json_str)
                    if team_data:
                        # Don't expose API key
                        teams.append({
                            "id": team_data["id"],
                            "team_name": team_data["team_name"],
                            "project_description": team_data["project_description"],
                            "registered_at": team_data["registered_at"],
                            "demos_run": team_data.get("demos_run", 0)
                        })
        
        # Sort by registration time (newest first)
        teams.sort(key=lambda x: x["registered_at"], reverse=True)
        return teams
    
    async def get_team(self, team_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific team by ID."""
        loop = asyncio.get_event_loop()
        memories = await loop.run_in_executor(
            None,
            lambda: self.client.search(
                f"team_id: {team_id}",
                user_id=self.workshop_user_id,
                limit=1
            )
        )
        
        memory_list = memories if isinstance(memories, list) else memories.get("results", [])
        for memory in memory_list:
            if memory.get("metadata", {}).get("team_id") == team_id:
                content = memory.get("memory", "")
                if "Team registration: " in content:
                    json_str = content.replace("Team registration: ", "")
                    return self._deserialize_team(json_str)
        
        return None
    
    async def increment_demo_count(self, team_id: str):
        """Increment demo count for a team."""
        # Get current team data
        team_data = await self.get_team(team_id)
        if not team_data:
            raise ValueError("Team not found")
        
        # Update demo count
        team_data["demos_run"] = team_data.get("demos_run", 0) + 1
        
        # Store updated data
        message = f"Team update: {self._serialize_team(team_data)}"
        metadata = {
            "type": "team_update",
            "team_id": team_id,
            "team_name": team_data["team_name"]
        }
        
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            lambda: self.client.add(
                [{"role": "system", "content": message}],
                user_id=self.workshop_user_id,
                metadata=metadata
            )
        )
        
        # Also increment global demo counter
        await self._increment_global_demo_count()
    
    async def _increment_global_demo_count(self):
        """Increment global demo count."""
        # Store demo run event
        message = f"Demo run at {datetime.utcnow().isoformat()}"
        metadata = {
            "type": "demo_run",
            "timestamp": datetime.utcnow().isoformat()
        }
        
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            lambda: self.client.add(
                [{"role": "system", "content": message}],
                user_id=self.workshop_user_id,
                metadata=metadata
            )
        )
    
    async def get_stats(self) -> Dict[str, int]:
        """Get workshop statistics."""
        teams = await self.get_teams()
        
        # Count demo runs
        loop = asyncio.get_event_loop()
        demo_memories = await loop.run_in_executor(
            None,
            lambda: self.client.search(
                "Demo run",
                user_id=self.workshop_user_id,
                limit=1000
            )
        )
        
        demo_list = demo_memories if isinstance(demo_memories, list) else demo_memories.get("results", [])
        demos_count = sum(
            1 for memory in demo_list
            if memory.get("metadata", {}).get("type") == "demo_run"
        )
        
        # Count active teams
        active_teams = sum(1 for team in teams if team.get("demos_run", 0) > 0)
        
        return {
            "teams_registered": len(teams),
            "demos_run": demos_count,
            "active_teams": active_teams
        }
    
    async def check_team_exists(self, team_name: str) -> bool:
        """Check if a team name already exists."""
        teams = await self.get_teams()
        return any(
            team["team_name"].lower() == team_name.lower()
            for team in teams
        )