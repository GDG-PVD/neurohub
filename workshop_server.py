#!/usr/bin/env python3
"""Simple workshop server for NeuroHub demo."""

import os
import json
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import uvicorn
import uuid
from contextlib import asynccontextmanager

# Simple in-memory storage (works well for workshop)
teams_db = {}
demos_run = 0

app = FastAPI(title="NeuroHub Workshop Server")

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


class TeamRegistration(BaseModel):
    team_name: str
    project_description: str
    omi_api_key: str


class DemoRequest(BaseModel):
    transcript: str
    team_id: str




@app.get("/")
async def root():
    # Serve the dashboard
    if os.path.exists("static/index.html"):
        return FileResponse("static/index.html")
    return {"message": "NeuroHub Workshop Server", "status": "running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/process", response_model=ProcessResponse)
async def process_conversation(request: ProcessRequest):
    """Process a conversation transcript (simulated multi-agent response)."""
    
    # Simulate multi-agent analysis
    analysis = {
        "context": {
            "topic": "Meeting or Conversation",
            "participants": 2,
            "sentiment": "collaborative"
        },
        "key_points": [
            "Discussion detected",
            "Multiple participants engaged"
        ]
    }
    
    # Simulate action extraction
    actions = []
    if "send" in request.transcript.lower() or "email" in request.transcript.lower():
        actions.append({
            "type": "email",
            "description": "Send follow-up email",
            "assignee": "detected participant"
        })
    
    if "meeting" in request.transcript.lower() or "tomorrow" in request.transcript.lower():
        actions.append({
            "type": "calendar",
            "description": "Schedule meeting",
            "deadline": "tomorrow"
        })
    
    # Generate summary
    summary = f"Processed conversation with {len(request.transcript.split())} words. "
    summary += f"Found {len(actions)} action items."
    
    return ProcessResponse(
        transcript=request.transcript,
        analysis=analysis,
        actions=actions,
        summary=summary
    )


@app.post("/audio")
async def process_audio(audio_data: bytes = b"", metadata: Dict[str, Any] = {}):
    """Process audio data (mock endpoint for compatibility)."""
    return {
        "transcript": metadata.get("simulated_transcript", "Audio processing simulated"),
        "duration": 10.5,
        "language": "en"
    }


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
        "demos_run": 0
    }
    
    teams_db[team_id] = team_data
    
    # Return team data without API key
    return {
        "id": team_id,
        "team_name": team.team_name,
        "project_description": team.project_description,
        "registered_at": team_data["registered_at"]
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
            "demos_run": team_data["demos_run"]
        })
    
    # Sort by registration time (newest first)
    teams.sort(key=lambda x: x["registered_at"], reverse=True)
    return teams


@app.post("/demo")
async def run_demo(request: DemoRequest):
    """Run a demo analysis for a team."""
    global demos_run
    
    # Verify team exists
    if request.team_id not in teams_db:
        raise HTTPException(status_code=404, detail="Team not found")
    
    # Increment demo counters
    demos_run += 1
    teams_db[request.team_id]["demos_run"] += 1
    
    # Simulate multi-agent analysis
    words = request.transcript.lower().split()
    
    # Detect participants (simple heuristic: look for names followed by colons)
    participants = set()
    for i, word in enumerate(words):
        if word.endswith(":"):
            participants.add(word[:-1].title())
    
    # Detect topic (look for keywords)
    topics = []
    topic_keywords = {
        "meeting": "Meeting Discussion",
        "project": "Project Planning",
        "demo": "Demo Preparation",
        "integration": "Technical Integration",
        "ai": "AI Development",
        "review": "Progress Review"
    }
    
    for keyword, topic in topic_keywords.items():
        if keyword in request.transcript.lower():
            topics.append(topic)
    
    # Extract actions
    actions = []
    if "send" in request.transcript.lower() or "email" in request.transcript.lower():
        actions.append({
            "type": "email",
            "description": "Send follow-up communication",
            "assignee": list(participants)[0] if participants else "Team member"
        })
    
    if "schedule" in request.transcript.lower() or "meeting" in request.transcript.lower():
        actions.append({
            "type": "calendar",
            "description": "Schedule meeting or follow-up",
            "deadline": "To be determined"
        })
    
    if "documentation" in request.transcript.lower() or "document" in request.transcript.lower():
        actions.append({
            "type": "documentation",
            "description": "Update or create documentation",
            "assignee": "Team"
        })
    
    # Generate analysis
    analysis = {
        "context": {
            "topic": topics[0] if topics else "General Discussion",
            "participants": len(participants),
            "sentiment": "collaborative" if len(participants) > 1 else "individual"
        },
        "key_points": [
            f"Discussion involved {len(participants)} participants",
            f"Main topic: {topics[0] if topics else 'General conversation'}",
            f"Identified {len(actions)} action items"
        ]
    }
    
    # Generate summary
    summary = f"Analyzed conversation with {len(words)} words. "
    summary += f"Detected {len(participants)} participants discussing "
    summary += f"'{topics[0] if topics else 'various topics'}'. "
    summary += f"Found {len(actions)} action items requiring follow-up."
    
    return ProcessResponse(
        transcript=request.transcript,
        analysis=analysis,
        actions=actions,
        summary=summary
    )


@app.get("/stats")
async def get_stats():
    """Get workshop statistics."""
    return {
        "teams_registered": len(teams_db),
        "demos_run": demos_run,
        "active_teams": sum(1 for team in teams_db.values() if team["demos_run"] > 0)
    }


# Mount static files for any additional assets
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)