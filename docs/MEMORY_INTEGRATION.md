# NeuroHub Memory Integration: OMI + Mem0

## Overview

The NeuroHub workshop demonstrates a powerful synergy between OMI device memories and Mem0's AI memory platform. This integration creates a comprehensive memory-enhanced AI system that can:

1. **Capture** conversations through OMI wearable devices
2. **Store** memories persistently in Mem0
3. **Search** across all stored memories
4. **Analyze** conversation patterns and extract insights
5. **Enhance** AI agents with contextual memory access

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│ OMI Device  │────▶│ Memory Bridge│────▶│    Mem0     │
│  (Capture)  │     │   (Sync)     │     │  (Storage)  │
└─────────────┘     └──────────────┘     └─────────────┘
                            │
                            ▼
                    ┌──────────────┐
                    │  AI Agents   │
                    │(Context-Aware)│
                    └──────────────┘
```

## Key Concepts

### 1. OMI Memories
- **What**: Audio recordings and transcripts captured by OMI wearable devices
- **Contains**: Transcript, participants, emotions, topics, action items, location
- **Purpose**: Real-time conversation capture and initial processing

### 2. Mem0 Integration
- **What**: Persistent, searchable memory storage with AI-native capabilities
- **Features**: Vector search, metadata filtering, cross-session persistence
- **Purpose**: Long-term memory storage and retrieval

### 3. Memory Bridge
- **What**: Integration layer between OMI and Mem0
- **Functions**:
  - Sync OMI memories to Mem0
  - Unified search across both systems
  - Memory analysis and insights
  - Context injection for AI agents

## Workshop Flow

### Phase 1: Setup
1. Teams register with their OMI API keys
2. Workshop server initializes memory bridge
3. Teams get access to memory features

### Phase 2: Capture
1. Teams use OMI devices to record conversations
2. OMI processes audio and creates memories
3. Memories include rich metadata (participants, emotions, topics)

### Phase 3: Sync & Store
1. Teams sync their OMI memories to Mem0
2. Memory bridge enriches metadata for better searchability
3. Memories become available for AI agent access

### Phase 4: Analyze & Use
1. Teams search their memories
2. AI agents use memory context for better responses
3. Teams analyze their conversation patterns

## API Endpoints

### Memory Sync
```http
POST /memory/sync
{
  "team_id": "uuid"
}
```
Syncs all OMI memories to Mem0 for a team.

### Memory Search
```http
POST /memory/search
{
  "team_id": "uuid",
  "query": "search terms",
  "limit": 10
}
```
Searches across team memories using semantic search.

### Memory Analysis
```http
GET /memory/analysis/{team_id}
```
Analyzes team memories to extract insights:
- Total conversation time
- Unique participants
- Top discussion topics
- Emotion patterns
- Action items

### Context-Enhanced Processing
```http
POST /demo
{
  "team_id": "uuid",
  "transcript": "conversation text",
  "use_memory_context": true
}
```
Processes conversations with relevant memory context.

## Memory Schema

### OMI Memory Format
```json
{
  "id": "memory_id",
  "transcript": "conversation transcript",
  "created_at": "2024-01-25T10:00:00Z",
  "duration": 300,
  "participants": ["Alice", "Bob"],
  "emotions": ["excited", "focused"],
  "topics": ["AI integration", "project planning"],
  "action_items": ["Schedule meeting", "Send documentation"],
  "location": {"lat": 42.3601, "lng": -71.0589}
}
```

### Mem0 Storage Format
```json
{
  "content": "Memory from OMI device: [transcript]",
  "metadata": {
    "source": "omi_device",
    "team_id": "uuid",
    "memory_id": "omi_memory_id",
    "timestamp": "2024-01-25T10:00:00Z",
    "participants": ["Alice", "Bob"],
    "topics": ["AI integration"],
    "action_items": ["Schedule meeting"]
  }
}
```

## Benefits for Workshop

### 1. Continuity
- Conversations persist across sessions
- Teams can build on previous discussions
- No context is lost between demos

### 2. Context Awareness
- AI agents can reference past conversations
- More relevant and personalized responses
- Better action item tracking

### 3. Learning Insights
- Teams can analyze their collaboration patterns
- Identify frequently discussed topics
- Track progress over time

### 4. Real-World Application
- Demonstrates production-ready memory systems
- Shows integration between hardware (OMI) and AI (Mem0)
- Practical example of memory-enhanced AI

## Implementation Examples

### Syncing Memories
```python
# Memory bridge syncs OMI memories to Mem0
async def sync_team_memories(team_id: str, omi_api_key: str):
    # Get memories from OMI
    omi_memories = await omi_connector.get_user_memories(team_id)
    
    # Sync each memory to Mem0
    for memory in omi_memories:
        await memory_bridge.sync_omi_memory_to_mem0(team_id, memory)
```

### Context-Aware Processing
```python
# AI agent uses memory context
async def process_with_memory(team_id: str, transcript: str):
    # Get relevant memories
    memory_context = await memory_bridge.get_contextual_memories(
        team_id, 
        transcript[:100]  # Use beginning as context
    )
    
    # Process with enhanced context
    analysis = analyze_transcript(transcript, memory_context)
    return enhanced_response
```

### Memory Search
```python
# Search across team memories
async def search_memories(team_id: str, query: str):
    results = await memory_bridge.search_unified_memories(
        team_id=team_id,
        query=query,
        include_mem0=True,
        include_omi=True
    )
    return results
```

## Best Practices

1. **Privacy**: Teams only access their own memories
2. **Consent**: Ensure all participants consent to recording
3. **Relevance**: Use focused queries for better search results
4. **Context Window**: Limit memory context to most relevant items
5. **Regular Sync**: Sync memories periodically for best results

## Future Enhancements

1. **Cross-Team Insights**: Aggregate anonymized insights
2. **Memory Chains**: Link related memories automatically
3. **Emotion Tracking**: Analyze emotional patterns over time
4. **Smart Summarization**: Auto-generate meeting summaries
5. **Proactive Reminders**: AI agents remind about action items

## Conclusion

The OMI + Mem0 integration demonstrates how hardware and software can work together to create truly intelligent, context-aware AI systems. By bridging device memories with AI memory platforms, we enable a new generation of applications that learn and adapt from every interaction.