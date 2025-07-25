# Architecture Documentation

## Overview

The OMI A2A Multi-Agent System demonstrates how multiple AI agents can collaborate to process conversations from OMI wearable devices. The system uses Google's A2A (Agent2Agent) protocol for standardized inter-agent communication.

## Key Components

### Agents

1. **[Gateway Agent](../../agents/omi_gateway/README.md)**
   - Central orchestrator for all workflows
   - WebSocket connection to OMI devices
   - Routes tasks to specialized agents
   - Aggregates results

2. **[Context Analysis Agent](../../agents/context_analysis/README.md)**
   - Analyzes conversation context
   - Extracts topics, sentiment, and intent
   - Uses GPT-4 for understanding

3. **[Action Planning Agent](../../agents/action_planning/README.md)**
   - Extracts actionable items from conversations
   - Creates task lists with assignees and deadlines
   - Prioritizes actions

4. **[Knowledge Agent](../../agents/knowledge/README.md)**
   - Information retrieval and search
   - RAG (Retrieval Augmented Generation)
   - Documentation lookup

5. **[Communication Agent](../../agents/communication/README.md)**
   - Sends emails and notifications
   - Manages external communications
   - Multi-channel messaging

### Core Infrastructure

- **[A2A Client](../../core/README.md)**: Wrapper around Google's A2A SDK
- **[OMI Connector](../../integrations/README.md)**: Integration with OMI backend
- **Redis Cache**: For temporary data and pub/sub

## Architecture Diagrams

- **[C4 Diagrams](c4-diagrams.md)**: System context, containers, and components
- **[Sequence Diagrams](sequence-diagrams.md)**: Key interaction flows
- **[Data Flow](data-flow.md)**: How data moves through the system

## Information Architecture

The system follows a Three Layer Information Architecture approach that organizes complexity while preserving context:

### Semantic Layer (Base Reality)
Captures fundamental knowledge units and relationships:
- **Agents**: Context Analysis, Knowledge Agent
- **Function**: Extract meaning from raw conversation data
- **Data**: Entities, topics, memories, relationships

### Kinetic Layer (Process & Movement)
Documents how data flows and processes interact:
- **Agents**: Gateway Agent, Action Planning, Communication
- **Function**: Orchestrate workflows and temporal sequences
- **Data**: Actions, deadlines, message routing

### Dynamic Layer (Evolution & Learning)
Enables system adaptation and learning over time:
- **Integration**: Mem0 platform, Workshop teams
- **Function**: Memory evolution, pattern recognition
- **Data**: Historical context, personalization

See [ADR-011](../adr/011-three-layer-ia-alignment.md) for detailed architecture mapping.

## Design Principles

1. **Separation of Concerns**: Each agent has a single, well-defined responsibility
2. **Loose Coupling**: Agents communicate only through A2A protocol
3. **Scalability**: Agents can be scaled independently
4. **Extensibility**: New agents can be added without modifying existing ones
5. **Resilience**: System continues functioning if individual agents fail
6. **Layered Architecture**: Clear boundaries between semantic, kinetic, and dynamic concerns

## Technology Stack

- **Language**: Python 3.11+
- **Framework**: FastAPI for HTTP/WebSocket servers
- **Protocol**: Google A2A (Agent2Agent)
- **AI/ML**: OpenAI GPT-4, LangChain
- **Deployment**: Docker + Docker Compose
- **Caching**: Redis

## Related Documentation

- [Architecture Decision Records](../adr/README.md)
- [API Documentation](../api/README.md)
- [Deployment Guide](../guides/deployment.md)
- [Development Guide](../guides/development.md)