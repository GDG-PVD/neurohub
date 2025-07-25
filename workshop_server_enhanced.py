#!/usr/bin/env python3
"""Enhanced workshop server with OMI-Mem0 memory integration for NeuroHub."""

import os
import json
from datetime import datetime
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import uvicorn
import uuid
from contextlib import asynccontextmanager

# Import memory bridge and connectors
from integrations.memory_bridge import MemoryBridge, MemoryEnhancedAgent
from integrations.omi_connector import OMIConnector

# Initialize components
MEM0_API_KEY = os.environ.get("MEM0_API_KEY", "")
OMI_API_URL = os.environ.get("OMI_API_BASE_URL", "https://neurohub-workshop.fly.dev")
DEFAULT_OMI_KEY = os.environ.get("OMI_API_KEY", "neurohub_workshop_2024")

# Create default OMI connector
default_omi = OMIConnector(OMI_API_URL, DEFAULT_OMI_KEY)

# Initialize memory bridge
memory_bridge = MemoryBridge(default_omi, MEM0_API_KEY) if MEM0_API_KEY else None

# In-memory storage
teams_db = {}
demos_run = 0

app = FastAPI(
    title="NeuroHub Workshop Server - Memory Enhanced",
    description="Multi-agent AI workshop with OMI device memory integration"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ProcessRequest(BaseModel):
    transcript: str
    session_id: Optional[str] = "demo-session"
    metadata: Optional[Dict[str, Any]] = {}


class ProcessResponse(BaseModel):
    transcript: str
    analysis: Dict[str, Any]
    actions: list
    summary: str
    memory_context: Optional[List[Dict[str, Any]]] = []


class TeamRegistration(BaseModel):
    team_name: str
    project_description: str
    omi_api_key: str


class DemoRequest(BaseModel):
    transcript: str
    team_id: str
    use_memory_context: Optional[bool] = True


class MemorySyncRequest(BaseModel):
    team_id: str


class MemorySearchRequest(BaseModel):
    team_id: str
    query: str
    limit: Optional[int] = 10


class MemoryAnalysisResponse(BaseModel):
    team_id: str
    insights: Dict[str, Any]
    timestamp: str


# Memory-enhanced agent for demonstrations
class DemoAgent(MemoryEnhancedAgent):
    """Demo agent with memory capabilities."""
    
    async def process_with_memory(
        self,
        team_id: str,
        transcript: str
    ) -> ProcessResponse:
        """Process conversation with memory context."""
        # Get relevant memories
        memory_context = []
        if memory_bridge:
            memory_context = await self.get_relevant_context(team_id, transcript[:100])
        
        # Simulate multi-agent analysis with memory awareness
        words = transcript.lower().split()
        
        # Detect participants
        participants = set()
        for i, word in enumerate(words):
            if word.endswith(":"):
                participants.add(word[:-1].title())
        
        # Detect topics with memory enhancement
        topics = []
        topic_keywords = {
            "meeting": "Meeting Discussion",
            "project": "Project Planning",
            "demo": "Demo Preparation",
            "integration": "Technical Integration",
            "ai": "AI Development",
            "memory": "Memory Systems",
            "omi": "OMI Device Usage"
        }
        
        for keyword, topic in topic_keywords.items():
            if keyword in transcript.lower():
                topics.append(topic)
        
        # Extract actions with memory-aware suggestions
        actions = []
        if "send" in transcript.lower() or "email" in transcript.lower():
            actions.append({
                "type": "email",
                "description": "Send follow-up communication",
                "assignee": list(participants)[0] if participants else "Team member",
                "context": "Check previous emails in memory"
            })
        
        if "schedule" in transcript.lower() or "meeting" in transcript.lower():
            actions.append({
                "type": "calendar",
                "description": "Schedule meeting or follow-up",
                "deadline": "To be determined",
                "context": f"Found {len([m for m in memory_context if 'meeting' in m.get('content', '').lower()])} related meetings in memory"
            })
        
        # Generate analysis with memory insights
        analysis = {
            "context": {
                "topic": topics[0] if topics else "General Discussion",
                "participants": len(participants),
                "sentiment": "collaborative" if len(participants) > 1 else "individual",
                "memory_enhanced": len(memory_context) > 0
            },
            "key_points": [
                f"Discussion involved {len(participants)} participants",
                f"Main topic: {topics[0] if topics else 'General conversation'}",
                f"Identified {len(actions)} action items",
                f"Found {len(memory_context)} relevant memories for context"
            ],
            "memory_insights": [
                {
                    "relevance": mem.get("relevance_score", 0),
                    "context": mem.get("content", "")[:100] + "..."
                }
                for mem in memory_context[:3]
            ] if memory_context else []
        }
        
        # Generate summary
        summary = f"Analyzed conversation with {len(words)} words. "
        summary += f"Detected {len(participants)} participants discussing "
        summary += f"'{topics[0] if topics else 'various topics'}'. "
        summary += f"Found {len(actions)} action items requiring follow-up."
        if memory_context:
            summary += f" Enhanced with {len(memory_context)} relevant memories."
        
        # Store this conversation as a memory
        if memory_bridge:
            await memory_bridge.create_memory_from_conversation(
                team_id,
                {
                    "summary": summary,
                    "analysis": analysis,
                    "actions": actions
                }
            )
        
        return ProcessResponse(
            transcript=transcript,
            analysis=analysis,
            actions=actions,
            summary=summary,
            memory_context=[
                {
                    "content": mem.get("content", "")[:200],
                    "relevance": mem.get("relevance_score", 0)
                }
                for mem in memory_context[:3]
            ]
        )


# Initialize demo agent
demo_agent = DemoAgent(memory_bridge) if memory_bridge else None


@app.get("/")
async def root():
    # Serve the dashboard
    if os.path.exists("static/index_enhanced.html"):
        return FileResponse("static/index_enhanced.html")
    elif os.path.exists("static/index.html"):
        return FileResponse("static/index.html")
    return {"message": "NeuroHub Workshop Server - Memory Enhanced", "status": "running"}


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "memory_bridge": "enabled" if memory_bridge else "disabled",
        "features": {
            "memory_sync": bool(memory_bridge),
            "memory_search": bool(memory_bridge),
            "memory_analysis": bool(memory_bridge),
            "contextual_processing": bool(memory_bridge)
        }
    }


