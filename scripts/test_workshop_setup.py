#!/usr/bin/env python3
"""
Workshop Setup Test Script
Run this to verify your environment is correctly configured
"""

import os
import sys
import asyncio
import importlib.util
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Colors for output
GREEN = '\033[0;32m'
RED = '\033[0;31m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
NC = '\033[0m'  # No Color


def print_status(message: str, status: bool):
    """Print colored status message"""
    symbol = "✅" if status else "❌"
    color = GREEN if status else RED
    print(f"{color}{symbol} {message}{NC}")


def print_info(message: str):
    """Print info message"""
    print(f"{BLUE}ℹ️  {message}{NC}")


def print_warning(message: str):
    """Print warning message"""
    print(f"{YELLOW}⚠️  {message}{NC}")


async def test_environment():
    """Test environment setup"""
    print(f"\n{BLUE}🔧 Testing Environment Setup{NC}\n")
    
    all_good = True
    
    # Test Python version
    python_version = sys.version_info
    python_ok = python_version >= (3, 11)
    print_status(
        f"Python version: {python_version.major}.{python_version.minor}.{python_version.micro} "
        f"(requires >= 3.11)", 
        python_ok
    )
    if not python_ok:
        all_good = False
    
    # Test UV installation
    try:
        import subprocess
        result = subprocess.run(["uv", "--version"], capture_output=True, text=True)
        uv_ok = result.returncode == 0
        print_status(f"UV package manager: {result.stdout.strip() if uv_ok else 'Not found'}", uv_ok)
    except:
        print_status("UV package manager: Not found", False)
        all_good = False
    
    # Test key packages
    packages = [
        ("fastapi", "FastAPI"),
        ("pydantic", "Pydantic"),
        ("websockets", "WebSockets"),
        ("aiohttp", "aiohttp"),
        ("openai", "OpenAI SDK"),
        ("rich", "Rich (terminal formatting)")
    ]
    
    print(f"\n{BLUE}📦 Testing Package Installation{NC}\n")
    
    for package, name in packages:
        try:
            importlib.import_module(package)
            print_status(f"{name}: Installed", True)
        except ImportError:
            print_status(f"{name}: Not installed", False)
            all_good = False
    
    # Test project structure
    print(f"\n{BLUE}📁 Testing Project Structure{NC}\n")
    
    required_dirs = [
        "agents",
        "agents/examples",
        "agents/templates",
        "core",
        "integrations",
        "docs",
        "scripts"
    ]
    
    for dir_path in required_dirs:
        full_path = PROJECT_ROOT / dir_path
        exists = full_path.exists()
        print_status(f"Directory {dir_path}: {'Found' if exists else 'Missing'}", exists)
        if not exists:
            all_good = False
    
    # Test environment variables
    print(f"\n{BLUE}🔑 Testing Environment Variables{NC}\n")
    
    env_vars = [
        ("OMI_API_BASE_URL", True),   # Required
        ("OMI_API_KEY", True),         # Required
        ("OPENAI_API_KEY", False),     # Optional
        ("ANTHROPIC_API_KEY", False),  # Optional
        ("FUTUREHOUSE_API_KEY", False),# Optional
        ("MEM0_API_KEY", False)        # Optional
    ]
    
    missing_required = []
    for var, required in env_vars:
        value = os.getenv(var)
        has_value = value is not None and value != ""
        
        if required and not has_value:
            missing_required.append(var)
            print_status(f"{var}: Not set (REQUIRED)", False)
            all_good = False
        elif required and has_value:
            print_status(f"{var}: Set", True)
        elif not required and not has_value:
            print_warning(f"{var}: Not set (optional)")
        else:
            print_status(f"{var}: Set", True)
    
    # Test core imports
    print(f"\n{BLUE}🧪 Testing Core Imports{NC}\n")
    
    try:
        from core.a2a_wrappers import A2AAgent, A2ATask
        print_status("A2A client imports: Success", True)
    except Exception as e:
        print_status(f"A2A client imports: Failed - {e}", False)
        all_good = False
    
    try:
        from integrations.omi_connector import OMIConnector
        print_status("OMI connector imports: Success", True)
    except Exception as e:
        print_status(f"OMI connector imports: Failed - {e}", False)
        all_good = False
    
    # Test example agents
    print(f"\n{BLUE}🤖 Testing Example Agents{NC}\n")
    
    try:
        from agents.examples.research_agent import ScientificResearchAgent
        agent = ScientificResearchAgent()
        print_status("Research agent: Loaded successfully", True)
    except Exception as e:
        print_status(f"Research agent: Failed - {e}", False)
        all_good = False
    
    try:
        from agents.examples.collaboration_agent import TeamCollaborationAgent
        agent = TeamCollaborationAgent()
        print_status("Collaboration agent: Loaded successfully", True)
    except Exception as e:
        print_status(f"Collaboration agent: Failed - {e}", False)
        all_good = False
    
    # Test network connectivity
    print(f"\n{BLUE}🌐 Testing Network Connectivity{NC}\n")
    
    try:
        import aiohttp
        async with aiohttp.ClientSession() as session:
            # Test OMI backend
            omi_url = os.getenv("OMI_API_BASE_URL", "https://neurohub-workshop.fly.dev")
            try:
                async with session.get(f"{omi_url}/health", timeout=5) as response:
                    omi_ok = response.status == 200
                    print_status(f"OMI backend ({omi_url}): {'Connected' if omi_ok else 'Failed'}", omi_ok)
            except:
                print_status(f"OMI backend ({omi_url}): Connection failed", False)
                all_good = False
            
            # Test external APIs (just check if reachable)
            apis = [
                ("https://api.openai.com", "OpenAI API"),
                ("https://api.anthropic.com", "Claude API"),
                ("https://api.futurehouse.org", "FutureHouse API")
            ]
            
            for url, name in apis:
                try:
                    async with session.head(url, timeout=3) as response:
                        # Just check if we can reach it (might return 401 without auth)
                        reachable = response.status < 500
                        print_status(f"{name}: {'Reachable' if reachable else 'Unreachable'}", reachable)
                except:
                    print_warning(f"{name}: Could not reach (may need VPN or be behind firewall)")
    
    except Exception as e:
        print_status(f"Network tests failed: {e}", False)
        all_good = False
    
    # Summary
    print(f"\n{BLUE}📊 Test Summary{NC}\n")
    
    if all_good:
        print(f"{GREEN}✅ All tests passed! Your environment is ready for the workshop.{NC}\n")
        print(f"{BLUE}Next steps:{NC}")
        print("1. Run: ./scripts/setup_team.sh YOUR_TEAM_NAME")
        print("2. Configure your API keys in teams/YOUR_TEAM_NAME/.env")
        print("3. Start building your agents!")
    else:
        print(f"{RED}❌ Some tests failed. Please fix the issues above.{NC}\n")
        if missing_required:
            print(f"{YELLOW}Missing required environment variables:{NC}")
            for var in missing_required:
                print(f"  - {var}")
            print("\nCreate a .env.local file with these variables or export them.")
    
    return all_good


