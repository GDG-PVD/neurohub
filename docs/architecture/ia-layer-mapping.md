# Three Layer IA - Agent Mapping

This document visualizes how NeuroHub agents and components map to the Three Layer Information Architecture.

## Layer Overview

```mermaid
graph TB
    %% Styling
    classDef semantic fill:#e8f5e9,stroke:#4caf50,color:#1b5e20
    classDef kinetic fill:#e3f2fd,stroke:#2196f3,color:#0d47a1
    classDef dynamic fill:#fce4ec,stroke:#e91e63,color:#880e4f
    classDef external fill:#f5f5f5,stroke:#9e9e9e,color:#424242
    
    %% External Systems
    OMI[OMI Device]:::external
    Mem0[Mem0 Platform]:::external
    External[External Services]:::external
    
    %% Layers
    subgraph Dynamic["Dynamic Layer (Evolution & Learning)"]
        MemEvolution[Memory Evolution]:::dynamic
        TeamLearning[Workshop Teams]:::dynamic
        Patterns[Pattern Recognition]:::dynamic
        Personalization[User Adaptation]:::dynamic
    end
    
    subgraph Kinetic["Kinetic Layer (Process & Movement)"]
        Gateway[Gateway Agent]:::kinetic
        Action[Action Planning Agent]:::kinetic
        Comm[Communication Agent]:::kinetic
        Workflow[A2A Orchestration]:::kinetic
    end
    
    subgraph Semantic["Semantic Layer (Base Reality)"]
        Context[Context Analysis Agent]:::kinetic
        Knowledge[Knowledge Agent]:::kinetic
        MemBridge[Memory Bridge]:::kinetic
        Entities[Entity Extraction]:::kinetic
    end
    
    %% Connections
    OMI --> Gateway
    Gateway --> Context
    Gateway --> Action
    Gateway --> Comm
    Context --> MemBridge
    Knowledge --> MemBridge
    MemBridge --> Mem0
    Action --> External
    Comm --> External
    
    %% Cross-layer connections
    MemBridge --> MemEvolution
    Gateway --> Workflow
    Context --> Patterns
    Knowledge --> TeamLearning
    Workflow --> Personalization
```

## Detailed Agent Mapping

### Semantic Layer Agents

| Agent/Component | Purpose | Key Responsibilities |
|----------------|---------|---------------------|
| **Context Analysis Agent** | Extract meaning from conversations | - Topic identification<br>- Sentiment analysis<br>- Intent recognition<br>- Entity extraction |
| **Knowledge Agent** | Store and retrieve information | - Vector storage<br>- Information retrieval<br>- Knowledge graphs<br>- Fact extraction |
| **Memory Bridge** | Structure memories for storage | - OMI memory conversion<br>- Mem0 format mapping<br>- Metadata enrichment |

### Kinetic Layer Agents

| Agent/Component | Purpose | Key Responsibilities |
|----------------|---------|---------------------|
| **Gateway Agent** | Orchestrate all workflows | - WebSocket management<br>- Agent coordination<br>- Result aggregation<br>- Error handling |
| **Action Planning Agent** | Track temporal sequences | - Action extraction<br>- Deadline management<br>- Priority assignment<br>- Task dependencies |
| **Communication Agent** | Execute external actions | - Email sending<br>- Calendar integration<br>- Notification dispatch<br>- API interactions |

### Dynamic Layer Components

| Component | Purpose | Key Responsibilities |
|-----------|---------|---------------------|
| **Mem0 Integration** | Enable memory persistence | - Long-term storage<br>- Memory evolution<br>- Cross-session context |
| **Workshop Teams** | Collective learning | - Team memory sharing<br>- Collaborative insights<br>- Group patterns |
| **Pattern Recognition** | Identify emerging insights | - Conversation trends<br>- Behavioral patterns<br>- Predictive modeling |

## Data Flow Between Layers

```mermaid
sequenceDiagram
    participant User
    participant Semantic
    participant Kinetic
    participant Dynamic
    
    User->>Kinetic: Audio/Commands
    Kinetic->>Semantic: Raw Data
    Semantic->>Semantic: Extract Meaning
    Semantic->>Kinetic: Structured Knowledge
    Kinetic->>Kinetic: Orchestrate Actions
    Kinetic->>Dynamic: Process Results
    Dynamic->>Dynamic: Learn & Adapt
    Dynamic->>Kinetic: Updated Models
    Kinetic->>User: Personalized Response
```

## Implementation Guidelines

### Creating New Agents

When creating new agents, identify which layer they belong to:

1. **Semantic Layer**: Focus on data extraction and structuring
   ```python
   class NewSemanticAgent(A2AAgent):
       layer = "semantic"
       # Extract, structure, enrich data
   ```

2. **Kinetic Layer**: Focus on process and coordination
   ```python
   class NewKineticAgent(A2AAgent):
       layer = "kinetic"
       # Orchestrate, route, execute
   ```

3. **Dynamic Layer**: Focus on learning and adaptation
   ```python
   class NewDynamicComponent:
       layer = "dynamic"
       # Learn, evolve, personalize
   ```

### Cross-Layer Communication

- **Upward**: Semantic → Kinetic → Dynamic (data enrichment)
- **Downward**: Dynamic → Kinetic → Semantic (model updates)
- **Lateral**: Within same layer only for specific workflows

## Benefits of This Architecture

1. **Clear Boundaries**: Each agent knows its role and scope
2. **Scalability**: Layers can scale independently
3. **Maintainability**: Changes isolated to specific layers
4. **Extensibility**: New capabilities map to clear locations
5. **Testability**: Layer interfaces enable focused testing

## References

- [Three Layer IA Principles](/Users/stephenszermer/Documents/Project Knowledge/Three Layer IA.md)
- [ADR-011: Three Layer IA Alignment](../adr/011-three-layer-ia-alignment.md)
- [Architecture Overview](README.md)
- [C4 Diagrams](c4-diagrams.md)