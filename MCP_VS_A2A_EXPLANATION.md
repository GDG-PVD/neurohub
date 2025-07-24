# 🔄 MCP vs A2A - Understanding the Difference

## Overview

This demo combines two different protocols to showcase the future of AI systems:

1. **MCP (Model Context Protocol)** - OMI's official API
2. **A2A (Agent-to-Agent Protocol)** - Multi-agent communication standard

## MCP (Model Context Protocol)

### What it is:
- OMI's official API for memory and conversation management
- Allows AI tools (like Claude) to interact with OMI device data
- Focuses on CRUD operations for memories and conversations

### Official MCP Tools:
- `get_memories` - Retrieve user memories
- `create_memory` - Create new memories
- `delete_memory` - Remove memories
- `edit_memory` - Update memory content
- `get_conversations` - Access conversation transcripts

### In Our Demo:
We use MCP to:
- Connect to the OMI backend
- Simulate conversation processing
- Demonstrate how OMI device data flows to AI systems

## A2A (Agent-to-Agent Protocol)

### What it is:
- A protocol for AI agents to communicate with each other
- Enables specialized agents to work together
- Not part of OMI's official system (our educational extension)

### Key Features:
- Agent discovery
- Capability announcement
- Task delegation
- Result aggregation

### In Our Demo:
We simulate A2A to show:
- How multiple agents could analyze OMI data
- Benefits of specialized AI agents
- Future possibilities for multi-agent systems

## How They Work Together

```
┌─────────────┐     MCP      ┌─────────────┐     A2A      ┌─────────────┐
│ OMI Device  │─────────────►│   Gateway   │─────────────►│   Agents    │
│             │              │   Agent     │              │  (Multiple) │
└─────────────┘              └─────────────┘              └─────────────┘
     Real                     Bridge between               Simulated for
   Hardware                    protocols                  demonstration
```

## For Students

### Real (MCP):
- OMI device → MCP Server → Your AI tool
- Official, production-ready
- Available today

### Educational (A2A):
- Shows future possibilities
- Demonstrates multi-agent concepts
- Not yet implemented in OMI

## Key Takeaway

This demo teaches two important concepts:
1. **How OMI works today** (MCP)
2. **How AI agents could work tomorrow** (A2A)

By combining both, students learn practical skills while exploring future possibilities in AI systems.