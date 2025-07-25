"""
Neuro-Focused Agent Demo (Simple version without rich)
For environments where rich is not available
"""

import asyncio
from typing import Dict, List, Optional

# Simulated agent responses for educational purposes
class CogniWatchAgent:
    """Cognitive Pattern Analysis Agent (Semantic Layer)"""
    
    async def analyze(self, transcript: str) -> Dict:
        """Analyze speech patterns for cognitive markers"""
        await asyncio.sleep(1)  # Simulate processing
        
        word_count = len(transcript.split())
        pause_count = transcript.count("...") + transcript.count("um") + transcript.count("uh")
        
        return {
            "speech_fluency": {
                "score": 0.85 if pause_count < 3 else 0.65,
                "pauses_detected": pause_count,
                "insight": "Speech patterns appear typical" if pause_count < 3 else "Increased hesitation detected"
            },
            "vocabulary_diversity": {
                "unique_words": len(set(transcript.lower().split())),
                "complexity_score": 0.75,
                "insight": "Vocabulary usage within normal range"
            },
            "topic_coherence": {
                "score": 0.90,
                "insight": "Conversation maintains logical flow"
            }
        }

class SocialPulseAgent:
    """Social Dynamics Monitoring Agent (Semantic Layer)"""
    
    async def analyze(self, transcript: str) -> Dict:
        """Analyze social and emotional patterns"""
        await asyncio.sleep(0.8)
        
        positive_words = ["happy", "good", "great", "wonderful", "excited", "grateful"]
        negative_words = ["sad", "worried", "tired", "stressed", "anxious"]
        
        words = transcript.lower().split()
        positive_count = sum(1 for word in words if word in positive_words)
        negative_count = sum(1 for word in words if word in negative_words)
        
        return {
            "emotional_tone": {
                "valence": "positive" if positive_count > negative_count else "neutral",
                "insight": "Emotional state appears balanced"
            },
            "social_engagement": {
                "interaction_quality": "good",
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
        
        if cognitive_data["speech_fluency"]["score"] < 0.70:
            actions.append({
                "action": "Schedule cognitive assessment",
                "priority": "medium",
                "timeline": "Within 2 weeks"
            })
        
        actions.append({
            "action": "Continue daily brain exercises",
            "priority": "ongoing",
            "timeline": "Daily"
        })
        
        return {"recommended_actions": actions}

class BrainHealthAdvisor:
    """Personalized Insights Agent (Dynamic Layer)"""
    
    async def generate_insights(self, all_data: Dict) -> Dict:
        """Generate personalized brain health recommendations"""
        await asyncio.sleep(0.7)
        
        recommendations = [
            "Cognitive Fitness: Try word puzzles or learning a new language",
            "Social Wellness: Schedule regular calls with friends",
            "Physical Activity: 20-minute walks, 3 times per week"
        ]
        
        return {
            "recommendations": recommendations,
            "strengths": ["Strong vocabulary", "Good social connections"],
            "areas_to_watch": ["Maintain current activity levels"]
        }

async def run_neuro_demo(transcript: str):
    """Run the multi-agent neuro analysis demo"""
    
    print("\n🧠 NeuroHub Multi-Agent Analysis Demo\n")
    print("Analyzing conversation with specialized neuro agents...\n")
    
    # Initialize agents
    cogni_watch = CogniWatchAgent()
    social_pulse = SocialPulseAgent()
    neuro_nav = NeuroNavigatorAgent()
    brain_advisor = BrainHealthAdvisor()
    
    # Run analyses
    print("⏳ Running Semantic Layer Analysis...")
    cognitive_results = await cogni_watch.analyze(transcript)
    social_results = await social_pulse.analyze(transcript)
    
    print("⏳ Running Kinetic Layer Coordination...")
    coordination_results = await neuro_nav.coordinate(cognitive_results, social_results)
    
    print("⏳ Running Dynamic Layer Insights...")
    all_results = {
        "cognitive": cognitive_results,
        "social": social_results,
        "coordination": coordination_results
    }
    insights = await brain_advisor.generate_insights(all_results)
    
    # Display Results
    print("\n✅ Analysis Complete!\n")
    
    # Cognitive Analysis
    print("🧠 Cognitive Analysis (CogniWatch)")
    print("-" * 50)
    print(f"Speech Fluency Score: {cognitive_results['speech_fluency']['score']:.2f}")
    print(f"  → {cognitive_results['speech_fluency']['insight']}")
    print(f"Vocabulary Diversity: {cognitive_results['vocabulary_diversity']['complexity_score']:.2f}")
    print(f"  → {cognitive_results['vocabulary_diversity']['insight']}")
    print(f"Topic Coherence: {cognitive_results['topic_coherence']['score']:.2f}")
    print(f"  → {cognitive_results['topic_coherence']['insight']}")
    
    # Social Analysis
    print("\n💬 Social Dynamics (SocialPulse)")
    print("-" * 50)
    print(f"Emotional Tone: {social_results['emotional_tone']['valence']}")
    print(f"Social Engagement: {social_results['social_engagement']['interaction_quality']}")
    print(f"Support Network: {social_results['social_engagement']['support_network_strength']:.2f}")
    print(f"  → {social_results['emotional_tone']['insight']}")
    
    # Care Actions
    print("\n📋 Care Coordination (NeuroNavigator)")
    print("-" * 50)
    for action in coordination_results["recommended_actions"]:
        print(f"• {action['action']}")
        print(f"  Priority: {action['priority']} | Timeline: {action['timeline']}")
    
    # Personalized Insights
    print("\n🎯 Brain Health Advisor")
    print("-" * 50)
    print("Personalized Recommendations:")
    for rec in insights["recommendations"]:
        print(f"• {rec}")
    print(f"\nStrengths: {', '.join(insights['strengths'])}")
    print(f"Areas to Monitor: {', '.join(insights['areas_to_watch'])}")
    
    # Educational Summary
    print("\n🎓 Educational Takeaways:")
    print("-" * 50)
    print("• Semantic agents extracted meaning from conversation")
    print("• Kinetic agents coordinated actionable next steps")
    print("• Dynamic agents provided personalized recommendations")
    print("• All agents work together to support brain health\n")

def main():
    """Run the demo with a sample conversation"""
    
    # Sample conversation
    sample_transcript = """
    I've been doing pretty well lately. Been keeping busy with my gardening 
    and... um... what was I saying? Oh yes, the garden. The tomatoes are 
    coming in nicely. I talk to my neighbor Susan about it sometimes, she's 
    very helpful. Though I do feel a bit tired in the afternoons. Maybe I 
    should... uh... exercise more? My daughter keeps telling me that. She 
    calls every week which is wonderful. I'm grateful for my family.
    """
    
    print("Sample OMI Conversation:")
    print("-" * 70)
    print(sample_transcript)
    print("-" * 70)
    
    # Run the analysis
    asyncio.run(run_neuro_demo(sample_transcript))
    
    # Workshop discussion
    print("🤔 Workshop Discussion Questions:")
    print("-" * 50)
    print("1. How could these agents help with early detection?")
    print("2. What privacy considerations are important?")
    print("3. How might families use this information?")
    print("4. What other neuro-focused agents could we add?")

if __name__ == "__main__":
    main()