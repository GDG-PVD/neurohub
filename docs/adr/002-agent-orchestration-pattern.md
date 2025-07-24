# ADR-002: Gateway Agent as Central Orchestrator

**Date:** 2025-07-24

**Status:** Accepted

**Deciders:** Development Team, AI Architecture Lead

**Tags:** architecture, patterns, orchestration

## Context

In a multi-agent system processing OMI conversations, we need to coordinate multiple specialized agents (context analysis, action planning, knowledge retrieval, etc.). Key challenges:

- OMI device should have a single connection point
- Agents need to be coordinated in specific workflows
- Some tasks are sequential, others can be parallel
- Results need to be aggregated and returned to the client
- System should be extensible for new agents

## Decision

Implement a Gateway Agent pattern where the OMI Gateway Agent acts as the central orchestrator for all multi-agent workflows. All external communication goes through the gateway, which then coordinates internal agent interactions.

## Considered Options

1. **Gateway/Orchestrator Pattern**: Central agent manages all workflows
   - Pros:
     - Single entry point for clients
     - Clear workflow management
     - Easier debugging and monitoring
     - Can optimize agent calls (parallel vs sequential)
   - Cons:
     - Gateway becomes a potential bottleneck
     - More complex gateway implementation
     - Single point of failure

2. **Peer-to-Peer Mesh**: Agents communicate directly with each other
   - Pros:
     - No central bottleneck
     - Agents can optimize their own interactions
     - More resilient to single failures
   - Cons:
     - Complex routing and discovery
     - Difficult to track workflows
     - Each agent needs to know about others
     - Hard to implement consistent error handling

3. **Event-Driven/Pub-Sub**: Agents react to events on a message bus
   - Pros:
     - Loose coupling between agents
     - Easy to add new agents
     - Natural async processing
   - Cons:
     - Hard to implement sequential workflows
     - Complex debugging of event chains
     - Need additional message broker infrastructure

## Consequences

### Positive
- Clear, understandable architecture
- OMI integration is simplified (single WebSocket connection)
- Workflows can be defined declaratively
- Easy to add authentication/rate limiting at gateway
- Natural place for logging and monitoring

### Negative
- Gateway agent is more complex than other agents
- All traffic flows through gateway (potential bottleneck)
- Gateway failure affects entire system

### Neutral
- Need to implement workflow engine in gateway
- Gateway maintains WebSocket connections
- Other agents can focus on their specific tasks

## Implementation Notes

```python
# Workflow definition in gateway
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

results = await orchestrator.execute_workflow(workflow)
```

## References

- [Gateway Pattern in Microservices](https://microservices.io/patterns/apigateway.html)
- [ADR-001: A2A Protocol Choice](001-use-a2a-protocol.md)
- [Orchestration vs Choreography](https://stackoverflow.com/questions/4127241/orchestration-vs-choreography)

## Notes

The gateway pattern aligns well with A2A protocol's task-based communication model. This decision simplifies the initial implementation while keeping the door open for more sophisticated patterns later.