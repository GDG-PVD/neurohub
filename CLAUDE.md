# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

NeuroHub is an educational demonstration of multi-agent AI systems using OMI wearable device and the A2A protocol. The project showcases how AI agents can collaborate to analyze real-time conversations.

## Key Development Commands

### Environment Setup
```bash
# Install UV package manager (required)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
uv venv
uv pip install -e ".[dev]"

# Copy environment configuration
cp .env.example .env.local
```

### Running the Application

#### Simple Demo (Recommended)
```bash
# Using cloud backend (workshop mode)
export OMI_API_BASE_URL=https://neurohub-workshop.fly.dev
export OMI_API_KEY=neurohub_workshop_2024
uv run python demo_simple.py

# Using local backend
./scripts/start_omi_mcp.sh  # Terminal 1
uv run python demo_simple.py  # Terminal 2
```

#### Full Multi-Agent System
```bash
# Start all services with Docker
docker-compose up

# Or start individual agents
uv run python agents/omi_gateway/agent.py
uv run python agents/context_analysis/agent.py
uv run python agents/action_planning/agent.py
```

### Testing
```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/test_demo_simple.py

# Run with coverage
uv run pytest --cov=agents --cov=core --cov=integrations
```

### Code Quality
```bash
# Format code
uv run black .

# Lint code
uv run ruff check .

# Type checking
uv run mypy .
```

## Architecture Overview

### Multi-Agent System Design
```
OMI Device → Gateway Agent → Context Analysis Agent
                          ↘ Action Planning Agent
                          ↘ Knowledge Agent
```

- **Gateway Agent** (port 8001): Orchestrates communication between OMI device and other agents
- **Context Analysis Agent** (port 8002): Analyzes conversation context and intent
- **Action Planning Agent** (port 8003): Extracts action items and deadlines
- **Knowledge Agent** (port 8004): Manages persistent knowledge storage

### Key Patterns

1. **A2A Protocol**: All agents communicate using Google's A2A protocol (currently mocked in `a2a_sdk.py`)
2. **Gateway Pattern**: OMI Gateway serves as the central orchestrator (see `agents/omi_gateway/agent.py`)
3. **Async Architecture**: All agent communication is asynchronous using FastAPI and WebSockets
4. **Educational Design**: Code prioritizes clarity over production features

### Project Structure
- `agents/`: Individual agent implementations
- `core/`: A2A client wrapper and shared utilities
- `integrations/`: External service connectors (OMI, AgentDB)
- `demo_simple.py`: Simplified demo for workshops (simulates multi-agent responses)
- `docs/adr/`: Architecture Decision Records documenting key choices

### Important Files
- `core/a2a_client.py`: Base classes for A2A agents and orchestration
- `integrations/omi_connector.py`: OMI device integration
- `config/settings.py`: Configuration management using Pydantic

## Development Notes

1. **UV Package Manager**: This project uses UV instead of pip. Always prefix Python commands with `uv run`
2. **Mock A2A SDK**: The real A2A SDK is not yet available, so `a2a_sdk.py` provides a mock implementation
3. **Simulated Agents**: In `demo_simple.py`, multi-agent responses are simulated for educational purposes
4. **Environment Variables**: Configure OMI connection and API keys in `.env.local`
5. **Educational Focus**: Code is optimized for learning, not production. Missing features like rate limiting and monitoring are intentional.