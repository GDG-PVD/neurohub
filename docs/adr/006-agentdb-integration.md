# ADR-006: Integrate AgentDB for Multi-Agent Data Persistence

**Date:** 2025-07-24

**Status:** Proposed

**Deciders:** Development Team, AI Architecture Lead

**Tags:** data-persistence, architecture, agent-state, ai-generated

## Context

Our multi-agent system currently lacks persistent storage for:
- Agent-specific working memory and context
- Conversation analysis results
- Task execution history
- Inter-agent shared data
- User-specific agent customizations

AgentDB offers a unique approach designed specifically for AI applications:
- Instant database provisioning with just a UUID
- No configuration or setup required
- Built-in vector search for semantic queries
- MCP (Model Context Protocol) server support
- Pay-per-query pricing model
- Database isolation per agent/conversation

## Decision

Integrate AgentDB as the primary data persistence layer for our multi-agent system, with each agent and conversation getting its own isolated database.

## Considered Options

1. **AgentDB**: Purpose-built database system for AI agents
   - Pros:
     - Zero configuration - just generate UUID
     - Built-in vector search for RAG
     - MCP server integration
     - True data isolation per agent/conversation
     - Serverless pricing model
     - SQLite/DuckDB compatibility
   - Cons:
     - External dependency
     - Potential vendor lock-in
     - Network latency for queries
     - Limited to SQLite/DuckDB features

2. **Local SQLite + Pinecone**: Traditional approach
   - Pros:
     - Full control over data
     - No external dependencies
     - SQLite is battle-tested
   - Cons:
     - Need to manage database files
     - Separate vector DB setup
     - No built-in multi-tenancy
     - More complex deployment

3. **PostgreSQL with pgvector**: Single shared database
   - Pros:
     - Mature, full-featured RDBMS
     - Vector search via pgvector
     - Good performance
   - Cons:
     - Requires database server management
     - Complex multi-tenancy implementation
     - Higher operational overhead
     - Not designed for agent use cases

## Consequences

### Positive
- **Instant Provisioning**: Agents can create databases on-demand
- **Perfect Isolation**: Each conversation/agent gets its own DB
- **Vector Search**: Built-in RAG capabilities without extra setup
- **MCP Integration**: Agents can use databases as context sources
- **Cost Efficiency**: Only pay for actual usage
- **Compliance**: Easy data deletion per conversation

### Negative
- **Internet Dependency**: Requires network connection
- **Vendor Risk**: Dependency on AgentDB service availability
- **Limited Features**: Constrained to SQLite/DuckDB capabilities
- **Migration Complexity**: Moving away would require data export

### Neutral
- Need to implement AgentDB SDK integration
- Each agent needs database management logic
- Monitoring and quota management required

## Implementation Notes

### Per-Agent Database Pattern
```javascript
// Each agent gets its own persistent database
const agentDbToken = `agent-${agentId}-db`;
const agentDb = agentdb.connect(agentDbToken, "agent_memory", "sqlite");

// Store agent-specific data
await agentDb.execute({
  sql: `CREATE TABLE IF NOT EXISTS agent_state (
    key TEXT PRIMARY KEY,
    value JSON,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  )`
});
```

### Per-Conversation Database Pattern
```javascript
// Each conversation gets isolated storage
const convDbToken = `conv-${conversationId}`;
const convDb = agentdb.connect(convDbToken, "conversation", "sqlite");

// Store conversation context and results
await convDb.execute({
  sql: `CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY,
    role TEXT,
    content TEXT,
    embeddings BLOB,  -- For vector search
    metadata JSON,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  )`
});
```

### Use Cases in Our System

1. **Context Analysis Agent**: Store user profiles and conversation history
2. **Action Planning Agent**: Track task execution history and outcomes  
3. **Knowledge Agent**: Cache retrieved documents with embeddings
4. **Communication Agent**: Log sent messages and delivery status
5. **Gateway Agent**: Maintain conversation state and workflow progress

## References

- [AgentDB Documentation](https://agentdb.dev/)
- [AgentDB SDK](https://www.npmjs.com/package/@agentdb/sdk)
- [A2A Task State Management](../architecture/task-persistence.md)
- [ADR-002: Gateway Pattern](002-agent-orchestration-pattern.md)

## Notes

This decision aligns with the A2A protocol's task-based model where each task could have its own isolated database. The MCP server capability of AgentDB also provides an interesting integration path with our existing MCP support in OMI.