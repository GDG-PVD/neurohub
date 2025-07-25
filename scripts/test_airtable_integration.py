#!/usr/bin/env python3
"""
Test script for Airtable MCP integration

This script demonstrates how to use the Airtable connector
with the NeuroHub multi-agent system.
"""

import asyncio
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env.local
load_dotenv(Path(__file__).parent.parent / ".env.local")

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from integrations.airtable_connector import AirtableConnector, AirtableConfig
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


async def test_airtable_operations():
    """Test various Airtable operations"""
    
    print("🔌 Testing Airtable MCP Integration\n")
    
    # Initialize connector
    try:
        config = AirtableConfig.from_env()
        connector = AirtableConnector(config)
        print("✅ Airtable connector initialized\n")
    except ValueError as e:
        print(f"❌ Error: {e}")
        print("\nPlease set these environment variables:")
        print("  export AIRTABLE_API_KEY=your_api_key")
        print("  export AIRTABLE_BASE_ID=your_base_id")
        return
    
    # Test 1: Save a conversation
    print("📝 Test 1: Saving conversation...")
    conversation_data = {
        "timestamp": datetime.now().isoformat(),
        "summary": "Discussion about implementing new features for the mobile app",
        "participants": ["Alice", "Bob", "AI Assistant"],
        "topics": ["mobile development", "feature planning", "user experience"],
        "agent_analysis": {
            "context_agent": "Technical discussion about mobile implementation",
            "action_agent": "3 action items identified",
            "knowledge_agent": "Related to previous mobile discussions"
        }
    }
    
    conversation_id = await connector.save_conversation(conversation_data)
    print(f"✅ Conversation saved with ID: {conversation_id}\n")
    
    # Test 2: Save action items
    print("📋 Test 2: Saving action items...")
    actions = [
        {
            "action_item": "Create wireframes for new mobile feature",
            "deadline": (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d"),
            "assignee": "Alice"
        },
        {
            "action_item": "Research React Native vs Flutter for implementation",
            "deadline": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
            "assignee": "Bob"
        },
        {
            "action_item": "Schedule user testing session",
            "deadline": (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d"),
            "assignee": "Alice"
        }
    ]
    
    action_ids = await connector.save_action_items(conversation_id, actions)
    print(f"✅ Saved {len(action_ids)} action items: {action_ids}\n")
    
    # Test 3: Save knowledge entry
    print("💡 Test 3: Saving knowledge entry...")
    knowledge_data = {
        "topic": "Mobile Development Best Practices",
        "content": "Key insights from the discussion: 1) Consider cross-platform frameworks, 2) Focus on performance optimization, 3) Implement proper offline support",
        "source_conversation": conversation_id,
        "tags": ["mobile", "development", "best-practices"]
    }
    
    knowledge_id = await connector.save_knowledge(knowledge_data)
    print(f"✅ Knowledge entry saved with ID: {knowledge_id}\n")
    
    # Test 4: Retrieve recent conversations
    print("🔍 Test 4: Retrieving recent conversations...")
    recent_conversations = await connector.get_recent_conversations(limit=5)
    print(f"✅ Found {len(recent_conversations)} recent conversations:")
    for conv in recent_conversations:
        print(f"  - {conv['conversation_id']}: {conv['summary'][:50]}...")
    print()
    
    # Test 5: Get pending actions
    print("⏰ Test 5: Retrieving pending actions...")
    pending_actions = await connector.get_pending_actions(assignee="Alice")
    print(f"✅ Found {len(pending_actions)} pending actions for Alice:")
    for action in pending_actions:
        print(f"  - {action['action_item']} (Due: {action['deadline']})")
    print()
    
    # Test 6: Update action status
    print("✏️ Test 6: Updating action status...")
    if action_ids:
        success = await connector.update_action_status(action_ids[0], "In Progress")
        if success:
            print(f"✅ Updated action {action_ids[0]} to 'In Progress'\n")
        else:
            print(f"❌ Failed to update action status\n")
    
    # Test 7: Search knowledge base
    print("🔎 Test 7: Searching knowledge base...")
    search_results = await connector.search_knowledge("mobile development", limit=3)
    print(f"✅ Found {len(search_results)} knowledge entries:")
    for result in search_results:
        print(f"  - {result['topic']}: {result['content'][:50]}...")
    print()
    
    print("✨ All tests completed!")
    print("\nNote: This demo uses simulated responses.")
    print("To use real Airtable data, configure the MCP server in Claude Desktop.")


async def demo_real_world_flow():
    """Demonstrate a real-world usage flow"""
    
    print("\n" + "="*60)
    print("🌟 Real-World Usage Demo")
    print("="*60 + "\n")
    
    try:
        config = AirtableConfig.from_env()
        connector = AirtableConnector(config)
    except ValueError:
        print("⚠️  Skipping real-world demo (environment not configured)")
        return
    
    # Simulate processing a conversation from OMI device
    print("1️⃣ OMI device captures conversation...")
    await asyncio.sleep(1)
    
    print("2️⃣ Gateway agent processes with multiple agents...")
    await asyncio.sleep(1)
    
    # Save the processed results
    print("3️⃣ Saving results to Airtable...")
    
    conversation_id = await connector.save_conversation({
        "timestamp": datetime.now().isoformat(),
        "summary": "Team standup: Discussed API integration progress and blockers",
        "participants": ["TeamLead", "Developer1", "Developer2"],
        "topics": ["API integration", "performance", "testing"],
        "agent_analysis": "Multiple technical tasks identified"
    })
    
    await connector.save_action_items(conversation_id, [
        {
            "action_item": "Fix authentication bug in API client",
            "deadline": datetime.now().strftime("%Y-%m-%d"),
            "assignee": "Developer1"
        },
        {
            "action_item": "Write integration tests for new endpoints",
            "deadline": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
            "assignee": "Developer2"
        }
    ])
    
    print("4️⃣ Data saved and available in Airtable!")
    print("\n✅ Workflow complete - check your Airtable base for results")


async def main():
    """Run all tests and demos"""
    await test_airtable_operations()
    await demo_real_world_flow()


if __name__ == "__main__":
    print("\n🚀 Airtable MCP Integration Test\n")
    print("This script demonstrates how to integrate Airtable with NeuroHub")
    print("using the Model Context Protocol (MCP) server.\n")
    
    # Check for environment variables
    if not os.getenv("AIRTABLE_API_KEY") or not os.getenv("AIRTABLE_BASE_ID"):
        print("⚠️  Environment variables not set!")
        print("\nTo run this test with real Airtable integration:")
        print("1. Get your API key from: https://airtable.com/create/tokens")
        print("2. Get your base ID from your Airtable base URL")
        print("3. Set environment variables:")
        print("   export AIRTABLE_API_KEY=patXXXXXXXXXXXXXX")
        print("   export AIRTABLE_BASE_ID=appXXXXXXXXXXXXXX")
        print("\nRunning with simulated responses...\n")
    
    asyncio.run(main())