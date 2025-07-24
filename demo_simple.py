#!/usr/bin/env python3
"""Simple OMI Demo - Direct Connection Test"""

import asyncio
from integrations.omi_connector import OMIConnector
from config.settings import settings

async def test_omi_direct():
    """Test direct OMI connection and processing."""
    print("\n🎯 Simple OMI Connection Demo\n")
    
    # Connect to OMI
    print("1️⃣  Connecting to OMI MCP Server...")
    async with OMIConnector(
        api_url=settings.omi.api_url,
        api_key=settings.omi.api_key
    ) as omi:
        print(f"   ✅ Connected to {settings.omi.api_url}\n")
        
        # Test audio processing
        print("2️⃣  Processing sample conversation...")
        test_audio = b"test audio data"
        result = await omi.process_audio(
            test_audio,
            {
                "session_id": "demo-session",
                "simulated_transcript": """
                Sarah: Good morning everyone. Let's start with the project status update.
                John: We've completed the API integration. Found some edge cases that need fixing.
                Sarah: Great! John, please send me a summary by 5 PM today.
                Mike: I can help with the edge cases. I'll share my code after this meeting.
                """
            }
        )
        
        print(f"   ✅ Transcript processed\n")
        
        # Simulate what the multi-agent system would do
        print("3️⃣  Simulating Multi-Agent Analysis...\n")
        
        print("🧠 Context Analysis (simulated):")
        print("   - Topic: Project Status Update")
        print("   - Participants: Sarah (lead), John, Mike")
        print("   - Sentiment: Collaborative, positive\n")
        
        print("📋 Action Items (simulated):")
        print("   1. John: Send project summary to Sarah by 5 PM")
        print("   2. Mike: Share edge case handling code with John")
        print("   3. Team: Fix edge cases in API integration\n")
        
        print("✨ Demo Complete!\n")
        print("Note: In the full multi-agent system, these analyses would be")
        print("performed by specialized AI agents working together through A2A protocol.\n")

if __name__ == "__main__":
    asyncio.run(test_omi_direct())