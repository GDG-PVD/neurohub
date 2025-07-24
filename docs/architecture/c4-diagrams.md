# C4 Architecture Diagrams

This document contains the C4 model diagrams for the OMI A2A Multi-Agent System.

## Level 1: System Context

Shows the OMI Multi-Agent System and its relationships with users and external systems.

```mermaid
graph TB
    %% Styling
    classDef person fill:#08427b,stroke:#073b6f,color:#fff
    classDef system fill:#1168bd,stroke:#0d5aa7,color:#fff
    classDef external fill:#999,stroke:#666,color:#fff
    
    %% Nodes
    User[User with OMI Device]:::person
    System[OMI Multi-Agent System]:::system
    OMIBackend[OMI Backend API]:::external
    OpenAI[OpenAI API]:::external
    ExtServices[External Services<br/>Email, Calendar, etc.]:::external
    
    %% Relationships
    User -->|Audio/Commands| System
    System -->|Results/Actions| User
    System -->|User Data/Memories| OMIBackend
    System -->|LLM Requests| OpenAI
    System -->|Actions| ExtServices
```

## Level 2: Container Diagram

Shows the high-level containers (applications/services) within the system.

```mermaid
graph TB
    %% Styling
    classDef person fill:#08427b,stroke:#073b6f,color:#fff
    classDef container fill:#1168bd,stroke:#0d5aa7,color:#fff
    classDef db fill:#0d5aa7,stroke:#073b6f,color:#fff
    classDef external fill:#999,stroke:#666,color:#fff
    classDef agentdb fill:#00c896,stroke:#00a876,color:#fff
    
    %% External
    User[User with OMI Device]:::person
    OMIBackend[OMI Backend API]:::external
    AgentDB[AgentDB Cloud<br/>Serverless Database]:::agentdb
    
    %% Containers
    subgraph System[OMI Multi-Agent System]
        Gateway[Gateway Agent<br/>Python/FastAPI<br/>Port 8001]:::container
        Context[Context Analysis Agent<br/>Python/A2A<br/>Port 8002]:::container
        Action[Action Planning Agent<br/>Python/A2A<br/>Port 8003]:::container
        Knowledge[Knowledge Agent<br/>Python/A2A<br/>Port 8004]:::container
        Comm[Communication Agent<br/>Python/A2A<br/>Port 8005]:::container
        Redis[(Redis Cache)]:::db
    end
    
    %% Relationships
    User -->|WebSocket| Gateway
    Gateway -->|A2A Protocol| Context
    Gateway -->|A2A Protocol| Action
    Gateway -->|A2A Protocol| Knowledge
    Gateway -->|A2A Protocol| Comm
    Gateway -->|Cache| Redis
    Gateway -->|API Calls| OMIBackend
    
    %% AgentDB connections
    Context -->|Store/Query| AgentDB
    Action -->|Task History| AgentDB
    Knowledge -->|Vector Search| AgentDB
    Comm -->|Message Logs| AgentDB
    Gateway -->|Conversation DB| AgentDB
```

## Level 3: Component Diagram - Gateway Agent

Shows the internal components of the Gateway Agent.

```mermaid
graph TB
    %% Styling
    classDef component fill:#85bbf0,stroke:#5d99c6,color:#000
    classDef external fill:#999,stroke:#666,color:#fff
    
    %% External
    User[OMI Device]:::external
    Agents[Other A2A Agents]:::external
    
    %% Components
    subgraph Gateway[Gateway Agent]
        WS[WebSocket Handler]:::component
        A2A[A2A Client]:::component
        Orch[Orchestrator]:::component
        OMI[OMI Connector]:::component
        API[REST API]:::component
    end
    
    %% Relationships
    User -->|WebSocket| WS
    WS --> Orch
    Orch --> A2A
    A2A -->|A2A Protocol| Agents
    Orch --> OMI
    API --> Orch
```

## Level 4: Code - Orchestrator Workflow

Shows how the Orchestrator component processes a conversation.

```mermaid
sequenceDiagram
    participant WS as WebSocket
    participant O as Orchestrator
    participant CA as Context Agent
    participant AP as Action Agent
    participant C as Client
    
    WS->>O: process_conversation(transcript)
    O->>O: Define workflow
    
    %% Context Analysis
    O->>CA: analyze_context(transcript)
    CA-->>O: context_result
    
    %% Action Planning
    O->>AP: extract_actions(transcript, context)
    AP-->>O: actions_result
    
    %% Aggregate Results
    O->>O: Aggregate results
    O->>C: Broadcast updates
    O-->>WS: Return final results
```

## Deployment View

Shows how the system is deployed using Docker.

```mermaid
graph TB
    %% Styling
    classDef host fill:#e0e0e0,stroke:#999,color:#000
    classDef container fill:#1168bd,stroke:#0d5aa7,color:#fff
    classDef network fill:#d4e1f5,stroke:#a8c5e8,color:#000
    
    %% Infrastructure
    subgraph Host[Docker Host]:::host
        subgraph Network[a2a-network]:::network
            GW[omi-gateway:8001]:::container
            CA[context-agent:8002]:::container
            AP[action-agent:8003]:::container
            KN[knowledge-agent:8004]:::container
            CM[communication-agent:8005]:::container
            RD[(redis:6379)]:::container
        end
    end
    
    %% External connections
    Internet[Internet] --> Host
```

## Key Design Decisions

1. **Gateway Pattern**: All external communication flows through the gateway agent
2. **A2A Protocol**: Agents communicate using Google's A2A standard
3. **Docker Deployment**: Each agent runs in its own container
4. **WebSocket Integration**: Real-time communication with OMI devices
5. **Workflow Orchestration**: Gateway manages multi-agent workflows

## References

- [C4 Model](https://c4model.com/)
- [ADR-001: A2A Protocol](../adr/001-use-a2a-protocol.md)
- [ADR-002: Gateway Pattern](../adr/002-agent-orchestration-pattern.md)
- [ADR-003: Docker Deployment](../adr/003-docker-deployment.md)