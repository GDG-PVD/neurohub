# Getting Started Guide

## Overview

This guide will help you set up and run the OMI A2A Multi-Agent Demo from scratch.

## Prerequisites

### Required
1. **Python 3.11+** - The project requires Python 3.11 or higher
2. **Docker Desktop** - For running the multi-agent system
3. **API Keys**:
   - **OMI API Key** - Get from your OMI app (Settings → Developer → Generate API Key)
   - **AgentDB API Key** - Sign up at [agentdb.dev](https://agentdb.dev)

### Optional but Recommended
- **OpenAI API Key** - For Context Analysis Agent (GPT-4)
- **UV Package Manager** - For faster dependency installation

## Step 1: Get Your API Keys

### OMI API Key
1. Open your OMI mobile app
2. Go to Settings → Developer
3. Tap "Generate API Key"
4. Copy the key (format: `omi_mcp_...`)

### AgentDB API Key
1. Visit [agentdb.dev](https://agentdb.dev)
2. Sign up for an account
3. Go to Dashboard → API Keys
4. Create a new key

### OpenAI API Key (Optional)
1. Visit [platform.openai.com](https://platform.openai.com)
2. Sign up/login
3. Go to API Keys
4. Create new secret key

## Step 2: Clone and Setup

```bash
# Clone the repository
git clone <repo-url>
cd omi/a2a-demo

# Run the setup script
./setup.sh

# Or manually:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e ".[dev]"
```

## Step 3: Configure Environment

1. Copy the example environment file:
```bash
cp .env.example .env.local
```

2. Edit `.env.local` and add your keys:
```env
# OMI Backend Configuration
OMI_API_KEY=omi_mcp_your_key_here
OMI_API_URL=http://localhost:8000  # Or your OMI backend URL

# AgentDB Configuration
AGENTDB_API_KEY=agentdb_your_key_here
AGENTDB_API_URL=https://api.agentdb.dev

# OpenAI Configuration (optional)
OPENAI_API_KEY=sk-your_key_here
```

## Step 4: Test Connections

### Test OMI Connection
```bash
python scripts/test_omi_connection.py
```

Expected output:
```
✅ API Key loaded: omi_mcp_da4ca036a2d6...
✅ API URL: http://localhost:8000
🎉 OMI connection test successful!
```

### Test AgentDB Connection
```bash
python scripts/test_agentdb.py
```

## Step 5: Start the System

### Using Docker (Recommended)
```bash
# Start all agents
docker-compose up

# Or run in background
docker-compose up -d

# Check status
docker-compose ps
```

### Running Locally (Development)
```bash
# Terminal 1: Gateway Agent
python -m agents.omi_gateway.agent

# Terminal 2: Context Analysis Agent
python -m agents.context_analysis.agent

# Add more agents as needed...
```

## Step 6: Run the Demo

```bash
# Make sure agents are running first!
python demo/scenarios/meeting_assistant.py
```

You should see:
```
🎯 OMI Multi-Agent Meeting Assistant Demo
✅ Connected to OMI Gateway
📤 Sent meeting transcript to multi-agent system
⏳ Processing through agents...
📊 MULTI-AGENT ANALYSIS RESULTS
```

## Troubleshooting

### "OMI_API_KEY not found"
- Make sure `.env.local` exists
- Check the key is in the correct format
- Restart your terminal/IDE

### "Cannot connect to OMI backend"
- Ensure OMI backend is running
- Check the URL in `.env.local`
- Verify firewall settings

### "AgentDB API error"
- Verify your API key is active
- Check your usage limits
- Ensure internet connection

### Docker Issues
- Make sure Docker Desktop is running
- Try `docker-compose down` then `up` again
- Check logs: `docker-compose logs <service-name>`

## Next Steps

1. **Explore the Demo**: Try different conversation scenarios
2. **Build Your Own Agent**: See [Development Guide](development.md)
3. **Customize Workflows**: Modify orchestration patterns
4. **Deploy to Production**: See [Deployment Guide](deployment.md)

## Useful Commands

```bash
# Using Makefile
make install      # Install dependencies
make dev         # Run gateway agent
make test        # Run tests
make docker-up   # Start all agents
make docker-down # Stop all agents

# Manual commands
docker-compose logs -f    # View logs
docker-compose restart    # Restart services
uvicorn --reload         # Dev mode with auto-reload
```

## Getting Help

- Check the [FAQ](faq.md)
- Review [Architecture Docs](../architecture/README.md)
- Join the OMI Discord community
- Open an issue on GitHub