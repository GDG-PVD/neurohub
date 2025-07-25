"""
Neuro-Focused Agent Demo for NeuroHub Workshop
Demonstrates how specialized agents can extend OMI capabilities for brain health
"""

import asyncio
from datetime import datetime
from typing import Dict, List, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

# Simulated agent responses for educational purposes
class CogniWatchAgent:
    """Cognitive Pattern Analysis Agent (Semantic Layer)"""
    
    async def analyze(self, transcript: str) -> Dict:
        """Analyze speech patterns for cognitive markers"""
        await asyncio.sleep(1)  # Simulate processing
        
        # In production: Use NLP libraries for real analysis
        word_count = len(transcript.split())
        pause_count = transcript.count("...") + transcript.count("um") + transcript.count("uh")
        
        return {
            "speech_fluency": {
                "score": 0.85 if pause_count < 3 else 0.65,
                "pauses_detected": pause_count,
                "words_per_minute": 150 if word_count > 50 else 120,
                "insight": "Speech patterns appear typical" if pause_count < 3 else "Increased hesitation detected"
            },
            "vocabulary_diversity": {
                "unique_words": len(set(transcript.lower().split())),
                "complexity_score": 0.75,
                "trend": "stable",
                "insight": "Vocabulary usage within normal range"
            },
            "topic_coherence": {
                "score": 0.90,
                "topic_shifts": 1,
                "insight": "Conversation maintains logical flow"
            }
        }

class SocialPulseAgent:
    """Social Dynamics Monitoring Agent (Semantic Layer)"""
    
    async def analyze(self, transcript: str) -> Dict:
        """Analyze social and emotional patterns"""
        await asyncio.sleep(0.8)
        
        # Simulated sentiment analysis
        positive_words = ["happy", "good", "great", "wonderful", "excited"]
        negative_words = ["sad", "worried", "tired", "stressed", "anxious"]
        
        words = transcript.lower().split()
        positive_count = sum(1 for word in words if word in positive_words)
        negative_count = sum(1 for word in words if word in negative_words)
        
        return {
            "emotional_tone": {
                "valence": "positive" if positive_count > negative_count else "neutral",
                "energy_level": "moderate",
                "stability": 0.80,
                "insight": "Emotional state appears balanced"
            },
            "social_engagement": {
                "interaction_quality": "good",
                "mentions_of_others": 3,
                "support_network_strength": 0.75,
                "insight": "Healthy social connections indicated"
            }
        }

class NeuroNavigatorAgent:
    """Care Coordination Agent (Kinetic Layer)"""
    
    async def coordinate(self, cognitive_data: Dict, social_data: Dict) -> Dict:
        """Generate care coordination actions"""
        await asyncio.sleep(0.5)
        
        actions = []
        
        # Generate actions based on analysis
        if cognitive_data["speech_fluency"]["score"] < 0.70:
            actions.append({
                "type": "appointment",
                "priority": "medium",
                "action": "Schedule cognitive assessment",
                "timeline": "Within 2 weeks"
            })
        
        if social_data["social_engagement"]["support_network_strength"] < 0.50:
            actions.append({
                "type": "social",
                "priority": "low",
                "action": "Connect with support group",
                "timeline": "This month"
            })
        
        # Always include wellness action
        actions.append({
            "type": "wellness",
            "priority": "ongoing",
            "action": "Continue daily brain exercises",
            "timeline": "Daily"
        })
        
        return {
            "recommended_actions": actions,
            "care_summary": "Overall health status: Good",
            "next_check_in": "1 week"
        }

class BrainHealthAdvisor:
    """Personalized Insights Agent (Dynamic Layer)"""
    
    async def generate_insights(self, all_data: Dict) -> Dict:
        """Generate personalized brain health recommendations"""
        await asyncio.sleep(0.7)
        
        recommendations = [
            {
                "category": "Cognitive Fitness",
                "recommendation": "Try word puzzles or learning a new language",
                "rationale": "Maintains vocabulary diversity and cognitive flexibility",
                "priority": "high"
            },
            {
                "category": "Social Wellness",
                "recommendation": "Schedule regular calls with friends",
                "rationale": "Social engagement supports cognitive health",
                "priority": "medium"
            },
            {
                "category": "Physical Activity",
                "recommendation": "20-minute walks, 3 times per week",
                "rationale": "Exercise boosts brain health and mood",
                "priority": "high"
            }
        ]
        
        return {
            "personalized_plan": recommendations,
            "risk_assessment": "Low risk profile",
            "strengths": ["Strong vocabulary", "Good social connections"],
            "areas_to_watch": ["Maintain current activity levels"]
        }

