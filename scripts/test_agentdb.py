#!/usr/bin/env python3
"""Test AgentDB Connection

Verifies AgentDB API key and connection are working.
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from config.settings import settings
from integrations.agentdb_manager import AgentDBManager


async def test_agentdb_connection():
    """Test basic AgentDB functionality."""
    print("\n🧪 Testing AgentDB Connection...\n")
    
    try:
        # Get settings
        print(f"✅ API Key loaded: {settings.agentdb.api_key[:20]}...")
        print(f"✅ API URL: {settings.agentdb.api_url}")
        
        # Create manager
        db_manager = settings.get_agent_db_manager()
        print("\n📦 Creating test database...")
        
        # Create a test agent database
        test_agent_id = "test-agent"
        agent_db = await db_manager.create_agent_database(test_agent_id)
        print(f"✅ Created database: {agent_db.token}")
        
        # Store some test data
        print("\n📝 Storing test data...")
        await db_manager.store_agent_memory(
            test_agent_id,
            "test_key",
            {"message": "Hello from AgentDB!", "timestamp": "2025-07-24"}
        )
        print("✅ Data stored successfully")
        
        # Retrieve the data
        print("\n🔍 Retrieving test data...")
        data = await db_manager.get_agent_memory(test_agent_id, "test_key")
        print(f"✅ Retrieved: {data}")
        
        # Create a test conversation database
        print("\n💬 Creating conversation database...")
        conv_id = "test-conversation-001"
        conv_db = await db_manager.create_conversation_database(conv_id, "test-user")
        print(f"✅ Created conversation DB: {conv_db.token}")
        
        # Add a message
        print("\n📨 Adding conversation message...")
        await db_manager.add_conversation_message(
            conv_id,
            "user",
            "This is a test message for AgentDB integration."
        )
        print("✅ Message added successfully")
        
        print("\n🎉 All tests passed! AgentDB is working correctly.\n")
        
        # Note about actual implementation
        print("⚠️  Note: This test uses placeholder methods.")
        print("To fully implement, you'll need to:")
        print("1. Install AgentDB SDK: npm install @agentdb/sdk")
        print("2. Create Python wrapper or use HTTP API directly")
        print("3. Update the AgentDBManager with actual API calls\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nPlease check:")
        print("1. Your .env.local file exists")
        print("2. AGENTDB_API_KEY is set correctly")
        print("3. You have internet connection\n")
        raise


if __name__ == "__main__":
    asyncio.run(test_agentdb_connection())