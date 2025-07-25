# 🚀 Quick Start Guide - NeuroHub with API Integrations

This guide shows how to run NeuroHub with all your configured API integrations.

## Prerequisites

✅ `.env.local` file is configured with your API keys
✅ UV package manager installed (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
✅ Dependencies installed (`uv pip install -e ".[dev]"`)

## 1. Create Airtable Base

Before running the full integration:

1. Go to [airtable.com](https://airtable.com)
2. Create a new base called "NeuroHub"
3. Get the base ID from the URL (e.g., `appABC123...`)
4. Update `.env.local`:
   ```bash
   AIRTABLE_BASE_ID=appYourBaseIdHere
   ```

## 2. Run the Simple Demo

Test basic OMI connection:

```bash
uv run python demo_simple.py
```

Expected output:
- ✅ Connected to OMI MCP Server
- ✅ Transcript processed
- ✅ Multi-agent analysis (simulated)

## 3. Test Airtable Integration

Once you have your base ID:

```bash
# Export the base ID
export AIRTABLE_BASE_ID=appYourBaseIdHere

# Run the test
uv run python scripts/test_airtable_integration.py
```

This will:
- Save conversation summaries
- Create action items
- Store knowledge entries

## 4. Run Full Multi-Agent System

Start all agents with Docker:

```bash
docker-compose up
```

Or run agents individually:

```bash
# Terminal 1: Gateway Agent
uv run python agents/omi_gateway/agent.py

# Terminal 2: Context Analysis Agent
uv run python agents/context_analysis/agent.py

# Terminal 3: Action Planning Agent
uv run python agents/action_planning/agent.py
```

## 5. Configure Claude Desktop MCP

Add to your `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "airtable": {
      "command": "node",
      "args": ["/path/to/airtable-mcp-server/dist/index.js"],
      "env": {
        "AIRTABLE_API_KEY": "your_airtable_api_key",
        "AIRTABLE_BASE_ID": "appYourBaseIdHere"
      }
    },
    "omi": {
      "command": "docker",
      "args": [
        "run", "--rm", "-i", 
        "-e", "OMI_API_KEY=your_omi_api_key",
        "omiai/mcp-server"
      ]
    }
  }
}
```

## 6. Test Research APIs

Create a test script to verify research API access:

```python
# test_research_apis.py
import os
from futurehouse_client import FutureHouseClient

# Test FutureHouse
client = FutureHouseClient(api_key=os.getenv("FUTUREHOUSE_API_KEY"))
print("✅ FutureHouse client initialized")

# Test other APIs as needed...
```

## Available Features

With your API keys configured, you can:

### 🧠 AI Agents
- Use GPT-4 for context analysis
- Use Gemini for alternative perspectives
- Process OMI device conversations

### 💾 Data Storage
- Store conversations in Airtable
- Track action items with deadlines
- Build searchable knowledge base

### 🔬 Research Integration
- Search PubMed for medical literature
- Analyze papers with PaperQA
- Access FutureHouse AI research tools

## Troubleshooting

### OMI Connection Issues
```bash
# Check if OMI MCP server is running
docker ps | grep omi-mcp-server

# Start it if needed
./scripts/start_omi_mcp.sh
```

### Airtable Errors
- Verify API key has correct scopes
- Check base ID format (starts with 'app')
- Ensure tables exist in your base

### API Key Issues
- Check `.env.local` is loaded: `echo $OPENAI_API_KEY`
- Verify keys are not expired
- Check rate limits

## Next Steps

1. **Customize Agents**: Modify agent behaviors in `agents/*/agent.py`
2. **Add New Integrations**: Create connectors in `integrations/`
3. **Build Dashboards**: Use Airtable's interface designer
4. **Deploy to Cloud**: Follow the deployment guides

## Security Reminder

⚠️ **NEVER commit `.env.local` to git!**

Always use:
```bash
git status  # Check no .env files are staged
git diff --cached  # Verify before committing
```

## Support

- Documentation: `docs/guides/`
- Issues: Create in project repository
- Examples: `scripts/test_*.py`

Happy building! 🚀