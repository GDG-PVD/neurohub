# ADR-009: Simplified Demo for Education

## Status
Accepted

## Context
The full multi-agent system with Docker Compose is powerful but overwhelming for students:
- Too many moving parts to understand
- Docker complexity obscures AI concepts
- Difficult to debug when things go wrong
- Students get lost in infrastructure

We need a simpler demonstration that still teaches multi-agent concepts.

## Decision
Create `demo_simple.py` that simulates multi-agent responses while connecting to the real OMI backend, allowing students to understand concepts without infrastructure complexity.

## Consequences

### Positive
- Students can run demo in 2 minutes
- Clear visualization of agent interactions
- Easy to modify and experiment
- Focus on AI concepts
- Single file to understand
- Works with just Python

### Negative
- Less realistic than full system
- Doesn't show actual agent communication
- Simulated responses instead of real AI
- May give wrong impression of complexity

### Neutral
- Different from production architecture
- Requires explanation of simplifications

## Implementation
```python
# demo_simple.py structure
1. Connect to OMI backend (real)
2. Process conversation (real)
3. Simulate agent analysis (fake)
4. Display results clearly
```

## Alternatives Considered
1. **Full Docker system only**: Too complex for teaching
2. **Pure simulation**: No real backend connection
3. **Jupyter notebooks**: Good but needs another tool
4. **Web UI**: Adds complexity

## Related
- [ADR-008: Cloud Deployment](008-cloud-deployment.md) - Complementary simplification
- [Working Demo Summary](../../WORKING_DEMO_SUMMARY.md)
- [Student Guide](../../STUDENT_GUIDE.md)