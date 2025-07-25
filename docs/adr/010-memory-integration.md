# ADR-010: Memory Integration with OMI and Mem0

## Status
Accepted

## Context
The NeuroHub workshop needed a way to demonstrate persistent memory capabilities in AI systems. Teams using OMI devices capture conversations as "memories," and we wanted to showcase how these memories can be:
- Stored persistently across sessions
- Searched semantically
- Used to provide context to AI agents
- Analyzed for patterns and insights

Both OMI and Mem0 use the concept of "memories," making them a natural fit for integration.

## Decision
We will integrate OMI device memories with Mem0's AI memory platform through a Memory Bridge component that:
1. Syncs OMI memories to Mem0 for persistent storage
2. Provides unified search across both systems
3. Enables memory analysis and insights extraction
4. Allows AI agents to access relevant memories for context

## Consequences

### Positive
- **Educational Value**: Students learn about production-ready memory systems
- **Real Integration**: Demonstrates hardware-software integration
- **Persistent Context**: Conversations persist across workshop sessions
- **Enhanced AI**: Agents provide better responses using memory context
- **Scalability**: Mem0 handles storage and search efficiently

### Negative
- **Additional Dependency**: Requires Mem0 API key for full features
- **Complexity**: Adds another layer to the system
- **API Limits**: Subject to Mem0's rate limits and quotas

### Neutral
- Memory features are optional - system works without Mem0
- Can fall back to in-memory storage if needed
- Requires explicit user consent for memory storage

## Implementation
- Created `integrations/memory_bridge.py` for OMI-Mem0 integration
- Enhanced workshop server with memory endpoints
- Updated dashboard with Memory Lab features
- Documented in `docs/MEMORY_INTEGRATION.md`

## Related ADRs
- [ADR-004: WebSocket OMI Integration](004-websocket-omi-integration.md) - Defines how we capture memories
- [ADR-009: Simplified Demo](009-simplified-demo.md) - Memory features complement the simple demo
- [ADR-011: Three Layer IA](011-three-layer-ia-alignment.md) - Memory spans Semantic and Dynamic layers