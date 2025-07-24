# ADR-003: Docker-based Agent Deployment

**Date:** 2025-07-24

**Status:** Accepted

**Deciders:** Development Team, DevOps Lead

**Tags:** infrastructure, deployment, docker, scalability

## Context

We need to deploy multiple independent agents (gateway, context analysis, action planning, etc.) for the OMI A2A demo. Requirements:

- Each agent should be independently deployable
- Easy local development and testing
- Consistent environment across development and demo
- Simple scaling if needed
- Quick setup for demos

## Decision

Deploy each agent as an independent Docker container, orchestrated with Docker Compose for local development and demos.

## Considered Options

1. **Docker + Docker Compose**: Containerized deployment
   - Pros:
     - Industry standard for microservices
     - Easy local development with docker-compose
     - Consistent environments
     - Each agent can have different dependencies
     - Simple networking between containers
   - Cons:
     - Requires Docker knowledge
     - Additional overhead vs direct execution
     - Need to manage container resources

2. **Single Python Application**: Monolithic deployment
   - Pros:
     - Simpler deployment (one process)
     - Easier debugging
     - No container overhead
   - Cons:
     - Dependency conflicts between agents
     - Can't scale agents independently
     - Harder to maintain separation of concerns
     - Single failure affects all agents

3. **Kubernetes**: Full orchestration platform
   - Pros:
     - Production-grade orchestration
     - Advanced scaling and health checks
     - Service discovery built-in
   - Cons:
     - Overkill for demo purposes
     - Complex setup and maintenance
     - Steep learning curve

## Consequences

### Positive
- Each agent has isolated environment
- Easy to add/remove agents
- Simple networking with Docker networks
- Can use different Python versions if needed
- Docker Compose provides easy multi-agent startup
- Portable across different host systems

### Negative
- Requires Docker Desktop installation
- Slightly more complex than running Python directly
- Need to manage Docker images and builds
- Container startup time adds latency

### Neutral
- Need Dockerfile for each agent type
- Environment variables managed through Docker
- Logs accessible via docker logs
- Can transition to Kubernetes later if needed

## Implementation Notes

```yaml
# docker-compose.yml structure
services:
  omi-gateway:
    build: ./agents/omi_gateway
    ports:
      - "8001:8000"
    environment:
      - OMI_API_URL=${OMI_API_URL}
    networks:
      - a2a-network

  context-agent:
    build: ./agents/context_analysis
    ports:
      - "8002:8000"
    networks:
      - a2a-network
```

```dockerfile
# Agent Dockerfile template
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "-m", "agent"]
```

## References

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Microservices with Docker](https://www.docker.com/resources/what-container/)
- [12-Factor App Principles](https://12factor.net/)

## Notes

Docker deployment aligns with modern microservices practices and makes the demo portable. The overhead is acceptable for the benefits gained in isolation and ease of deployment.