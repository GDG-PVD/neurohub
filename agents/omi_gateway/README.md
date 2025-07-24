# OMI Gateway Agent

## Overview

The Gateway Agent is the central orchestrator of the OMI A2A Multi-Agent System. It serves as the single entry point for OMI devices and coordinates all multi-agent workflows.

## Responsibilities

1. **WebSocket Management**: Maintains real-time connections with OMI devices
2. **Workflow Orchestration**: Coordinates sequential and parallel agent tasks
3. **Result Aggregation**: Combines outputs from multiple agents
4. **Error Handling**: Manages failures and retries across the system
5. **Client Updates**: Broadcasts real-time status updates

## API Endpoints

### WebSocket: `/ws`
Real-time bidirectional communication with OMI devices.

**Message Types:**
- `audio`: Raw audio data for processing
- `transcript`: Pre-transcribed text for analysis

**Example:**
```json
{
  "type": "transcript",
  "transcript": "Meeting discussion text...",
  "metadata": {
    "user_id": "user123",
    "session_id": "session456"
  }
}
```

### HTTP: `/health`
Health check endpoint returning agent status.

## A2A Capabilities

The Gateway exposes these A2A capabilities:

1. **process_conversation**: Main conversation processing workflow
2. **stream_audio**: Real-time audio streaming support
3. **get_status**: Current agent statistics

See [agent_card.json](agent_card.json) for full capability definitions.

## Configuration

Environment variables:
- `GATEWAY_AGENT_PORT`: HTTP/WebSocket port (default: 8001)
- `OMI_API_URL`: OMI backend URL
- `OMI_API_KEY`: Authentication key
- `A2A_AGENT_PORT`: A2A protocol port (default: 8000)

## Workflow Management

The Gateway uses a declarative workflow system:

```python
workflow = [
    {
        "agent": "context-analysis",
        "task": "analyze_context",
        "data": {"transcript": transcript},
        "save_to_context": "context_analysis"
    },
    {
        "agent": "action-planning",
        "task": "extract_actions",
        "use_context": True,
        "save_to_context": "actions"
    }
]
```

## Development

```bash
# Run standalone
python -m agents.omi_gateway.agent

# Run with Docker
docker build -t omi-gateway -f agents/omi_gateway/Dockerfile .
docker run -p 8001:8000 omi-gateway
```

## Architecture Notes

- Uses FastAPI for WebSocket and HTTP handling
- Implements A2A protocol via base `A2AAgent` class
- Maintains WebSocket client registry for broadcasts
- Orchestrator handles both sequential and parallel workflows

## Related Documentation

- [Architecture Overview](../../docs/architecture/README.md)
- [ADR-002: Gateway Pattern](../../docs/adr/002-agent-orchestration-pattern.md)
- [A2A Protocol Integration](../../core/README.md)