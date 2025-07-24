# ADR-004: WebSocket for Real-time OMI Integration

**Date:** 2025-07-24

**Status:** Accepted

**Deciders:** Development Team, AI Architecture Lead

**Tags:** integration, real-time, protocols

## Context

The OMI device streams audio data in real-time for transcription and processing. We need a reliable, low-latency protocol for continuous data streaming between the OMI device and our gateway agent.

## Decision

Use WebSocket protocol for real-time audio streaming and bidirectional communication with OMI devices.

## Considered Options

1. **WebSocket**: Full-duplex communication protocol
   - Pros:
     - Bidirectional real-time communication
     - Low latency
     - Wide client/server support
     - Works through proxies/firewalls
     - Native browser support
   - Cons:
     - Connection management complexity
     - No built-in reconnection
     - Stateful connections

2. **Server-Sent Events (SSE)**: One-way server-to-client streaming
   - Pros:
     - Simple protocol
     - Auto-reconnection
     - Works over HTTP
   - Cons:
     - Unidirectional only
     - Not suitable for audio upload
     - Limited binary support

3. **gRPC Streaming**: High-performance RPC with streaming
   - Pros:
     - Efficient binary protocol
     - Bidirectional streaming
     - Strong typing
   - Cons:
     - Complex setup
     - Limited browser support
     - Requires HTTP/2

## Consequences

### Positive
- Real-time audio streaming capability
- Instant transcription feedback
- Bidirectional control messages
- Compatible with existing OMI infrastructure
- Easy integration with FastAPI

### Negative
- Need to implement reconnection logic
- Connection state management
- Potential for connection drops

### Neutral
- Requires WebSocket client in mobile app
- Need to handle binary audio data
- Connection pooling considerations

## Implementation Notes

```python
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    agent.websocket_clients.add(websocket)
    
    try:
        while True:
            data = await websocket.receive_json()
            # Process audio or transcript
    except WebSocketDisconnect:
        agent.websocket_clients.remove(websocket)
```

## References

- [WebSocket Protocol RFC 6455](https://datatracker.ietf.org/doc/html/rfc6455)
- [ADR-002: Gateway Pattern](002-agent-orchestration-pattern.md) - Gateway manages WebSocket connections
- [FastAPI WebSocket Documentation](https://fastapi.tiangolo.com/advanced/websockets/)

## Notes

WebSocket aligns well with our real-time processing requirements and is already used by OMI's existing infrastructure, making integration straightforward.