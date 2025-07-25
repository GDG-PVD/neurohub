# 🔌 Airtable MCP Integration Guide

This guide explains how to integrate the Airtable MCP server with the NeuroHub multi-agent system.

## Overview

The Airtable MCP server allows AI agents to interact with Airtable databases, enabling persistent storage and retrieval of:
- Conversation summaries
- Action items
- Knowledge base entries
- Agent collaboration data

## Prerequisites

1. **Airtable Account**: Sign up at [airtable.com](https://airtable.com)
2. **API Key**: Generate from Account → Developer hub → Personal access tokens
3. **Base ID**: Found in your Airtable base URL (e.g., `appXXXXXXXXXXXXXX`)
4. **Node.js**: Required for running the MCP server

## Installation

### 1. Install Airtable MCP Server

```bash
# Clone the repository
git clone https://github.com/domdomegg/airtable-mcp-server.git
cd airtable-mcp-server

# Install dependencies
npm install

# Build the server
npm run build
```

### 2. Configure Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "airtable": {
      "command": "node",
      "args": ["/path/to/airtable-mcp-server/dist/index.js"],
      "env": {
        "AIRTABLE_API_KEY": "your_api_key_here",
        "AIRTABLE_BASE_ID": "your_base_id_here"
      }
    },
    "omi": {
      "command": "docker",
      "args": ["run", "--rm", "-i", "-e", "OMI_API_KEY=your_omi_key", "omiai/mcp-server"]
    }
  }
}
```

### 3. Create Airtable Schema

Create a new base in Airtable with these tables:

#### Conversations Table
- **conversation_id** (Single line text, Primary)
- **timestamp** (Date time)
- **summary** (Long text)
- **participants** (Multiple select)
- **topics** (Multiple select)
- **agent_analysis** (Long text)

#### Actions Table
- **action_id** (Autonumber, Primary)
- **conversation_id** (Link to Conversations)
- **action_item** (Long text)
- **deadline** (Date)
- **assignee** (Single select)
- **status** (Single select: Pending, In Progress, Complete)
- **created_by** (Single line text)

#### Knowledge Table
- **knowledge_id** (Autonumber, Primary)
- **topic** (Single line text)
- **content** (Long text)
- **source_conversation** (Link to Conversations)
- **tags** (Multiple select)
- **created_at** (Date time)

## Integration with NeuroHub

### 1. Create Airtable Integration Module

Create `integrations/airtable_connector.py`:

```python
import os
from typing import List, Dict, Any, Optional
from datetime import datetime
import asyncio
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class AirtableConfig:
    """Configuration for Airtable connection"""
    api_key: str
    base_id: str
    
    @classmethod
    def from_env(cls) -> "AirtableConfig":
        """Load configuration from environment variables"""
        api_key = os.getenv("AIRTABLE_API_KEY")
        base_id = os.getenv("AIRTABLE_BASE_ID")
        
        if not api_key or not base_id:
            raise ValueError("AIRTABLE_API_KEY and AIRTABLE_BASE_ID must be set")
        
        return cls(api_key=api_key, base_id=base_id)

