# 🚀 OMI + A2A Multi-Agent Demo Quick Start

## What This Demo Shows

This demo integrates the OMI wearable device with Google's Agent2Agent (A2A) protocol to create a powerful multi-agent system that:

1. **Captures conversations** via OMI device
2. **Orchestrates multiple AI agents** working together
3. **Analyzes context** and extracts insights
4. **Plans and executes actions** automatically
5. **Demonstrates agent-to-agent communication** using A2A protocol

## Architecture at a Glance

```
OMI Device → Gateway Agent → [Context Agent, Action Agent, Knowledge Agent...] → Results
```

## 🏃 Quick Start (5 minutes)

### 1. Prerequisites
- Python 3.11+
- Docker Desktop
- OMI API key (get from your OMI app: Settings → Developer → Generate API Key)
- AgentDB API key (from https://agentdb.dev)
- OpenAI API key (for AI agents) - optional but recommended

### 2. Setup

```bash
# Clone and navigate to demo
cd a2a-demo

# Run setup script (auto-detects UV if installed)
./setup.sh

# Edit .env.local with your API keys
nano .env.local  # or use your preferred editor
```

💡 **Using UV?** The setup script automatically detects and uses UV if installed. UV is much faster than pip for dependency resolution and installation.

### 3. Start the Multi-Agent System

```bash
# Start all agents with Docker
docker-compose up
```

You'll see 5 agents start up:
- 🌐 **OMI Gateway** (port 8001) - Main orchestrator
- 🧠 **Context Analysis** (port 8002) - Understands conversations
- 📋 **Action Planning** (port 8003) - Extracts tasks
- 📚 **Knowledge** (port 8004) - Information retrieval
- 📨 **Communication** (port 8005) - External messaging

### 4. Run the Demo

```bash
# In a new terminal
source venv/bin/activate
python demo/scenarios/meeting_assistant.py
```

## 🎭 Demo Scenarios

### Meeting Assistant
The included demo shows a meeting being processed:
1. Meeting transcript sent to Gateway
2. Context Agent analyzes participants and topics
3. Action Agent extracts tasks and deadlines
4. Communication Agent prepares follow-ups
5. Results aggregated and displayed

### What You'll See
```
🎯 OMI Multi-Agent Meeting Assistant Demo

✅ Connected to OMI Gateway
📤 Sent meeting transcript to multi-agent system
⏳ Processing through agents...

============================================================
📊 MULTI-AGENT ANALYSIS RESULTS
============================================================

🧠 Context Analysis Agent:

📝 Summary: Project status meeting discussing API integration
   testing, edge cases, and upcoming client presentation.

🏷️  Topics:
   - API Integration Testing
   - Error Handling Implementation
   - Client Presentation Preparation
   - Q4 Achievements

😊 Sentiment: positive

📋 Action Planning Agent:

Extracted 5 action items:

1. implement_retry_mechanism:
   Description: Implement retry mechanism with exponential backoff
   Details:
     - assignee: John & Mike
     - deadline: Thursday

2. send_test_summary:
   Description: Send test results summary
   Details:
     - assignee: John
     - deadline: Today 5 PM
```

## 🔧 Development

### Add a New Agent

1. Create agent directory: `agents/my_agent/`
2. Implement agent class extending `A2AAgent`
3. Define capabilities and handlers
4. Add to `docker-compose.yml`
5. Register in orchestration workflows

### Test Individual Agents

```bash
# Run a single agent
python -m agents.context_analysis.agent

# Test agent communication
curl http://localhost:8002/.well-known/agent.json
```

## 📁 Project Structure

```
a2a-demo/
├── agents/              # Individual A2A agents
│   ├── omi_gateway/     # Main orchestrator
│   ├── context_analysis/ # Context understanding
│   └── action_planning/  # Task extraction
├── core/               # A2A client wrapper
├── integrations/       # OMI connector
├── demo/              # Demo scenarios
└── docker-compose.yml  # Multi-agent setup
```

## 🌟 Key Features Demonstrated

- **A2A Protocol**: Agent discovery, task-based communication
- **Multi-Agent Orchestration**: Sequential and parallel workflows
- **Real-time Processing**: WebSocket streaming from OMI
- **Intelligent Analysis**: LLM-powered understanding
- **Action Execution**: Automated task handling

## 🚀 Next Steps

1. **Extend the demo**: Add more agents (calendar, email, CRM)
2. **Build a UI**: Create visualization dashboard
3. **Add more scenarios**: Personal assistant, learning companion
4. **Production deployment**: Scale with Kubernetes

## 📄 Resources

- [OMI Documentation](https://docs.omi.me)
- [A2A Protocol Spec](https://github.com/google-a2a/A2A)
- [Demo Source Code](./README.md)

---

**Questions?** Join the OMI Discord or check the documentation!