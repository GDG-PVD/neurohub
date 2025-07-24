# AgentDB Setup Guide

## Prerequisites

1. AgentDB account (sign up at https://agentdb.dev)
2. API key from AgentDB dashboard
3. Python 3.11+ or Node.js 18+

## Configuration

### 1. Create Local Environment File

Create `.env.local` in the project root:

```bash
cp .env.example .env.local
```

### 2. Add Your API Key

Edit `.env.local` and add your AgentDB API key:

```env
# AgentDB Configuration
AGENTDB_API_KEY=your_agentdb_api_key_here
AGENTDB_API_URL=https://api.agentdb.dev
```

⚠️ **Security Notes:**
- Never commit `.env.local` to version control
- The `.gitignore` file already excludes it
- For production, use environment variables or a secrets manager

### 3. Install SDK

#### For JavaScript/TypeScript:
```bash
npm install @agentdb/sdk
# or
yarn add @agentdb/sdk
```

#### For Python:
```bash
# Currently, use the REST API directly
# Python SDK coming soon
pip install aiohttp
```

## Testing the Connection

### Using the Test Script

```bash
cd a2a-demo
python scripts/test_agentdb.py
```

This will:
1. Verify your API key is loaded
2. Create a test agent database
3. Store and retrieve data
4. Create a conversation database

### Manual Test with curl

```bash
# Test API key (replace with your key)
curl -X POST https://api.agentdb.dev/v1/databases \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"token": "test-db-001", "name": "test", "type": "sqlite"}'
```

## Usage in Agents

### 1. Import Settings

```python
from config.settings import settings

# Get AgentDB manager
db_manager = settings.get_agent_db_manager()
```

### 2. Create Agent Database

```python
class MyAgent(A2AAgent):
    async def initialize(self):
        # Create persistent database for this agent
        self.db = await db_manager.create_agent_database(self.agent_id)
        
        # Load previous state if exists
        state = await db_manager.get_agent_memory(
            self.agent_id,
            "agent_state"
        )
```

### 3. Store and Retrieve Data

```python
# Store data
await db_manager.store_agent_memory(
    agent_id="my-agent",
    key="user_preferences",
    value={"theme": "dark", "language": "en"}
)

# Retrieve data
prefs = await db_manager.get_agent_memory(
    agent_id="my-agent",
    key="user_preferences"
)
```

## Environment Variables Reference

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `AGENTDB_API_KEY` | Your AgentDB API key | Yes | - |
| `AGENTDB_API_URL` | AgentDB API endpoint | No | https://api.agentdb.dev |

## Troubleshooting

### API Key Not Found

If you see "AGENTDB_API_KEY not found":
1. Check `.env.local` exists
2. Verify the key is set correctly
3. Restart your application

### Connection Errors

1. Verify internet connection
2. Check API key is valid
3. Ensure API URL is correct

### Rate Limits

AgentDB has the following limits:
- Starter: 1M requests/month
- Pro: 10M requests/month
- Enterprise: Unlimited

## Best Practices

1. **One Database Per Agent**: Each agent should have its own database
2. **Conversation Isolation**: Create new database for each conversation
3. **Clean Up**: Delete old conversation databases for GDPR compliance
4. **Monitor Usage**: Track your API usage in AgentDB dashboard
5. **Backup Important Data**: Use export feature for critical data

## Next Steps

1. [Implement vector search](../architecture/agentdb-integration.md#vector-search-integration)
2. [Set up monitoring](monitoring.md)
3. [Configure data retention](data-retention.md)