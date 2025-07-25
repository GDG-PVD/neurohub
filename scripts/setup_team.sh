#!/bin/bash
# NeuroHub Workshop - Team Setup Script
# This script sets up a team's development environment for the hackathon

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get team name from argument
TEAM_NAME=$1

if [ -z "$TEAM_NAME" ]; then
    echo -e "${RED}Error: Please provide a team name${NC}"
    echo "Usage: ./setup_team.sh TEAM_NAME"
    echo "Example: ./setup_team.sh team_alpha"
    exit 1
fi

echo -e "${BLUE}🚀 NeuroHub Workshop Setup for Team: ${TEAM_NAME}${NC}\n"

# Create team directory
TEAM_DIR="teams/${TEAM_NAME}"
echo -e "${GREEN}1. Creating team directory...${NC}"
mkdir -p $TEAM_DIR/{agents,configs,tests,docs}

# Copy templates
echo -e "${GREEN}2. Copying agent templates...${NC}"
cp -r agents/templates/* $TEAM_DIR/agents/
cp agents/examples/*.py $TEAM_DIR/agents/

# Create team-specific configuration
echo -e "${GREEN}3. Creating team configuration...${NC}"
cat > $TEAM_DIR/configs/team_config.json << EOF
{
    "team_name": "${TEAM_NAME}",
    "created_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
    "members": [],
    "omi_device_id": "",
    "use_case": "",
    "agents": []
}
EOF

# Create .env file for the team
echo -e "${GREEN}4. Setting up environment variables...${NC}"
cat > $TEAM_DIR/.env << EOF
# Team ${TEAM_NAME} Environment Variables
# Add your API keys here (DO NOT COMMIT THIS FILE!)

# OMI Configuration
OMI_API_BASE_URL=https://neurohub-workshop.fly.dev
OMI_API_KEY=neurohub_workshop_2024

# LLM Providers (get your own keys)
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_claude_key_here

# External APIs
FUTUREHOUSE_API_KEY=your_futurehouse_key_here
MEM0_API_KEY=your_mem0_key_here

# Team Configuration
TEAM_NAME=${TEAM_NAME}
AGENT_PREFIX=${TEAM_NAME}_
EOF

# Create a starter agent for the team
echo -e "${GREEN}5. Creating starter agent...${NC}"
cat > $TEAM_DIR/agents/${TEAM_NAME}_agent.py << 'EOF'
"""
Starter agent for team: TEAM_NAME_PLACEHOLDER
Customize this agent for your use case!
"""

from agents.templates.agent_builder import CustomAgent, A2ATask
import asyncio


class TeamAgent(CustomAgent):
    """Your team's custom agent"""
    
    def __init__(self):
        super().__init__(
            name="TEAM_NAME_PLACEHOLDER-agent",
            description="Our awesome agent that does...",
            capabilities=["analyze", "process", "integrate"],
            mcp_provider="openai"  # or "claude"
        )
    
    async def process_omi_memory(self, omi_memory: dict, options: dict) -> dict:
        """
        Implement your main logic here
        
        This method receives OMI memory data and should return
        processed results based on your use case
        """
        transcript = omi_memory.get("transcript", "")
        
        # TODO: Add your processing logic
        # Example: Extract specific information, analyze patterns, etc.
        
        result = {
            "processed": True,
            "transcript_length": len(transcript),
            "insights": []  # Add your insights here
        }
        
        return result


# Quick test function
async def test_agent():
    agent = TeamAgent()
    
    # Test task
    task = A2ATask(
        id="test-1",
        type="process",
        data={
            "omi_memory": {
                "transcript": "This is a test conversation from the OMI device."
            }
        }
    )
    
    result = await agent.process_task(task)
    print(f"Test result: {result}")


if __name__ == "__main__":
    print("Testing TEAM_NAME_PLACEHOLDER agent...")
    asyncio.run(test_agent())
EOF

# Replace placeholder with actual team name
sed -i.bak "s/TEAM_NAME_PLACEHOLDER/${TEAM_NAME}/g" $TEAM_DIR/agents/${TEAM_NAME}_agent.py
rm $TEAM_DIR/agents/${TEAM_NAME}_agent.py.bak

# Create README for the team
echo -e "${GREEN}6. Creating team documentation...${NC}"
cat > $TEAM_DIR/README.md << EOF
# Team ${TEAM_NAME} - NeuroHub Workshop

## Quick Start

1. **Install dependencies**:
   \`\`\`bash
   cd $(pwd)
   uv pip install -e ".[dev,demo]"
   \`\`\`

2. **Configure environment**:
   - Edit \`teams/${TEAM_NAME}/.env\` with your API keys
   - Update \`configs/team_config.json\` with team details

3. **Test your agent**:
   \`\`\`bash
   uv run python teams/${TEAM_NAME}/agents/${TEAM_NAME}_agent.py
   \`\`\`

4. **Connect to OMI device**:
   \`\`\`bash
   uv run python workshop_server_enhanced.py
   \`\`\`

## Your Agents

- \`${TEAM_NAME}_agent.py\` - Your starter agent (customize this!)
- \`agent_builder.py\` - Template for building new agents
- \`research_agent.py\` - Example research agent
- \`collaboration_agent.py\` - Example team collaboration agent

## Resources

- [Workshop Guide](../../WORKSHOP_HACKATHON_GUIDE.md)
- [Agent Templates](../../agents/templates/)
- [API Documentation](../../docs/apis/)

## Team Members

Add your team members here:
1. 
2. 
3. 
4. 

## Use Case

Describe your use case here...

## Architecture

Add your agent architecture diagram here...

Good luck! 🚀
EOF

# Create a test file
echo -e "${GREEN}7. Creating test file...${NC}"
cat > $TEAM_DIR/tests/test_${TEAM_NAME}_agent.py << EOF
"""
Tests for ${TEAM_NAME} agent
"""

import pytest
import asyncio
from agents.${TEAM_NAME}_agent import TeamAgent
from core.a2a_client import A2ATask


@pytest.mark.asyncio
async def test_agent_initialization():
    """Test agent initializes correctly"""
    agent = TeamAgent()
    assert agent.name == "${TEAM_NAME}-agent"
    assert "analyze" in agent.capabilities


@pytest.mark.asyncio
async def test_process_omi_memory():
    """Test processing OMI memory"""
    agent = TeamAgent()
    
    task = A2ATask(
        id="test-1",
        type="process",
        data={
            "omi_memory": {
                "transcript": "Test conversation"
            }
        }
    )
    
    result = await agent.process_task(task)
    assert result["status"] == "success"
    assert "result" in result


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
EOF

# Create run script
echo -e "${GREEN}8. Creating run scripts...${NC}"
cat > $TEAM_DIR/run_agent.sh << EOF
#!/bin/bash
# Quick script to run your agent

cd $(pwd)
source teams/${TEAM_NAME}/.env
uv run python teams/${TEAM_NAME}/agents/${TEAM_NAME}_agent.py
EOF

chmod +x $TEAM_DIR/run_agent.sh

# Create docker-compose for the team (optional)
echo -e "${GREEN}9. Creating Docker configuration...${NC}"
cat > $TEAM_DIR/docker-compose.yml << EOF
version: '3.8'

services:
  ${TEAM_NAME}-agent:
    build: 
      context: ../../
      dockerfile: Dockerfile
    environment:
      - TEAM_NAME=${TEAM_NAME}
    env_file:
      - .env
    volumes:
      - ./agents:/app/teams/${TEAM_NAME}/agents
    ports:
      - "850\${TEAM_NUMBER:-0}:8000"
    command: uv run python teams/${TEAM_NAME}/agents/${TEAM_NAME}_agent.py
EOF

# Final setup summary
echo -e "\n${GREEN}✅ Setup Complete!${NC}\n"
echo -e "${BLUE}Team ${TEAM_NAME} workspace created at: ${TEAM_DIR}${NC}"
echo -e "\n${YELLOW}Next Steps:${NC}"
echo -e "1. ${YELLOW}cd ${TEAM_DIR}${NC}"
echo -e "2. ${YELLOW}Edit .env${NC} with your API keys"
echo -e "3. ${YELLOW}Update configs/team_config.json${NC} with team details"
echo -e "4. ${YELLOW}Customize agents/${TEAM_NAME}_agent.py${NC} for your use case"
echo -e "5. ${YELLOW}Run ./run_agent.sh${NC} to test your agent"
echo -e "\n${GREEN}📚 Resources:${NC}"
echo -e "- Workshop Guide: ${BLUE}WORKSHOP_HACKATHON_GUIDE.md${NC}"
echo -e "- Agent Examples: ${BLUE}agents/examples/${NC}"
echo -e "- Slack Channel: ${BLUE}#neurohub-hackathon${NC}"
echo -e "\n${GREEN}Happy hacking! 🚀${NC}"

# Create quick reference card
cat > $TEAM_DIR/QUICK_REFERENCE.md << EOF
# Quick Reference - Team ${TEAM_NAME}

## Common Commands

\`\`\`bash
# Run your agent
./run_agent.sh

# Test with OMI device
uv run python workshop_server_enhanced.py

# Run tests
uv run pytest tests/

# Format code
uv run black agents/

# Check types
uv run mypy agents/
\`\`\`

## Agent Methods to Implement

1. \`process_omi_memory()\` - Main processing logic
2. \`handle_analyze()\` - Analysis tasks
3. \`handle_query()\` - Question answering
4. \`handle_integrate()\` - External API calls

## Available APIs

- **FutureHouse**: Scientific research (CROW, FALCON, OWL, PHOENIX)
- **Mem0**: Memory storage and retrieval
- **OpenAI/Claude**: General AI capabilities

## Debugging Tips

- Check logs in \`logs/\` directory
- Use \`logger.info()\` for debugging
- Test with small transcripts first
- Verify API keys are set correctly
EOF

echo -e "\n${GREEN}Team ${TEAM_NAME} is ready to build amazing agents! 🎉${NC}"