"""
Team Collaboration Agent - Functional example for hackathon teams
Shows integration with project management tools and multi-agent orchestration
"""

import asyncio
import json
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass, field

from core.a2a_wrappers import A2AAgent, A2ATask, A2AOrchestrator


@dataclass
class ActionItem:
    """Structured action item from meeting"""
    action: str
    assignee: Optional[str]
    deadline: Optional[datetime]
    priority: str = "medium"
    status: str = "pending"
    context: str = ""


@dataclass
class MeetingInsights:
    """Insights extracted from team meeting"""
    summary: str
    decisions: List[str]
    action_items: List[ActionItem]
    blockers: List[str]
    sentiment: str
    key_topics: List[str]


class TeamCollaborationAgent(A2AAgent):
    """
    Agent that enhances team meetings by:
    1. Extracting action items and decisions
    2. Identifying blockers and risks
    3. Tracking progress over time
    4. Integrating with project management tools
    """
    
    def __init__(self):
        super().__init__(
            name="team-collaboration-agent",
            capabilities=[
                "extract_actions",
                "track_decisions",
                "identify_blockers",
                "analyze_sentiment",
                "generate_summaries"
            ]
        )
        
        # Track meeting history
        self.meeting_history = []
        self.team_members = set()
        
    async def process_task(self, task: A2ATask) -> dict:
        """Process collaboration tasks"""
        
        if task.type == "analyze_meeting":
            return await self.analyze_team_meeting(task.data)
        elif task.type == "track_progress":
            return await self.track_action_progress(task.data)
        elif task.type == "generate_standup":
            return await self.generate_standup_summary(task.data)
        else:
            return {"error": f"Unknown task type: {task.type}"}
    
    async def analyze_team_meeting(self, data: dict) -> dict:
        """Analyze team meeting conversation"""
        
        transcript = data.get("transcript", "")
        meeting_type = data.get("meeting_type", "general")
        
        # Extract insights
        insights = await self.extract_meeting_insights(transcript, meeting_type)
        
        # Store in history
        self.meeting_history.append({
            "timestamp": datetime.now().isoformat(),
            "type": meeting_type,
            "insights": insights
        })
        
        # Format response
        return {
            "status": "success",
            "meeting_type": meeting_type,
            "summary": insights.summary,
            "decisions": insights.decisions,
            "action_items": [self._action_to_dict(a) for a in insights.action_items],
            "blockers": insights.blockers,
            "sentiment": insights.sentiment,
            "key_topics": insights.key_topics,
            "integrations": await self.create_integrations(insights)
        }
    
    async def extract_meeting_insights(self, transcript: str, 
                                     meeting_type: str) -> MeetingInsights:
        """Extract structured insights from meeting transcript"""
        
        # Extract different components
        action_items = self.extract_action_items(transcript)
        decisions = self.extract_decisions(transcript)
        blockers = self.extract_blockers(transcript)
        sentiment = self.analyze_team_sentiment(transcript)
        topics = self.extract_key_topics(transcript)
        summary = self.generate_summary(transcript, meeting_type)
        
        return MeetingInsights(
            summary=summary,
            decisions=decisions,
            action_items=action_items,
            blockers=blockers,
            sentiment=sentiment,
            key_topics=topics
        )
    
    def extract_action_items(self, transcript: str) -> List[ActionItem]:
        """Extract action items from conversation"""
        
        action_items = []
        action_phrases = [
            "will do", "i'll handle", "action item", "todo", "need to",
            "should", "must", "going to", "plan to", "assigned to"
        ]
        
        sentences = transcript.split('.')
        for sentence in sentences:
            sentence_lower = sentence.lower()
            
            for phrase in action_phrases:
                if phrase in sentence_lower:
                    # Extract action
                    action = sentence.strip()
                    
                    # Try to identify assignee
                    assignee = None
                    team_indicators = ["i'll", "i will", "me", "my"]
                    for indicator in team_indicators:
                        if indicator in sentence_lower:
                            assignee = "self"  # In real app: extract actual name
                            break
                    
                    # Look for deadline
                    deadline = None
                    time_indicators = ["by tomorrow", "by end of week", "by friday"]
                    for indicator in time_indicators:
                        if indicator in sentence_lower:
                            # Simple deadline extraction
                            if "tomorrow" in indicator:
                                deadline = datetime.now() + timedelta(days=1)
                            elif "end of week" in indicator:
                                deadline = datetime.now() + timedelta(days=5)
                            break
                    
                    # Determine priority
                    priority = "medium"
                    if "urgent" in sentence_lower or "asap" in sentence_lower:
                        priority = "high"
                    elif "eventually" in sentence_lower or "sometime" in sentence_lower:
                        priority = "low"
                    
                    action_items.append(ActionItem(
                        action=action,
                        assignee=assignee,
                        deadline=deadline,
                        priority=priority,
                        context=transcript[:100]
                    ))
                    break
        
        return action_items
    
    def extract_decisions(self, transcript: str) -> List[str]:
        """Extract decisions made during meeting"""
        
        decisions = []
        decision_phrases = [
            "we decided", "decision is", "agreed to", "consensus is",
            "we'll go with", "final decision", "approved"
        ]
        
        sentences = transcript.split('.')
        for sentence in sentences:
            for phrase in decision_phrases:
                if phrase in sentence.lower():
                    decisions.append(sentence.strip())
                    break
        
        return decisions
    
    def extract_blockers(self, transcript: str) -> List[str]:
        """Identify blockers and challenges"""
        
        blockers = []
        blocker_phrases = [
            "blocked by", "waiting on", "can't proceed", "stuck on",
            "problem with", "issue with", "challenge is", "preventing"
        ]
        
        sentences = transcript.split('.')
        for sentence in sentences:
            for phrase in blocker_phrases:
                if phrase in sentence.lower():
                    blockers.append(sentence.strip())
                    break
        
        return blockers
    
    def analyze_team_sentiment(self, transcript: str) -> str:
        """Analyze overall team sentiment"""
        
        positive_indicators = [
            "excited", "great", "awesome", "perfect", "excellent",
            "happy", "confident", "optimistic"
        ]
        negative_indicators = [
            "worried", "concerned", "frustrated", "difficult",
            "challenging", "unclear", "confused"
        ]
        
        transcript_lower = transcript.lower()
        positive_count = sum(1 for word in positive_indicators 
                           if word in transcript_lower)
        negative_count = sum(1 for word in negative_indicators 
                           if word in transcript_lower)
        
        if positive_count > negative_count * 2:
            return "positive"
        elif negative_count > positive_count * 2:
            return "concerned"
        else:
            return "neutral"
    
    def extract_key_topics(self, transcript: str) -> List[str]:
        """Extract main topics discussed"""
        
        # Simple topic extraction - in production use NLP
        topics = []
        
        # Look for project-related terms
        project_terms = [
            "frontend", "backend", "api", "database", "ui", "ux",
            "deployment", "testing", "feature", "bug", "release"
        ]
        
        transcript_lower = transcript.lower()
        for term in project_terms:
            if term in transcript_lower:
                topics.append(term)
        
        return topics[:5]  # Top 5 topics
    
    def generate_summary(self, transcript: str, meeting_type: str) -> str:
        """Generate concise meeting summary"""
        
        word_count = len(transcript.split())
        
        if meeting_type == "standup":
            return f"Daily standup with {word_count} words discussed. " \
                   f"Team shared updates on current tasks and blockers."
        elif meeting_type == "planning":
            return f"Planning meeting covered upcoming sprint tasks. " \
                   f"{word_count} words exchanged on priorities and assignments."
        else:
            return f"Team meeting with {word_count} words discussed. " \
                   f"Covered project updates and next steps."
    
    async def create_integrations(self, insights: MeetingInsights) -> dict:
        """Create integration payloads for external tools"""
        
        integrations = {}
        
        # GitHub Issues
        if insights.action_items:
            integrations["github"] = {
                "create_issues": [
                    {
                        "title": item.action[:50],
                        "body": f"{item.action}\n\nContext: {item.context}",
                        "labels": [item.priority],
                        "assignees": [item.assignee] if item.assignee else []
                    }
                    for item in insights.action_items
                ]
            }
        
        # Slack Summary
        integrations["slack"] = {
            "message": f"*Meeting Summary*\n{insights.summary}\n\n" +
                      f"*Decisions:* {len(insights.decisions)}\n" +
                      f"*Action Items:* {len(insights.action_items)}\n" +
                      f"*Blockers:* {len(insights.blockers)}\n" +
                      f"*Team Sentiment:* {insights.sentiment}"
        }
        
        # Trello/Jira Cards
        integrations["project_management"] = {
            "cards": [
                {
                    "name": item.action,
                    "desc": item.context,
                    "due": item.deadline.isoformat() if item.deadline else None,
                    "labels": [item.priority]
                }
                for item in insights.action_items
            ]
        }
        
        return integrations
    
    async def track_action_progress(self, data: dict) -> dict:
        """Track progress on previous action items"""
        
        # Get historical action items
        all_actions = []
        for meeting in self.meeting_history:
            all_actions.extend(meeting["insights"].action_items)
        
        # Group by status
        pending = [a for a in all_actions if a.status == "pending"]
        completed = [a for a in all_actions if a.status == "completed"]
        overdue = [a for a in all_actions 
                  if a.deadline and a.deadline < datetime.now() 
                  and a.status == "pending"]
        
        return {
            "status": "success",
            "summary": {
                "total_actions": len(all_actions),
                "pending": len(pending),
                "completed": len(completed),
                "overdue": len(overdue)
            },
            "overdue_items": [self._action_to_dict(a) for a in overdue],
            "completion_rate": len(completed) / len(all_actions) if all_actions else 0
        }
    
    async def generate_standup_summary(self, data: dict) -> dict:
        """Generate standup summary from meeting history"""
        
        lookback_days = data.get("days", 1)
        cutoff = datetime.now() - timedelta(days=lookback_days)
        
        recent_meetings = [
            m for m in self.meeting_history
            if datetime.fromisoformat(m["timestamp"]) > cutoff
        ]
        
        # Aggregate insights
        all_actions = []
        all_blockers = []
        
        for meeting in recent_meetings:
            insights = meeting["insights"]
            all_actions.extend(insights.action_items)
            all_blockers.extend(insights.blockers)
        
        return {
            "status": "success",
            "period": f"Last {lookback_days} days",
            "meetings_count": len(recent_meetings),
            "total_actions": len(all_actions),
            "active_blockers": all_blockers,
            "team_velocity": self._calculate_velocity(all_actions)
        }
    
    def _action_to_dict(self, action: ActionItem) -> dict:
        """Convert ActionItem to dictionary"""
        return {
            "action": action.action,
            "assignee": action.assignee,
            "deadline": action.deadline.isoformat() if action.deadline else None,
            "priority": action.priority,
            "status": action.status
        }
    
    def _calculate_velocity(self, actions: List[ActionItem]) -> str:
        """Calculate team velocity based on action completion"""
        if not actions:
            return "No data"
        
        completed = len([a for a in actions if a.status == "completed"])
        rate = completed / len(actions)
        
        if rate > 0.8:
            return "High"
        elif rate > 0.5:
            return "Medium"
        else:
            return "Low"


