# Architecture Decision Records

## Decision Registry

| ID | Title | Date | Status | Tags | Summary |
|----|-------|------|--------|------|----------|
| [ADR-001](001-use-a2a-protocol.md) | Use Google A2A Protocol for Multi-Agent Communication | 2025-07-24 | Accepted | architecture, integration | Adopt A2A as the standard for agent-to-agent communication |
| [ADR-002](002-agent-orchestration-pattern.md) | Gateway Agent as Central Orchestrator | 2025-07-24 | Accepted | architecture, patterns | Use gateway pattern for coordinating multi-agent workflows |
| [ADR-003](003-docker-deployment.md) | Docker-based Agent Deployment | 2025-07-24 | Accepted | infrastructure, deployment | Deploy each agent as an independent Docker container |
| [ADR-004](004-websocket-omi-integration.md) | WebSocket for Real-time OMI Integration | 2025-07-24 | Accepted | integration, real-time | Use WebSocket for streaming audio/transcript data from OMI |
| [ADR-005](005-llm-context-analysis.md) | LLM-based Context Analysis | 2025-07-24 | Accepted | ai, architecture | Use GPT-4 for conversation analysis and intent extraction |
| [ADR-006](006-agentdb-integration.md) | Integrate AgentDB for Multi-Agent Data Persistence | 2025-07-24 | Accepted | data-persistence, architecture, agent-state | Use AgentDB for isolated agent and conversation storage |
| [ADR-007](007-uv-package-manager.md) | Adopt UV as Package Manager | 2025-07-24 | Accepted | tooling, development, dependencies | Use UV for fast Python package management |
| [ADR-008](008-cloud-deployment.md) | Cloud Deployment for Workshops | 2025-07-25 | Accepted | deployment, education | Pre-deploy backend to cloud for simplified workshop setup |
| [ADR-009](009-simplified-demo.md) | Simplified Demo for Education | 2025-07-25 | Accepted | education, architecture | Create single-file demo that simulates multi-agent behavior |
| [ADR-010](010-memory-integration.md) | Memory Integration with OMI and Mem0 | 2025-01-25 | Accepted | integration, memory, ai | Integrate OMI memories with Mem0 AI memory platform |
| [ADR-011](011-three-layer-ia-alignment.md) | Three Layer Information Architecture | 2025-01-25 | Accepted | architecture, design | Align agents with Semantic/Kinetic/Dynamic layers |
| [ADR-012](012-neuro-agent-extensions.md) | Neurological Health Agent Extensions | 2025-01-25 | Proposed | agents, health, education | Create specialized neuro-focused agents for brain health |

## About ADRs

Architecture Decision Records (ADRs) capture important architectural decisions made during the project. Each ADR documents:

- **Context**: Why the decision was needed
- **Decision**: What was decided
- **Options**: What alternatives were considered
- **Consequences**: The implications of the decision

## Creating New ADRs

1. Copy the [template](template.md) to a new file: `XXX-short-title.md`
2. Fill in all sections
3. Add entry to the registry above
4. Submit PR for review

## Status Definitions

- **Proposed**: Decision is under consideration
- **Accepted**: Decision has been approved and implemented
- **Deprecated**: Decision is no longer recommended
- **Superseded**: Replaced by another ADR (link to new one)