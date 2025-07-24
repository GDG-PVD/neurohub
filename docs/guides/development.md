# Development Guide

## Getting Started

### Prerequisites

- Python 3.11+
- Docker Desktop
- Git
- A code editor (VS Code recommended)

### Initial Setup

1. Clone the repository:
```bash
git clone <repo-url>
cd omi/a2a-demo
```

2. Install dependencies (UV recommended):

**Option A: Using UV (Faster)**
```bash
# Install UV if needed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Run setup script (auto-detects UV)
./setup.sh
```

**Option B: Using pip**
```bash
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
```

3. Configure environment:
```bash
cp .env.example .env.local
# Edit .env.local with your API keys
```

4. Start the system:
```bash
docker-compose up
```

## Project Structure

```
a2a-demo/
├── agents/              # Individual agents
│   ├── <agent_name>/
│   │   ├── agent.py     # Agent implementation
│   │   ├── agent_card.json  # A2A discovery
│   │   ├── Dockerfile   # Container definition
│   │   └── README.md    # Agent documentation
├── core/               # Shared libraries
├── integrations/       # External service connectors
├── docs/               # Documentation
└── demo/               # Demo scenarios
```

## Creating a New Agent

### 1. Create Agent Structure

```bash
mkdir -p agents/my_agent
cd agents/my_agent
```

### 2. Implement the Agent

Create `agent.py`:

```python
from core.a2a_client import A2AAgent, AgentCapability

class MyAgent(A2AAgent):
    def __init__(self):
        capabilities = [
            AgentCapability(
                name="my_capability",
                description="What this capability does",
                input_schema={...},
                output_schema={...}
            )
        ]
        
        super().__init__(
            agent_id="my-agent",
            name="My Agent",
            port=8006,
            capabilities=capabilities
        )
        
        # Register handlers
        self.register_handler("my_capability", self.handle_my_capability)
    
    async def handle_my_capability(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Implement capability logic
        return {"result": "processed"}
```

### 3. Create Agent Card

`agent_card.json`:
```json
{
  "agent_id": "my-agent",
  "name": "My Agent",
  "capabilities": [...],
  "interaction_modes": ["sync", "stream", "async"],
  "data_types": ["text", "structured_json"]
}
```

### 4. Add to Docker Compose

Update `docker-compose.yml`:
```yaml
my-agent:
  build:
    context: .
    dockerfile: agents/my_agent/Dockerfile
  ports:
    - "8006:8000"
  environment:
    - A2A_AGENT_PORT=8000
  networks:
    - a2a-network
```

## Development Workflow

### Local Development

1. **Activate virtual environment:**
```bash
source venv/bin/activate
```

2. **Run agent locally:**
```bash
python -m agents.my_agent.agent
```

3. **Test with curl:**
```bash
# Check agent card
curl http://localhost:8006/.well-known/agent.json

# Send task
curl -X POST http://localhost:8006/task \
  -H "Content-Type: application/json" \
  -d '{"type": "my_capability", "data": {...}}'
```

### Testing

```bash
# Run unit tests
pytest agents/my_agent/tests/

# Run integration tests
python demo/test_integration.py
```

### Code Quality

```bash
# Format code
black agents/my_agent/

# Lint
flake8 agents/my_agent/

# Type checking
mypy agents/my_agent/
```

## Best Practices

### 1. Agent Design

- **Single Responsibility**: Each agent should do one thing well
- **Stateless**: Agents should not maintain conversation state
- **Idempotent**: Same input should produce same output
- **Error Handling**: Always return structured errors

### 2. A2A Protocol

- Always implement agent discovery (`.well-known/agent.json`)
- Use proper HTTP status codes
- Include request IDs for tracing
- Implement health checks

### 3. Documentation

- Every agent needs a README.md
- Document all capabilities
- Include usage examples
- Update ADRs for design decisions

### 4. Testing

- Unit test individual handlers
- Integration test agent interactions
- Test error scenarios
- Validate agent cards

## Debugging

### View Agent Logs

```bash
# Single agent
docker logs a2a-demo_my-agent_1

# Follow logs
docker logs -f a2a-demo_my-agent_1

# All agents
docker-compose logs
```

### Common Issues

1. **Port conflicts**: Ensure each agent uses a unique port
2. **Network issues**: Verify agents are on same Docker network
3. **Discovery failures**: Check agent card JSON validity
4. **Task routing**: Verify agent IDs match in orchestrator

## Contributing

1. Create feature branch
2. Implement changes
3. Update documentation
4. Add tests
5. Submit PR with:
   - Description of changes
   - Link to relevant ADR (if applicable)
   - Test results

## Resources

- [A2A Protocol Spec](https://github.com/google-a2a/A2A)
- [Architecture Overview](../architecture/README.md)
- [ADR Template](../adr/template.md)
- [API Documentation](../api/README.md)