async def test_simple_agent():
    """Test creating a simple agent"""
    print(f"\n{BLUE}🧪 Testing Simple Agent Creation{NC}\n")
    
    try:
        from agents.templates.agent_builder import CustomAgent
        from core.a2a_wrappers import A2ATask
        
        # Create simple agent
        agent = CustomAgent(
            name="test-agent",
            description="Test agent for workshop",
            capabilities=["test"],
            mcp_provider="openai"
        )
        
        # Create test task
        task = A2ATask(
            id="test-1",
            type="analyze",
            data={"text": "Hello workshop!", "analysis_type": "test"}
        )
        
        # Process task
        result = await agent.process_task(task)
        
        success = result.get("status") == "success"
        print_status("Simple agent test: " + ("Passed" if success else "Failed"), success)
        
        if success:
            print_info("Agent successfully processed a test task!")
        
        return success
        
    except Exception as e:
        print_status(f"Simple agent test: Failed - {e}", False)
        return False


async def main():
    """Run all tests"""
    print(f"{BLUE}{'='*60}{NC}")
    print(f"{BLUE}🚀 NeuroHub Workshop Environment Test{NC}")
    print(f"{BLUE}{'='*60}{NC}")
    
    # Run environment tests
    env_ok = await test_environment()
    
    # Run agent test if environment is OK
    if env_ok:
        await test_simple_agent()
    
    print(f"\n{BLUE}{'='*60}{NC}")
    print(f"{BLUE}Happy hacking! 🎉{NC}")
    print(f"{BLUE}{'='*60}{NC}\n")


if __name__ == "__main__":
    asyncio.run(main())