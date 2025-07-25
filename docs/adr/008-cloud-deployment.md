# ADR-008: Cloud Deployment for Workshops

## Status
Accepted

## Context
Running workshops with Docker requirements has proven problematic:
- Students spend 30+ minutes installing Docker
- Docker Desktop licensing concerns
- Different behavior across OS platforms
- Network/firewall issues in classroom settings
- Limited time for actual learning

We need a simpler deployment strategy for educational workshops.

## Decision
We will pre-deploy the OMI MCP backend to cloud platforms (primarily Fly.io) for workshops, allowing students to connect to a shared backend without local Docker requirements.

## Consequences

### Positive
- Student setup time reduced from 30+ minutes to 5 minutes
- No Docker installation required
- Consistent environment for all students
- Focus on AI concepts instead of DevOps
- Works on any device with internet
- Instructor can monitor usage centrally

### Negative
- Requires internet connection
- Shared API keys (less secure)
- Cloud hosting costs (minimal with free tiers)
- Single point of failure
- Less realistic than local deployment

### Neutral
- Different from production deployment patterns
- Requires pre-workshop setup by instructor

## Implementation
1. Created `workshop_deploy.sh` for one-click deployment
2. Added cloud configuration to documentation
3. Updated student guides to use cloud backend
4. Created monitoring scripts for instructors

## Alternatives Considered
1. **Pre-configured VMs**: Too resource intensive
2. **Codespaces/GitPod**: Good but requires accounts
3. **Local binary**: Would need multi-platform builds
4. **Keep Docker**: Original approach, too many issues

## Related
- [ADR-003: Docker Deployment](003-docker-deployment.md) - Original approach
- [ADR-009: Simplified Demo](009-simplified-demo.md) - Complementary simplification
- [Backend Hosting Guide](../../BACKEND_HOSTING_GUIDE.md)
- [Workshop Deployment Guide](../../WORKSHOP_DEPLOYMENT_GUIDE.md)