class CollaborationOrchestrator(A2AOrchestrator):
    """
    Orchestrates multiple agents for comprehensive meeting analysis
    Demonstrates multi-agent collaboration
    """
    
    def __init__(self):
        super().__init__()
        self.collab_agent = TeamCollaborationAgent()
        # Could add more agents here:
        # self.sentiment_agent = SentimentAnalysisAgent()
        # self.technical_agent = TechnicalDiscussionAgent()
    
    async def analyze_comprehensive_meeting(self, transcript: str) -> dict:
        """Run comprehensive meeting analysis using multiple agents"""
        
        # Step 1: Basic collaboration analysis
        collab_task = A2ATask(
            id="meeting-1",
            type="analyze_meeting",
            data={"transcript": transcript, "meeting_type": "planning"}
        )
        collab_result = await self.collab_agent.process_task(collab_task)
        
        # Step 2: Could add more agent analyses here
        # sentiment_result = await self.sentiment_agent.analyze(transcript)
        # technical_result = await self.technical_agent.analyze(transcript)
        
        # Step 3: Aggregate results
        return {
            "collaboration_insights": collab_result,
            # "sentiment_analysis": sentiment_result,
            # "technical_discussion": technical_result,
            "recommendations": self.generate_recommendations(collab_result)
        }
    
    def generate_recommendations(self, collab_result: dict) -> List[str]:
        """Generate recommendations based on analysis"""
        
        recommendations = []
        
        # Check for concerning patterns
        if collab_result.get("sentiment") == "concerned":
            recommendations.append("Schedule team morale check-in")
        
        if len(collab_result.get("blockers", [])) > 3:
            recommendations.append("Prioritize blocker resolution session")
        
        if len(collab_result.get("action_items", [])) > 10:
            recommendations.append("Consider breaking down large tasks")
        
        # Always recommend follow-up
        recommendations.append("Schedule follow-up on action items")
        
        return recommendations