@app.post("/process", response_model=ProcessResponse)
async def process_conversation(request: ProcessRequest):
    """Process a conversation transcript (basic, no team context)."""
    # For non-team requests, use basic processing
    return await demo_agent.process_with_memory("anonymous", request.transcript) if demo_agent else ProcessResponse(
        transcript=request.transcript,
        analysis={"context": {"topic": "General", "participants": 1}},
        actions=[],
        summary="Basic processing without memory enhancement"
    )


@app.post("/register")
async def register_team(team: TeamRegistration):
    """Register a new team."""
    # Check if team name already exists
    for team_data in teams_db.values():
        if team_data["team_name"].lower() == team.team_name.lower():
            raise HTTPException(status_code=400, detail="Team name already exists")
    
    team_id = str(uuid.uuid4())
    team_data = {
        "id": team_id,
        "team_name": team.team_name,
        "project_description": team.project_description,
        "omi_api_key": team.omi_api_key,
        "registered_at": datetime.utcnow().isoformat(),
        "demos_run": 0,
        "memories_synced": 0,
        "memory_features_enabled": bool(memory_bridge)
    }
    
    teams_db[team_id] = team_data
    
    # Return team data without API key
    return {
        "id": team_id,
        "team_name": team.team_name,
        "project_description": team.project_description,
        "registered_at": team_data["registered_at"],
        "memory_features_enabled": team_data["memory_features_enabled"]
    }


