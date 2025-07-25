# 🎯 MCP Usage Examples - NeuroHub Integration

Now that you have Airtable and OMI MCP servers configured in Claude Desktop, here are practical examples of how to use them together.

## Verifying MCP Servers

In Claude Desktop, you can verify the servers are working:

```
# List available MCP tools
list_tools()

# You should see tools from both servers:
# - From Airtable: list_tables, read_records, create_record, update_record, delete_record
# - From OMI: get_memories, create_memory, delete_memory, edit_memory, get_conversations
```

## Example Workflows

### 1. Process OMI Conversation and Store in Airtable

```python
# Get recent conversation from OMI
conversation = get_conversations(limit=1)

# Analyze the conversation (using Claude's capabilities)
summary = analyze_conversation(conversation[0])

# Store in Airtable
create_record(
    table_name="Conversations",
    fields={
        "conversation_id": conversation[0]["id"],
        "timestamp": conversation[0]["created_at"],
        "summary": summary,
        "topics": extract_topics(conversation[0]),
        "raw_transcript": conversation[0]["transcript"]
    }
)
```

### 2. Extract Action Items and Track Them

```python
# Get conversation from OMI
conv = get_conversations(limit=1)[0]

# Extract action items
actions = extract_action_items(conv["transcript"])

# Store each action in Airtable
for action in actions:
    create_record(
        table_name="Actions",
        fields={
            "conversation_id": conv["id"],
            "action_item": action["description"],
            "deadline": action["deadline"],
            "assignee": action["assignee"],
            "status": "Pending"
        }
    )
```

### 3. Build Knowledge Base from Conversations

```python
# Get multiple conversations
conversations = get_conversations(limit=10)

# Extract key insights
for conv in conversations:
    insights = extract_key_insights(conv["transcript"])
    
    for insight in insights:
        create_record(
            table_name="Knowledge",
            fields={
                "topic": insight["topic"],
                "content": insight["content"],
                "source_conversation": conv["id"],
                "tags": insight["tags"],
                "created_at": datetime.now().isoformat()
            }
        )
```

### 4. Daily Summary Dashboard

```python
# Get today's conversations from OMI
today_conversations = get_conversations(limit=50)
today_only = filter_by_date(today_conversations, date=today())

# Get pending actions from Airtable
pending_actions = read_records(
    table_name="Actions",
    filter_by_formula="AND({status}='Pending', {deadline}>=TODAY())"
)

# Create summary
print(f"📊 Daily Summary")
print(f"- Conversations today: {len(today_only)}")
print(f"- Pending actions: {len(pending_actions)}")
print(f"- Due today: {count_due_today(pending_actions)}")
```

### 5. Memory Enhancement Workflow

```python
# Get OMI memories
memories = get_memories(limit=100)

# Enrich with additional context
for memory in memories:
    # Search Airtable for related conversations
    related = read_records(
        table_name="Conversations",
        filter_by_formula=f"SEARCH('{memory['topic']}', {{summary}})"
    )
    
    if related:
        # Update memory with additional context
        edit_memory(
            memory_id=memory["id"],
            content=memory["content"] + f"\n\nRelated discussions: {len(related)}"
        )
```

## Integration with NeuroHub Agents

When running NeuroHub agents, they can now leverage both MCP servers:

### Gateway Agent Enhancement

```python
# In agents/omi_gateway/agent.py
async def process_with_mcp(self, conversation_id: str):
    # Get conversation from OMI MCP
    conv_data = await self.mcp_client.call("get_conversations", {
        "conversation_id": conversation_id
    })
    
    # Process with agents
    results = await self.process_with_agents(conv_data)
    
    # Store results in Airtable MCP
    await self.mcp_client.call("create_record", {
        "table_name": "ProcessedConversations",
        "fields": {
            "conversation_id": conversation_id,
            "agent_results": json.dumps(results),
            "processed_at": datetime.now().isoformat()
        }
    })
```

## Best Practices

1. **Batch Operations**: When processing multiple items, use batch operations to reduce API calls
2. **Error Handling**: Always handle MCP errors gracefully
3. **Rate Limiting**: Be mindful of rate limits for both OMI and Airtable
4. **Data Consistency**: Ensure conversation IDs are consistent between systems
5. **Privacy**: Be careful with sensitive conversation data

## Troubleshooting

### Common Issues

1. **MCP Tools Not Available**
   - Restart Claude Desktop after config changes
   - Check Docker is running (for OMI MCP)
   - Verify Node.js path (for Airtable MCP)

2. **Authentication Errors**
   - Verify API keys in config
   - Check key permissions
   - Ensure base ID is correct

3. **Data Not Syncing**
   - Check table names match
   - Verify field names are correct
   - Look for type mismatches

## Advanced Patterns

### 1. Conversation Threading
Link related conversations across time:

```python
# Find previous related conversations
previous = read_records(
    table_name="Conversations",
    filter_by_formula=f"AND({{participants}}='{participant}', {{timestamp}}<'{current_time}')",
    max_records=5
)

# Create thread link
create_record(
    table_name="ConversationThreads",
    fields={
        "current_conversation": current_id,
        "previous_conversations": [p["id"] for p in previous],
        "thread_topic": common_topic
    }
)
```

### 2. Automated Insights
Generate insights from patterns:

```python
# Analyze conversation patterns
all_convs = read_records(table_name="Conversations", max_records=100)
patterns = analyze_patterns(all_convs)

# Store insights
for pattern in patterns:
    create_record(
        table_name="Insights",
        fields={
            "pattern_type": pattern["type"],
            "description": pattern["description"],
            "frequency": pattern["count"],
            "examples": pattern["conversation_ids"][:3]
        }
    )
```

## Next Steps

1. **Create Custom Views** in Airtable for different use cases
2. **Set Up Automations** in Airtable for notifications
3. **Build Dashboards** using Airtable's interface designer
4. **Integrate with Other Tools** via Airtable's integrations

Remember: The MCP servers provide the bridge between OMI's conversation data and Airtable's powerful database features, enabling sophisticated multi-agent workflows!