# 📖 OMI MCP Official Reference

This document summarizes the official OMI Model Context Protocol (MCP) server documentation.

## Overview

The OMI MCP server is a Model Context Protocol server for OMI interaction and automation. It provides tools to read, search, and manipulate Memories and Conversations.

## Configuration

### API Key Setup

1. **Generate API Key**: In the OMI app, go to `Settings > Developer > MCP`
2. **Use API Key**: 
   - Can be provided with each tool call
   - Falls back to `OMI_API_KEY` environment variable

### Docker Installation

The official way to run the OMI MCP server is via Docker:

```json
"mcpServers": {
  "omi": {
    "command": "docker",
    "args": ["run", "--rm", "-i", "-e", "OMI_API_KEY=your_api_key_here", "omiai/mcp-server"]
  }
}
```

## Available Tools

The OMI MCP server provides 5 main tools:

### 1. `get_memories`
- **Purpose**: Retrieve a list of user memories
- **Inputs**:
  - `limit` (number, optional): Max memories to retrieve (default: 100)
  - `categories` (array of MemoryFilterOptions, optional): Categories to filter by
- **Returns**: JSON object with list of memories

### 2. `create_memory`
- **Purpose**: Create a new memory
- **Inputs**:
  - `content` (string): Memory content
  - `category` (MemoryFilterOptions): Memory category
- **Returns**: Created memory object

### 3. `delete_memory`
- **Purpose**: Delete a memory by ID
- **Inputs**:
  - `memory_id` (string): ID of memory to delete
- **Returns**: Operation status

### 4. `edit_memory`
- **Purpose**: Edit a memory's content
- **Inputs**:
  - `memory_id` (string): ID of memory to edit
  - `content` (string): New content
- **Returns**: Operation status

### 5. `get_conversations`
- **Purpose**: Retrieve user conversations
- **Inputs**:
  - `include_discarded` (boolean, optional): Include discarded conversations (default: false)
  - `limit` (number, optional): Max conversations to retrieve (default: 25)
- **Returns**: List of conversation objects with transcripts, timestamps, geolocation, and summaries

## Debugging

### MCP Inspector
```bash
# For uvx installations
npx @modelcontextprotocol/inspector uvx mcp-server-omi

# For development
cd path/to/servers/src/omi
npx @modelcontextprotocol/inspector uv run mcp-server-omi
```

### View Logs
```bash
tail -n 20 -f ~/Library/Logs/Claude/mcp-server-omi.log
```

## Advanced Configuration

### Custom Backend URL
For self-hosted OMI backends:
```bash
export OMI_API_BASE_URL="https://your-backend-url.com"
```

## Examples

Official examples are available at:
https://github.com/BasedHardware/omi/tree/main/mcp/examples

These include integrations with:
- LangChain
- OpenAI Agents
- DSPy

## License

The OMI MCP server is licensed under the MIT License.

## Important Notes for Our Demo

1. **Docker Image**: We're using `omiai/mcp-server:latest`
2. **Default Port**: The server runs on port 8000
3. **API Key Format**: Keys typically start with `omi_mcp_`
4. **Memory Categories**: The official docs mention MemoryFilterOptions but don't specify what they are
5. **Conversation Data**: Includes transcripts, timestamps, geolocation, and structured summaries

## Differences from Our Demo

Our demo simulates the MCP functionality but:
- Uses a simplified API subset
- Focuses on conversation processing rather than memory management
- Demonstrates multi-agent analysis (not part of official MCP)
- Adds A2A protocol integration (our extension)

The official MCP server is more focused on memory and conversation management, while our demo extends this with multi-agent AI capabilities.