@app.get("/teams")
async def get_teams():
    """Get all registered teams (without API keys)."""
    teams = []
    for team_data in teams_db.values():
        teams.append({
            "id": team_data["id"],
            "team_name": team_data["team_name"],
            "project_description": team_data["project_description"],
            "registered_at": team_data["registered_at"],
            "demos_run": team_data["demos_run"],
            "memories_synced": team_data.get("memories_synced", 0),
            "memory_features_enabled": team_data.get("memory_features_enabled", False)
        })
    
    # Sort by registration time (newest first)
    teams.sort(key=lambda x: x["registered_at"], reverse=True)
    return teams


@app.post("/demo")
async def run_demo(request: DemoRequest):
    """Run a demo analysis for a team with optional memory context."""
    global demos_run
    
    # Verify team exists
    if request.team_id not in teams_db:
        raise HTTPException(status_code=404, detail="Team not found")
    
    # Increment demo counters
    demos_run += 1
    teams_db[request.team_id]["demos_run"] += 1
    
    # Process with memory enhancement if available
    if demo_agent and request.use_memory_context:
        return await demo_agent.process_with_memory(request.team_id, request.transcript)
    else:
        # Fallback to basic processing
        return ProcessResponse(
            transcript=request.transcript,
            analysis={"context": {"topic": "General", "participants": 1}},
            actions=[],
            summary="Basic processing without memory enhancement"
        )


@app.post("/memory/sync")
async def sync_team_memories(
    request: MemorySyncRequest,
    background_tasks: BackgroundTasks
):
    """Sync a team's OMI memories to Mem0."""
    if not memory_bridge:
        raise HTTPException(status_code=503, detail="Memory features not available")
    
    # Verify team exists
    if request.team_id not in teams_db:
        raise HTTPException(status_code=404, detail="Team not found")
    
    team_data = teams_db[request.team_id]
    
    # Start sync in background
    async def sync_task():
        result = await memory_bridge.sync_team_memories(
            request.team_id,
            team_data["omi_api_key"]
        )
        teams_db[request.team_id]["memories_synced"] = result.get("synced", 0)
    
    background_tasks.add_task(sync_task)
    
    return {
        "status": "sync_started",
        "team_id": request.team_id,
        "message": "Memory synchronization started in background"
    }


@app.post("/memory/search")
async def search_memories(request: MemorySearchRequest):
    """Search a team's memories."""
    if not memory_bridge:
        raise HTTPException(status_code=503, detail="Memory features not available")
    
    # Verify team exists
    if request.team_id not in teams_db:
        raise HTTPException(status_code=404, detail="Team not found")
    
    results = await memory_bridge.search_unified_memories(
        team_id=request.team_id,
        query=request.query,
        limit=request.limit
    )
    
    return {
        "team_id": request.team_id,
        "query": request.query,
        "results": results,
        "count": len(results)
    }


@app.get("/memory/analysis/{team_id}")
async def analyze_team_memories(team_id: str) -> MemoryAnalysisResponse:
    """Analyze a team's memories to extract insights."""
    if not memory_bridge:
        raise HTTPException(status_code=503, detail="Memory features not available")
    
    # Verify team exists
    if team_id not in teams_db:
        raise HTTPException(status_code=404, detail="Team not found")
    
    insights = await memory_bridge.analyze_team_memories(team_id)
    
    return MemoryAnalysisResponse(
        team_id=team_id,
        insights=insights,
        timestamp=datetime.utcnow().isoformat()
    )


@app.get("/stats")
async def get_stats():
    """Get workshop statistics."""
    total_memories = 0
    if memory_bridge:
        for team_id in teams_db:
            team_memories = teams_db[team_id].get("memories_synced", 0)
            total_memories += team_memories
    
    return {
        "teams_registered": len(teams_db),
        "demos_run": demos_run,
        "active_teams": sum(1 for team in teams_db.values() if team["demos_run"] > 0),
        "total_memories_synced": total_memories,
        "memory_features_enabled": bool(memory_bridge)
    }


# Mount static files for any additional assets
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting NeuroHub Workshop Server - Memory Enhanced")
    print(f"Memory Bridge: {'Enabled' if memory_bridge else 'Disabled'}")
    uvicorn.run(app, host="0.0.0.0", port=port)