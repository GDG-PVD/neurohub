# 🎓 OMI + Multi-Agent AI Demo - Student Guide

## 📚 Table of Contents
1. [What is This Demo?](#what-is-this-demo)
2. [Prerequisites](#prerequisites)
3. [Step-by-Step Setup](#step-by-step-setup)
4. [Running the Demo](#running-the-demo)
5. [Understanding What's Happening](#understanding-whats-happening)
6. [Troubleshooting](#troubleshooting)
7. [Glossary](#glossary)

> **⚠️ IMPORTANT**: This demo uses UV for Python commands. Always type `uv run python` instead of just `python`. See [UV_COMMANDS_GUIDE.md](UV_COMMANDS_GUIDE.md) for details!

---

## 🤔 What is This Demo?

This demo shows how a **wearable AI device** (OMI) can work with multiple AI agents to analyze conversations in real-time. Think of it like having a team of AI assistants that each specialize in different tasks:

- 🎙️ **OMI Device**: A wearable that records conversations
- 🤖 **AI Agents**: Specialized programs that analyze different aspects of conversations
- 🔄 **A2A Protocol**: A way for AI agents to talk to each other

### Real-World Example
Imagine you're in a meeting. The OMI device records the conversation, then:
1. One AI agent figures out what the meeting is about
2. Another AI agent finds all the action items
3. Another AI agent could send follow-up emails
4. They all work together automatically!

---

## 📋 Prerequisites

### Required Software
You'll need to install these programs first:

1. **Python 3.11 or newer**
   - 🍎 Mac: Download from [python.org](https://www.python.org/downloads/)
   - 🪟 Windows: Download from [python.org](https://www.python.org/downloads/)
   - 🐧 Linux: `sudo apt install python3.11`

2. **Docker Desktop**
   - Download from [docker.com](https://www.docker.com/products/docker-desktop/)
   - This runs the AI services in containers (like mini virtual machines)

3. **Git** (to download the code)
   - 🍎 Mac: Comes pre-installed or use `brew install git`
   - 🪟 Windows: Download from [git-scm.com](https://git-scm.com/)
   - 🐧 Linux: `sudo apt install git`

4. **A Text Editor** (to view/edit code)
   - Recommended: [VS Code](https://code.visualstudio.com/)

### Check Your Installation
Open a terminal/command prompt and run:
```bash
python --version     # Should show 3.11 or higher
docker --version     # Should show Docker version
git --version        # Should show git version
```

---

## 🚀 Step-by-Step Setup

### Step 1: Download the Demo Code

Open your terminal and run:
```bash
# Navigate to your projects folder (or create one)
cd ~/Desktop
mkdir ai-demos
cd ai-demos

# Clone the NeuroHub repository
git clone git@github.com:GDG-PVD/neurohub.git
cd neurohub
```

### Step 2: Install UV (Fast Python Package Manager)

UV makes installing Python packages much faster:

```bash
# On Mac/Linux:
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows (PowerShell):
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Step 3: Set Up the Python Environment

```bash
# Create a virtual environment and install dependencies
uv venv
uv pip install -e ".[dev]"
```

This installs all the required Python packages for the demo.

### Step 4: Configure Your API Keys

The demo needs some API keys to work. We'll create a configuration file:

```bash
# Create the configuration file
cp .env.example .env.local

# Open it in your text editor
# On Mac: open .env.local
# On Windows: notepad .env.local
```

In the file, you'll see:
```env
# OMI Backend Configuration
OMI_API_KEY=omi_mcp_your_key_here
OMI_API_URL=http://localhost:8000

# AgentDB Configuration (optional)
AGENTDB_API_KEY=your_key_here
```

For this demo, you can use these test keys:
```env
OMI_API_KEY=omi_mcp_da4ca036a2d6b21febcb3b99ad2b49da
OMI_API_URL=http://localhost:8000
```

Save and close the file.

### Step 5: Start the OMI Server

The OMI server simulates the wearable device's backend:

```bash
# Make sure Docker Desktop is running first!

# Start the OMI server
./scripts/start_omi_mcp.sh
```

You should see:
```
🚀 Starting OMI MCP Server...
✅ Using API Key: omi_mcp_da4ca036a2d6...
✅ OMI MCP Server started on http://localhost:8000
```

**Keep this terminal window open!**

---

## 🎮 Running the Demo

### Option 1: Simple Demo (Recommended for First Time)

Open a **new terminal window** and run:

```bash
# Navigate to the demo folder
cd ~/Desktop/ai-demos/omi/a2a-demo

# Run the demo with UV (Easiest!)
uv run python demo_simple.py
```

**Note**: If you see an error about `venv/bin/activate`, you're using the wrong command. We use UV which creates `.venv` (with a dot), not `venv`.

You'll see output like:
```
🎯 Simple OMI Connection Demo

1️⃣  Connecting to OMI MCP Server...
   ✅ Connected to http://localhost:8000

2️⃣  Processing sample conversation...
   ✅ Transcript processed

3️⃣  Simulating Multi-Agent Analysis...

🧠 Context Analysis (simulated):
   - Topic: Project Status Update
   - Participants: Sarah (lead), John, Mike
   - Sentiment: Collaborative, positive

📋 Action Items (simulated):
   1. John: Send project summary to Sarah by 5 PM
   2. Mike: Share edge case handling code with John
   3. Team: Fix edge cases in API integration

✨ Demo Complete!
```

### Option 2: Test OMI Connection

To verify everything is working:

```bash
uv run python scripts/test_omi_connection.py
```

This will test the connection to the OMI server and show what capabilities are available.

---

## 🧠 Understanding What's Happening

### The Architecture

```
┌─────────────┐     ┌─────────────────┐     ┌──────────────────┐
│ OMI Device  │────▶│  Gateway Agent  │────▶│ Context Analysis │
│ (Wearable)  │     │  (Orchestrator) │     │     Agent        │
└─────────────┘     └────────┬────────┘     └──────────────────┘
                             │
                             │               ┌──────────────────┐
                             └──────────────▶│ Action Planning  │
                                             │     Agent        │
                                             └──────────────────┘
```

1. **OMI Device** captures audio from conversations
2. **Gateway Agent** receives the audio and coordinates other agents
3. **Specialized Agents** each analyze different aspects:
   - Context Analysis: What's the conversation about?
   - Action Planning: What tasks were mentioned?
   - Knowledge Agent: What information is needed?
   - Communication Agent: Who needs to be notified?

### The A2A Protocol

A2A (Agent-to-Agent) is like a common language that lets AI agents:
- 🔍 Discover each other's capabilities
- 💬 Send tasks to each other
- 🤝 Work together on complex problems

### What Makes This Special?

Instead of one big AI doing everything, we have:
- **Specialized agents** that are experts in their domain
- **Scalability** - add new agents without changing existing ones
- **Reliability** - if one agent fails, others continue working
- **Flexibility** - mix and match agents for different use cases

---

## 🔧 Troubleshooting

### Common Issues and Solutions

#### "Cannot connect to Docker"
- **Solution**: Make sure Docker Desktop is running (look for the whale icon in your system tray)

#### "Module not found" errors
- **Solution**: Make sure you're using UV to run Python commands:
  ```bash
  uv run python your_script.py  # This handles the environment for you
  ```
  Or manually activate the virtual environment:
  ```bash
  source .venv/bin/activate  # Mac/Linux
  .venv\Scripts\activate     # Windows
  ```

#### "Connection refused on port 8000"
- **Solution**: The OMI server isn't running. Start it with:
  ```bash
  ./scripts/start_omi_mcp.sh
  ```

#### "Permission denied" when running scripts
- **Solution**: Make the script executable:
  ```bash
  chmod +x scripts/start_omi_mcp.sh
  ```

#### "venv/bin/activate not found"
- **Solution**: We use UV which creates `.venv` (with a dot), not `venv`. Use:
  ```bash
  uv run python demo_simple.py  # No activation needed!
  ```

#### Docker containers keep restarting
- **Solution**: This is a known issue with the full multi-agent demo. For now, use the simple demo (`demo_simple.py`) which works perfectly!

#### "Container name already in use" error
- **Solution**: The OMI server is already running! The updated script will detect this automatically. To manually restart:
  ```bash
  docker stop omi-mcp-server
  ./scripts/start_omi_mcp.sh
  ```
  Or use the stop script:
  ```bash
  ./scripts/stop_omi_mcp.sh
  ./scripts/start_omi_mcp.sh
  ```

### Getting Help

If you're stuck:
1. Check the error message carefully
2. Look at the [troubleshooting guide](docs/guides/troubleshooting.md)
3. Ask your instructor or TA
4. Check the project's documentation

---

## 📖 Glossary

**Agent**: A specialized AI program that performs specific tasks

**A2A Protocol**: Agent-to-Agent protocol - a standard way for AI agents to communicate

**API**: Application Programming Interface - how programs talk to each other

**API Key**: A secret password that gives you access to a service

**Docker**: Software that runs applications in isolated containers

**MCP**: Model Context Protocol - A standard for AI tools to interact with context providers like OMI

**Orchestrator**: A coordinator that manages multiple agents

**Virtual Environment**: An isolated Python installation for this project

**WebSocket**: A technology for real-time, two-way communication

---

## 🎯 Learning Objectives

After completing this demo, you'll understand:
1. How AI agents can work together to solve complex problems
2. The basics of distributed AI systems
3. How wearable devices can integrate with AI services
4. The importance of modular architecture in AI systems

---

## 📚 Further Learning

Want to learn more? Check out:
- [OMI Documentation](https://docs.omi.me)
- [Introduction to Multi-Agent Systems](docs/guides/multi-agent-intro.md)
- [A2A Protocol Specification](https://github.com/a2a-project/a2a-spec)
- [Building Your Own Agent](docs/guides/create-agent.md)

---

## 🎉 Congratulations!

You've successfully run a multi-agent AI demo! This is cutting-edge technology that represents the future of AI systems - where multiple specialized agents work together like a team.

### What's Next?
- Try modifying the sample conversation in `demo_simple.py`
- Explore the agent code in the `agents/` directory
- Think about what other types of agents could be useful
- Consider how this technology could be applied in your field of study

---

*Remember: Learning AI is a journey. Don't worry if everything doesn't make sense immediately. Each time you work with these systems, you'll understand a bit more!* 🚀