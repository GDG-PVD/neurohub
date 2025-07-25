# ADR-009: Cloud-First Architecture

## Status
Accepted

## Context
The original NeuroHub design required Docker Desktop for running the OMI MCP server locally. This created friction for:
- Workshop participants who may not have Docker installed
- Quick demonstrations and prototyping
- Cross-platform compatibility issues
- Resource constraints on development machines

Additionally, we integrated Airtable as a cloud-based data persistence layer, requiring a cloud-first approach for seamless integration.

## Decision
We will adopt a cloud-first architecture where:
1. The OMI backend runs on a cloud service (currently https://neurohub-workshop.fly.dev)
2. All services prioritize cloud endpoints over local deployment
3. Local Docker deployment becomes optional, not required
4. Airtable serves as the primary data persistence layer

## Consequences

### Positive
- **Zero local setup**: Students can start immediately without Docker
- **Platform agnostic**: Works on any OS with Python
- **Simplified deployment**: No container management required
- **Better reliability**: Cloud services handle uptime and scaling
- **Integrated data layer**: Airtable provides instant persistence and visualization

### Negative
- **Internet dependency**: Requires stable internet connection
- **Potential latency**: Cloud services may have higher latency than local
- **API rate limits**: Subject to cloud service rate limiting
- **Cost considerations**: Cloud services may incur costs at scale

### Neutral
- Configuration now uses environment variables pointing to cloud services
- Documentation updated to prioritize cloud setup
- Local development still possible but not the default path

## Implementation
1. Updated `.env.local` to use cloud endpoints by default
2. Modified `config/settings.py` to support both URL environment variables
3. Created cloud-specific documentation (`CLOUD_QUICK_START.md`)
4. Removed Docker as a hard requirement
5. Integrated Airtable MCP server for data persistence

## Related ADRs
- [ADR-006: AgentDB Integration](006-agentdb-integration.md) - Cloud database choice
- [ADR-008: Cloud Deployment](008-cloud-deployment.md) - Deployment strategy
- [ADR-010: Airtable Integration](010-airtable-integration.md) - Data persistence layer