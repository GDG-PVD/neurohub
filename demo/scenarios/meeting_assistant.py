"""Meeting Assistant Demo Scenario

Demonstrates multi-agent collaboration for meeting analysis.
"""

import asyncio
import json
from datetime import datetime

import aiohttp
import websockets


class MeetingAssistantDemo:
    """Demo scenario for meeting assistant functionality."""
    
    def __init__(self, gateway_url: str = "http://localhost:8001"):
        self.gateway_url = gateway_url
        self.ws_url = gateway_url.replace("http", "ws") + "/ws"
    
    async def run_demo(self):
        """Run the meeting assistant demo."""
        print("\n🎯 OMI Multi-Agent Meeting Assistant Demo\n")
        print("Connecting to OMI Gateway...")
        
        # Sample meeting transcript
        meeting_transcript = """
        Sarah: Good morning everyone. Let's start with the project status update.
        
        John: Sure. We've completed the API integration and it's now in testing. 
        We found a few edge cases that need to be addressed before the Friday deadline.
        
        Sarah: What kind of edge cases are we talking about?
        
        John: Mainly around error handling when the external service is down. 
        We need to implement a retry mechanism with exponential backoff.
        
        Mike: I can help with that. I've implemented something similar in the payment service.
        Let me share the code with you after this meeting.
        
        Sarah: Great! Mike, can you work with John to get this resolved by Thursday?
        Also, John, please send me a summary of the test results by end of day.
        
        John: Will do. I'll have the summary ready by 5 PM.
        
        Sarah: Perfect. Next, let's discuss the upcoming client presentation.
        We need to prepare slides showing our Q4 achievements. 
        Mike, can you gather the metrics from all teams?
        
        Mike: Yes, I'll compile everything and have it ready by Wednesday.
        
        Sarah: Excellent. Let's schedule a review meeting for Thursday at 2 PM.
        I'll send out the calendar invite. Any questions?
        
        John: No questions from me.
        
        Mike: All clear.
        
        Sarah: Great! Let's get to work. Thanks everyone.
        """
        
        try:
            # Connect to WebSocket
            async with websockets.connect(self.ws_url) as websocket:
                print("✅ Connected to OMI Gateway\n")
                
                # Send meeting transcript
                message = {
                    "type": "transcript",
                    "transcript": meeting_transcript,
                    "metadata": {
                        "user_id": "demo_user",
                        "session_id": "meeting_" + datetime.now().strftime("%Y%m%d_%H%M%S"),
                        "meeting_type": "project_status",
                        "participants": ["Sarah", "John", "Mike"]
                    }
                }
                
                await websocket.send(json.dumps(message))
                print("📤 Sent meeting transcript to multi-agent system\n")
                print("⏳ Processing through agents...\n")
                
                # Receive results
                response = await websocket.recv()
                result = json.loads(response)
                
                # Display results
                self.display_results(result)
                
                # Listen for any follow-up messages
                print("\n👂 Listening for agent updates...\n")
                
                # Set a timeout for demo purposes
                try:
                    while True:
                        update = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                        update_data = json.loads(update)
                        
                        if update_data.get("type") == "conversation_processed":
                            print("📨 Update from agents:")
                            print(f"   - Actions completed: {len(update_data['data']['actions'])}")
                            
                except asyncio.TimeoutError:
                    print("\n✅ Demo completed!")
                    
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("\nMake sure all agents are running:")
            print("  docker-compose up")
    
    def display_results(self, result: dict):
        """Display the multi-agent analysis results."""
        print("=" * 60)
        print("📊 MULTI-AGENT ANALYSIS RESULTS")
        print("=" * 60)
        
        # Context Analysis
        if "analysis" in result:
            analysis = result["analysis"]
            print("\n🧠 Context Analysis Agent:")
            print(f"\n📝 Summary: {analysis.get('summary', 'N/A')}")
            
            print("\n🏷️  Topics:")
            for topic in analysis.get("topics", []):
                print(f"   - {topic}")
            
            print(f"\n😊 Sentiment: {analysis.get('sentiment', 'N/A')}")
            
            print("\n👥 Entities:")
            for entity in analysis.get("entities", []):
                print(f"   - {entity}")
        
        # Action Planning
        if "actions" in result:
            print("\n\n📋 Action Planning Agent:")
            print(f"\nExtracted {len(result['actions'])} action items:")
            
            for i, action in enumerate(result["actions"], 1):
                print(f"\n{i}. {action.get('type', 'Unknown')}:")
                print(f"   Description: {action.get('description', 'N/A')}")
                
                if "data" in action:
                    print("   Details:")
                    for key, value in action["data"].items():
                        print(f"     - {key}: {value}")
        
        # Summary
        if "summary" in result:
            print("\n\n📌 Overall Summary:")
            print(f"{result['summary']}")
        
        print("\n" + "=" * 60)


async def main():
    """Run the demo."""
    demo = MeetingAssistantDemo()
    await demo.run_demo()


if __name__ == "__main__":
    print("\n🚀 Starting OMI Multi-Agent Demo...\n")
    asyncio.run(main())