class AirtableConnector:
    """
    Connector for Airtable operations via MCP server
    
    This connector simulates MCP server calls for educational purposes.
    In a real implementation, this would communicate with the actual
    Airtable MCP server.
    """
    
    def __init__(self, config: AirtableConfig):
        self.config = config
        self.base_url = f"https://api.airtable.com/v0/{config.base_id}"
        
    async def save_conversation(self, conversation_data: Dict[str, Any]) -> str:
        """Save conversation summary to Airtable"""
        # In real implementation, this would call the MCP server
        logger.info(f"Saving conversation to Airtable: {conversation_data}")
        
        # Simulated response
        return f"conv_{datetime.now().timestamp()}"
    
    async def save_action_items(self, conversation_id: str, actions: List[Dict[str, Any]]) -> List[str]:
        """Save action items to Airtable"""
        logger.info(f"Saving {len(actions)} action items for conversation {conversation_id}")
        
        # Simulated response
        action_ids = []
        for i, action in enumerate(actions):
            action_ids.append(f"action_{conversation_id}_{i}")
        
        return action_ids
    
    async def save_knowledge(self, knowledge_data: Dict[str, Any]) -> str:
        """Save knowledge entry to Airtable"""
        logger.info(f"Saving knowledge to Airtable: {knowledge_data}")
        
        # Simulated response
        return f"knowledge_{datetime.now().timestamp()}"
    
    async def get_recent_conversations(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieve recent conversations from Airtable"""
        logger.info(f"Retrieving last {limit} conversations from Airtable")
        
        # Simulated response
        return [
            {
                "conversation_id": f"conv_{i}",
                "timestamp": datetime.now().isoformat(),
                "summary": f"Sample conversation {i}",
                "topics": ["topic1", "topic2"]
            }
            for i in range(limit)
        ]
    
    async def get_pending_actions(self, assignee: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieve pending action items from Airtable"""
        logger.info(f"Retrieving pending actions for {assignee or 'all users'}")
        
        # Simulated response
        return [
            {
                "action_id": f"action_{i}",
                "action_item": f"Sample action {i}",
                "deadline": "2024-12-31",
                "assignee": assignee or "unassigned",
                "status": "Pending"
            }
            for i in range(3)
        ]
```

### 2. Update Gateway Agent

Modify `agents/omi_gateway/agent.py` to include Airtable integration:

```python
# Add to imports
from integrations.airtable_connector import AirtableConnector, AirtableConfig

# In the OmiGatewayAgent class __init__ method:
try:
    self.airtable = AirtableConnector(AirtableConfig.from_env())
    logger.info("Airtable connector initialized")
except Exception as e:
    logger.warning(f"Airtable connector not available: {e}")
    self.airtable = None

# In the process_conversation method, after getting agent responses:
if self.airtable:
    # Save conversation summary
    conversation_id = await self.airtable.save_conversation({
        "timestamp": datetime.now().isoformat(),
        "summary": combined_response.get("summary", ""),
        "participants": ["user"],
        "topics": combined_response.get("topics", []),
        "agent_analysis": str(agent_responses)
    })
    
    # Save action items if any
    if "actions" in combined_response:
        await self.airtable.save_action_items(
            conversation_id,
            combined_response["actions"]
        )
```

### 3. Environment Configuration

Add to `.env.local`:

```bash
# Airtable Configuration
AIRTABLE_API_KEY=your_api_key_here
AIRTABLE_BASE_ID=your_base_id_here

# Optional: Table names (if different from defaults)
AIRTABLE_CONVERSATIONS_TABLE=Conversations
AIRTABLE_ACTIONS_TABLE=Actions
AIRTABLE_KNOWLEDGE_TABLE=Knowledge
```

## Usage Examples

### 1. Direct MCP Server Usage (in Claude)

When the MCP server is configured, you can use these commands:

```
# List tables in your base
list_tables()

# Read records from a table
read_records(table_name="Conversations", max_records=10)

# Create a new record
create_record(
    table_name="Actions",
    fields={
        "action_item": "Review MCP integration",
        "deadline": "2024-12-15",
        "status": "Pending"
    }
)

# Update a record
update_record(
    table_name="Actions",
    record_id="recXXXXXXXXXXXXXX",
    fields={"status": "Complete"}
)
```

### 2. Integration with NeuroHub Demo

Run the enhanced demo:

```bash
# Start with Airtable integration
AIRTABLE_API_KEY=your_key AIRTABLE_BASE_ID=your_base uv run python demo_simple.py
```

### 3. Viewing Results

1. Open your Airtable base
2. Check the Conversations table for processed conversations
3. Review Actions table for extracted action items
4. Browse Knowledge table for stored insights

## Advanced Features

### 1. Real-time Sync

Create `scripts/airtable_sync.py`:

```python
import asyncio
from integrations.airtable_connector import AirtableConnector, AirtableConfig

async def sync_pending_actions():
    """Sync pending actions from Airtable"""
    connector = AirtableConnector(AirtableConfig.from_env())
    
    while True:
        actions = await connector.get_pending_actions()
        print(f"Found {len(actions)} pending actions")
        
        for action in actions:
            print(f"- {action['action_item']} (Due: {action['deadline']})")
        
        await asyncio.sleep(60)  # Check every minute

if __name__ == "__main__":
    asyncio.run(sync_pending_actions())
```

### 2. Webhook Integration

For real-time updates from Airtable:

1. Set up Airtable webhooks in your base
2. Create endpoint in Gateway Agent to receive updates
3. Process changes and notify other agents

## Troubleshooting

### Common Issues

1. **MCP Server Not Found**
   - Ensure Node.js is installed
   - Check path in claude_desktop_config.json
   - Verify server is built (`npm run build`)

2. **Authentication Errors**
   - Verify API key has correct scopes
   - Check base ID format
   - Ensure environment variables are set

3. **Table Not Found**
   - Verify table names match configuration
   - Check permissions on base
   - Ensure tables are created with correct schema

### Debug Mode

Enable debug logging:

```python
import logging
logging.getLogger("integrations.airtable_connector").setLevel(logging.DEBUG)
```

## Best Practices

1. **Rate Limiting**: Airtable has API rate limits (5 requests/second)
2. **Batch Operations**: Use batch create/update for multiple records
3. **Error Handling**: Always handle network and API errors gracefully
4. **Data Validation**: Validate data before sending to Airtable
5. **Backup**: Regularly export Airtable data for backup

## Next Steps

1. Explore advanced Airtable features (views, formulas, automations)
2. Implement bidirectional sync between agents and Airtable
3. Create dashboards using Airtable's interface designer
4. Set up automated workflows with Airtable automations

## Resources

- [Airtable MCP Server Repo](https://github.com/domdomegg/airtable-mcp-server)
- [Airtable API Documentation](https://airtable.com/api)
- [MCP Protocol Specification](https://modelcontextprotocol.io)
- [NeuroHub Documentation](./README.md)