# Demo function for workshop
async def demo_collaboration_agent():
    """Demonstrate the collaboration agent"""
    
    agent = TeamCollaborationAgent()
    
    # Sample team meeting transcript
    sample_meeting = """
    Alright team, let's start our sprint planning. First, Sarah, can you 
    give us an update on the API integration?
    
    Sarah: Sure! I've completed the authentication module, but I'm blocked 
    by the missing API documentation from the vendor. I'll handle reaching 
    out to them today.
    
    Mike: Great. I've been working on the frontend and it's going well. 
    I should have the dashboard ready by end of week. One concern though - 
    we need to decide on the charting library. I propose we go with Chart.js.
    
    Team: Sounds good, let's go with Chart.js. Decision made.
    
    John: I'll take on setting up the testing framework. This is urgent 
    because we need it before we can merge any new features. I'll get it 
    done by tomorrow.
    
    Sarah: Also, we agreed to do daily standups at 10 AM starting tomorrow.
    Everyone good with that?
    
    Team: Yes, approved!
    
    Mike: One more thing - I'm worried about the deployment timeline. 
    We might need an extra week for proper testing.
    """
    
    print("🤝 Team Collaboration Agent Demo\n")
    print("Analyzing team meeting...\n")
    
    # Process meeting
    task = A2ATask(
        id="demo-meeting",
        type="analyze_meeting",
        data={
            "transcript": sample_meeting,
            "meeting_type": "planning"
        }
    )
    
    result = await agent.process_task(task)
    
    # Display results
    print("📊 Meeting Analysis Results:\n")
    print(f"Summary: {result['summary']}\n")
    
    print("✅ Decisions Made:")
    for decision in result['decisions']:
        print(f"  - {decision}")
    print()
    
    print("📋 Action Items:")
    for item in result['action_items']:
        print(f"  - {item['action']}")
        print(f"    Assignee: {item['assignee'] or 'Unassigned'}")
        print(f"    Priority: {item['priority']}")
        print(f"    Deadline: {item['deadline'] or 'No deadline'}")
    print()
    
    print("🚧 Blockers:")
    for blocker in result['blockers']:
        print(f"  - {blocker}")
    print()
    
    print(f"😊 Team Sentiment: {result['sentiment']}")
    print(f"🏷️ Key Topics: {', '.join(result['key_topics'])}")
    
    print("\n🔌 Integration Payloads Generated:")
    for platform, payload in result['integrations'].items():
        print(f"  - {platform}: Ready to sync")


if __name__ == "__main__":
    # Run the demo
    asyncio.run(demo_collaboration_agent())