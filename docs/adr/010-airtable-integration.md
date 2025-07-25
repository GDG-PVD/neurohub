# ADR-010: Airtable Integration via MCP

## Status
Accepted

## Context
NeuroHub needs a persistent data layer to store:
- Conversation summaries from OMI device
- Extracted action items with deadlines
- Knowledge base entries for future reference
- Agent collaboration history

We needed a solution that was:
- Easy to set up for workshops
- Provides instant visual interface
- Supports real-time collaboration
- Accessible via API

## Decision
We will use Airtable as our primary data persistence layer, accessed through the Model Context Protocol (MCP) server architecture. This provides:
1. Zero-setup database (cloud-based)
2. Visual interface for non-technical users
3. API access for programmatic interaction
4. MCP server integration for Claude Desktop

## Consequences

### Positive
- **Instant visualization**: Data immediately viewable in Airtable's UI
- **No database setup**: Students don't need to configure databases
- **Rich features**: Filtering, sorting, views built-in
- **Collaboration**: Multiple users can view/edit simultaneously
- **MCP integration**: Works seamlessly with Claude Desktop

### Negative
- **Vendor lock-in**: Tied to Airtable's service
- **API limits**: Subject to rate limiting
- **Cost at scale**: Free tier has limitations
- **Schema flexibility**: Less flexible than traditional databases

### Neutral
- Requires API key management
- Data residency depends on Airtable's infrastructure
- Integration through simulated MCP calls in Python

## Implementation
1. Created `integrations/airtable_connector.py` for Python access
2. Defined schema for Conversations, Actions, and Knowledge tables
3. Integrated with OMI Gateway agent for automatic data storage
4. Created MCP server configuration for Claude Desktop
5. Added comprehensive testing and examples

## Schema Design
```
Conversations
├── conversation_id (Primary)
├── timestamp
├── summary
├── participants
├── topics
└── agent_analysis

Actions
├── action_id (Primary)
├── conversation_id (Link)
├── action_item
├── deadline
├── assignee
└── status

Knowledge
├── knowledge_id (Primary)
├── topic
├── content
├── source_conversation (Link)
├── tags
└── created_at
```

## Related ADRs
- [ADR-006: AgentDB Integration](006-agentdb-integration.md) - Alternative persistence approach
- [ADR-009: Cloud-First Architecture](009-cloud-first-architecture.md) - Enables cloud services
- [ADR-001: Use A2A Protocol](001-use-a2a-protocol.md) - Data flow architecture