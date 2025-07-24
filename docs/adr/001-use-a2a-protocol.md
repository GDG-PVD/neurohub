# ADR-001: Use Google A2A Protocol for Multi-Agent Communication

**Date:** 2025-07-24

**Status:** Accepted

**Deciders:** Development Team, AI Architecture Lead

**Tags:** architecture, integration, protocols, ai-generated

## Context

The OMI project needs to demonstrate multi-agent AI capabilities where different specialized agents collaborate to process conversations from the OMI wearable device. We need a standardized way for these agents to:

- Discover each other's capabilities
- Communicate tasks and results
- Handle both synchronous and asynchronous interactions
- Support different data types (text, audio, JSON)

Google recently released the Agent2Agent (A2A) protocol (April 2025) with backing from 50+ major tech companies. This open standard is designed specifically for agent interoperability.

## Decision

We will adopt Google's A2A protocol as the communication standard for all agents in the OMI multi-agent demo system.

## Considered Options

1. **Google A2A Protocol**: Industry-backed standard for agent communication
   - Pros: 
     - Industry standard with growing adoption
     - Well-documented with official SDKs
     - Supports discovery, sync/async, and streaming
     - Compatible with existing JSON-RPC standards
   - Cons: 
     - Relatively new (v1.0 released 2025)
     - May have breaking changes as it evolves
     - Requires learning new protocol specifics

2. **Custom REST/WebSocket Protocol**: Build our own communication layer
   - Pros: 
     - Full control over implementation
     - Can optimize for OMI-specific needs
     - No external dependencies
   - Cons: 
     - Significant development effort
     - No interoperability with other systems
     - Need to solve discovery, routing, etc. from scratch

3. **MCP (Model Context Protocol)**: Anthropic's protocol for LLM tools
   - Pros: 
     - Good for LLM-tool interactions
     - Simpler protocol
     - Already used in OMI backend
   - Cons: 
     - Designed for tools, not agent-to-agent communication
     - Limited to synchronous interactions
     - No built-in agent discovery

## Consequences

### Positive
- Agents can be developed independently and still interoperate
- Built-in agent discovery via `.well-known/agent.json`
- Support for streaming real-time data (important for audio)
- Can potentially integrate with other A2A-compliant systems
- Good documentation and SDK support

### Negative
- Learning curve for the development team
- Dependency on external protocol evolution
- May be overkill for simple demo scenarios

### Neutral
- Need to wrap A2A SDK for our specific use cases
- Each agent needs to expose standard A2A endpoints
- Requires HTTP server for each agent

## Implementation Notes

```python
# Example A2A agent setup
from a2a_sdk import A2AClient, AgentCard

class OmiGatewayAgent(A2AAgent):
    def __init__(self):
        super().__init__(
            agent_id="omi-gateway",
            name="OMI Conversation Gateway",
            capabilities=[...]
        )
```

## References

- [A2A Protocol Specification](https://github.com/google-a2a/A2A)
- [A2A Python SDK Documentation](https://pypi.org/project/a2a-sdk/)
- [Google's A2A Announcement Blog](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/)

## Notes

This decision was made with AI assistance (Claude) during the initial architecture design phase. The AI helped research A2A capabilities and compare it with alternatives based on project requirements.