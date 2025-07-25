# 📋 Decision Registry

This document tracks all architectural decisions made for the NeuroHub (OMI + A2A Demo) project.

## Decision Summary

| ID | Date | Decision | Status | ADR |
|----|------|----------|--------|-----|
| D001 | 2024-01-10 | Use Google A2A Protocol for agent communication | ✅ Implemented | [ADR-001](docs/adr/001-use-a2a-protocol.md) |
| D002 | 2024-01-11 | Implement Gateway orchestration pattern | ✅ Implemented | [ADR-002](docs/adr/002-agent-orchestration-pattern.md) |
| D003 | 2024-01-11 | Use Docker for deployment | ✅ Implemented | [ADR-003](docs/adr/003-docker-deployment.md) |
| D004 | 2024-01-12 | WebSocket for OMI integration | ✅ Implemented | [ADR-004](docs/adr/004-websocket-omi-integration.md) |
| D005 | 2024-01-12 | Context analysis via LLM | ✅ Implemented | [ADR-005](docs/adr/005-llm-context-analysis.md) |
| D006 | 2024-01-13 | AgentDB for persistence | ⚠️ Partial | [ADR-006](docs/adr/006-agentdb-integration.md) |
| D007 | 2024-01-14 | UV package manager adoption | ✅ Implemented | [ADR-007](docs/adr/007-uv-package-manager.md) |
| D008 | 2024-01-15 | Cloud deployment for workshops | ✅ Implemented | [ADR-008](docs/adr/008-cloud-deployment.md) |
| D009 | 2024-01-15 | Simplified demo for education | ✅ Implemented | [ADR-009](docs/adr/009-simplified-demo.md) |
| D010 | 2025-01-25 | OMI-Mem0 memory integration | ✅ Implemented | [ADR-010](docs/adr/010-memory-integration.md) |
| D011 | 2025-01-25 | Three Layer IA alignment | ✅ Implemented | [ADR-011](docs/adr/011-three-layer-ia-alignment.md) |

## Decision Details

### D001: Use Google A2A Protocol
- **Context**: Need standardized agent communication
- **Decision**: Adopt A2A protocol
- **Consequences**: Interoperability with future A2A agents
- **Status**: Fully implemented with mock SDK

### D002: Gateway Orchestration Pattern
- **Context**: Multiple agents need coordination
- **Decision**: Central gateway manages workflows
- **Consequences**: Single point of control, easier debugging
- **Status**: Fully implemented

### D003: Docker Deployment
- **Context**: Need consistent deployment across environments
- **Decision**: Each agent in separate container
- **Consequences**: Resource overhead, but great isolation
- **Status**: Docker Compose implemented

### D004: WebSocket for OMI Integration
- **Context**: Real-time audio streaming from OMI
- **Decision**: WebSocket for bidirectional communication
- **Consequences**: More complex than REST, but necessary for real-time
- **Status**: Implemented in gateway

### D005: LLM Context Analysis
- **Context**: Need to understand conversation intent
- **Decision**: Use LLM for flexible analysis
- **Consequences**: API costs, but much more flexible
- **Status**: OpenAI integration complete

### D006: AgentDB Integration
- **Context**: Need persistent storage for agent data
- **Decision**: Use AgentDB for vector storage
- **Consequences**: External dependency
- **Status**: Mock implementation only

### D007: UV Package Manager
- **Context**: pip is slow for workshops
- **Decision**: Use UV for faster installs
- **Consequences**: Additional tool to learn
- **Status**: Fully adopted

### D008: Cloud Deployment for Workshops
- **Context**: Docker setup too complex for students
- **Decision**: Pre-deploy backend to cloud
- **Consequences**: Internet dependency, but much simpler
- **Status**: Fly.io deployment ready

### D009: Simplified Demo
- **Context**: Full multi-agent system too complex for teaching
- **Decision**: Create demo_simple.py with simulated agents
- **Consequences**: Less realistic, but better for learning
- **Status**: Primary demo path

### D010: OMI-Mem0 Memory Integration
- **Context**: Need persistent memory storage for workshop teams
- **Decision**: Integrate OMI memories with Mem0 platform
- **Consequences**: Enhanced AI capabilities, optional dependency
- **Status**: Fully implemented with fallback

### D011: Three Layer IA Alignment
- **Context**: Need comprehensive information architecture
- **Decision**: Align agents with Semantic/Kinetic/Dynamic layers
- **Consequences**: Clear boundaries, better scalability
- **Status**: Architecture documented and aligned

## Decision Process

1. **Identify Need**: Problem or opportunity arises
2. **Document Context**: Create ADR with context
3. **Evaluate Options**: List alternatives
4. **Make Decision**: Choose with rationale
5. **Record Consequences**: Expected outcomes
6. **Implement**: Update code and docs
7. **Review**: Update status after implementation

## Pending Decisions

| Question | Priority | Target Date |
|----------|----------|-------------|
| Move from mock A2A to real SDK? | Low | When available |
| Add more agent types? | Medium | Based on feedback |
| Kubernetes deployment? | Low | If needed |
| Production monitoring? | Medium | For real deployments |

## Superseded Decisions

| Original | Superseded By | Reason |
|----------|---------------|---------|
| Full AgentDB integration | Mock implementation | AgentDB SDK not ready |
| Local Docker requirement | Cloud deployment | Too complex for students |
| AgentDB for workshop persistence | Mem0 integration | AgentDB API issues, Mem0 better fit |

## Related Documents

- [Architecture Overview](docs/architecture/README.md)
- [C4 Diagrams](docs/architecture/c4-diagrams.md)
- [ADR Template](docs/adr/template.md)
- [TODO List](TODO.md)

---

*Last Updated: 2025-01-25*