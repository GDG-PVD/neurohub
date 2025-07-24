#!/usr/bin/env python3
"""Test OMI Backend Connection

Verifies OMI API key and connection are working.
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from config.settings import settings
from integrations.omi_connector import OMIConnector


async def test_omi_connection():
    """Test basic OMI backend connectivity."""
    print("\n🔌 Testing OMI Backend Connection...\n")
    
    try:
        # Get settings
        print(f"✅ API Key loaded: {settings.omi.api_key[:20]}...")
        print(f"✅ API URL: {settings.omi.api_url}")
        
        # Create connector
        async with OMIConnector(
            api_url=settings.omi.api_url,
            api_key=settings.omi.api_key
        ) as omi:
            print("\n📊 Testing OMI API endpoints...\n")
            
            # Test 1: Get user memories (should work with MCP key)
            print("1. Testing memory retrieval...")
            memories = await omi.get_user_memories("test-user", limit=5)
            print(f"   ✅ Retrieved {len(memories)} memories")
            
            # Test 2: Get apps
            print("\n2. Testing app retrieval...")
            apps = await omi.get_apps(enabled_only=True)
            print(f"   ✅ Found {len(apps)} enabled apps")
            if apps:
                print("   Apps:")
                for app in apps[:3]:  # Show first 3
                    print(f"   - {app.get('name', 'Unknown')}")
            
            # Test 3: Test audio processing (simulated)
            print("\n3. Testing audio processing (simulated)...")
            test_audio = b"test audio data"
            result = await omi.process_audio(
                test_audio,
                {"session_id": "test-session", "simulated_transcript": "Hello, this is a test."}
            )
            print(f"   ✅ Transcript: {result.get('transcript', 'N/A')}")
            
            print("\n🎉 OMI connection test successful!\n")
            
            # Note about MCP capabilities
            print("ℹ️  Note: Your MCP API key allows:")
            print("   - Reading memories and conversations")
            print("   - Searching memories")
            print("   - Getting user context")
            print("   - Limited write operations\n")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nPlease check:")
        print("1. Your .env.local file exists")
        print("2. OMI_API_KEY is set correctly")
        print("3. OMI backend is running (default: http://localhost:8000)")
        print("4. Your API key has proper permissions\n")
        
        # Check if it's a connection error
        if "Cannot connect" in str(e) or "ClientConnectorError" in str(e):
            print("💡 Tip: Make sure the OMI backend is running:")
            print("\n   Option 1: Run OMI MCP Server (Docker):")
            print("   ./scripts/start_omi_mcp.sh")
            print("\n   Option 2: Run OMI backend locally:")
            print("   cd ../backend")
            print("   python main.py\n")
        raise


async def test_mcp_endpoints():
    """Test MCP-specific endpoints if available."""
    print("\n🔧 Testing MCP-specific endpoints...\n")
    
    try:
        # These endpoints might be available with MCP keys
        async with OMIConnector(
            api_url=settings.omi.api_url,
            api_key=settings.omi.api_key
        ) as omi:
            # Try MCP-specific operations
            print("Testing MCP memory search...")
            results = await omi.search_memories(
                user_id="test-user",
                query="test query",
                limit=3
            )
            print(f"✅ Search returned {len(results)} results\n")
            
    except Exception as e:
        print(f"ℹ️  MCP endpoint test failed (this may be normal): {e}\n")


if __name__ == "__main__":
    print("\n🚀 OMI Backend Connection Test\n")
    print("This script tests the connection to your OMI backend")
    print("using the MCP API key you've configured.\n")
    
    asyncio.run(test_omi_connection())
    
    # Optionally test MCP-specific features
    # asyncio.run(test_mcp_endpoints())