async def run_neuro_demo(transcript: str):
    """Run the multi-agent neuro analysis demo"""
    
    layout = Layout()
    
    console.print("\n[bold cyan]🧠 NeuroHub Multi-Agent Analysis Demo[/bold cyan]\n")
    console.print("[yellow]Analyzing conversation with specialized neuro agents...[/yellow]\n")
    
    # Initialize agents
    cogni_watch = CogniWatchAgent()
    social_pulse = SocialPulseAgent()
    neuro_nav = NeuroNavigatorAgent()
    brain_advisor = BrainHealthAdvisor()
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        
        # Semantic Layer Analysis
        semantic_task = progress.add_task("[cyan]Semantic Layer Analysis...", total=2)
        
        cognitive_task = asyncio.create_task(cogni_watch.analyze(transcript))
        social_task = asyncio.create_task(social_pulse.analyze(transcript))
        
        cognitive_results = await cognitive_task
        progress.update(semantic_task, advance=1)
        
        social_results = await social_task
        progress.update(semantic_task, advance=1)
        
        # Kinetic Layer Actions
        kinetic_task = progress.add_task("[blue]Kinetic Layer Coordination...", total=1)
        coordination_results = await neuro_nav.coordinate(cognitive_results, social_results)
        progress.update(kinetic_task, advance=1)
        
        # Dynamic Layer Insights
        dynamic_task = progress.add_task("[magenta]Dynamic Layer Insights...", total=1)
        all_results = {
            "cognitive": cognitive_results,
            "social": social_results,
            "coordination": coordination_results
        }
        insights = await brain_advisor.generate_insights(all_results)
        progress.update(dynamic_task, advance=1)
    
    # Display Results
    console.print("\n[bold green]✅ Analysis Complete![/bold green]\n")
    
    # Cognitive Analysis Panel
    cog_table = Table(title="🧠 Cognitive Analysis (CogniWatch)")
    cog_table.add_column("Metric", style="cyan")
    cog_table.add_column("Score", style="green")
    cog_table.add_column("Insight", style="yellow")
    
    cog_table.add_row(
        "Speech Fluency",
        f"{cognitive_results['speech_fluency']['score']:.2f}",
        cognitive_results['speech_fluency']['insight']
    )
    cog_table.add_row(
        "Vocabulary Diversity",
        f"{cognitive_results['vocabulary_diversity']['complexity_score']:.2f}",
        cognitive_results['vocabulary_diversity']['insight']
    )
    cog_table.add_row(
        "Topic Coherence",
        f"{cognitive_results['topic_coherence']['score']:.2f}",
        cognitive_results['topic_coherence']['insight']
    )
    
    console.print(cog_table)
    console.print()
    
    # Social Analysis Panel
    social_panel = Panel(
        f"[bold]Emotional Tone:[/bold] {social_results['emotional_tone']['valence']}\n"
        f"[bold]Social Engagement:[/bold] {social_results['social_engagement']['interaction_quality']}\n"
        f"[bold]Support Network:[/bold] {social_results['social_engagement']['support_network_strength']:.2f}\n"
        f"\n[italic]{social_results['emotional_tone']['insight']}[/italic]",
        title="💬 Social Dynamics (SocialPulse)",
        border_style="blue"
    )
    console.print(social_panel)
    console.print()
    
    # Care Actions
    if coordination_results["recommended_actions"]:
        action_table = Table(title="📋 Care Coordination (NeuroNavigator)")
        action_table.add_column("Action", style="cyan")
        action_table.add_column("Priority", style="yellow")
        action_table.add_column("Timeline", style="green")
        
        for action in coordination_results["recommended_actions"]:
            action_table.add_row(
                action["action"],
                action["priority"],
                action["timeline"]
            )
        
        console.print(action_table)
        console.print()
    
    # Personalized Insights
    insights_panel = Panel(
        "[bold]Personalized Brain Health Plan:[/bold]\n\n" +
        "\n".join([
            f"• [cyan]{rec['category']}:[/cyan] {rec['recommendation']}"
            for rec in insights["personalized_plan"]
        ]) +
        f"\n\n[bold green]Strengths:[/bold green] {', '.join(insights['strengths'])}" +
        f"\n[bold yellow]Monitor:[/bold yellow] {', '.join(insights['areas_to_watch'])}",
        title="🎯 Brain Health Advisor",
        border_style="magenta"
    )
    console.print(insights_panel)
    
    # Educational Summary
    console.print("\n[bold cyan]🎓 Educational Insights:[/bold cyan]")
    console.print("• [green]Semantic agents[/green] extracted meaning from conversation")
    console.print("• [blue]Kinetic agents[/blue] coordinated actionable next steps")
    console.print("• [magenta]Dynamic agents[/magenta] provided personalized recommendations")
    console.print("• [yellow]All agents work together[/yellow] to support brain health\n")

def main():
    """Run the demo with a sample conversation"""
    
    # Sample conversation that demonstrates various patterns
    sample_transcript = """
    I've been doing pretty well lately. Been keeping busy with my gardening 
    and... um... what was I saying? Oh yes, the garden. The tomatoes are 
    coming in nicely. I talk to my neighbor Susan about it sometimes, she's 
    very helpful. Though I do feel a bit tired in the afternoons. Maybe I 
    should... uh... exercise more? My daughter keeps telling me that. She 
    calls every week which is wonderful. I'm grateful for my family.
    """
    
    console.print("[bold]Sample OMI Conversation:[/bold]")
    console.print(Panel(sample_transcript, border_style="dim"))
    
    # Run the analysis
    asyncio.run(run_neuro_demo(sample_transcript))
    
    # Workshop discussion points
    console.print("\n[bold cyan]🤔 Workshop Discussion:[/bold cyan]")
    console.print("1. How could these agents help with early detection?")
    console.print("2. What privacy considerations are important?")
    console.print("3. How might families use this information?")
    console.print("4. What other neuro-focused agents could we add?")

if __name__ == "__main__":
    main()