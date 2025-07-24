#!/bin/bash
# Start OMI MCP Server

echo "🚀 Starting OMI MCP Server..."

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop first."
    exit 1
fi

# Check if container is already running
if docker ps --format '{{.Names}}' | grep -q "^omi-mcp-server$"; then
    echo "✅ OMI MCP Server is already running on http://localhost:8000"
    echo "   To restart, run: docker stop omi-mcp-server && ./scripts/start_omi_mcp.sh"
    exit 0
fi

# Check if container exists but is stopped
if docker ps -a --format '{{.Names}}' | grep -q "^omi-mcp-server$"; then
    echo "🔄 Removing stopped container..."
    docker rm omi-mcp-server >/dev/null 2>&1
fi

# Check if API key is set
if [ -z "$OMI_API_KEY" ]; then
    # Try to load from .env.local
    if [ -f .env.local ]; then
        export $(grep OMI_API_KEY .env.local | xargs)
    fi
fi

if [ -z "$OMI_API_KEY" ]; then
    echo "❌ OMI_API_KEY not found. Please set it in .env.local or environment."
    exit 1
fi

echo "✅ Using API Key: ${OMI_API_KEY:0:20}..."

# Start the MCP server
docker run --rm -i \
    -e "OMI_API_KEY=$OMI_API_KEY" \
    -p 8000:8000 \
    --name omi-mcp-server \
    omiai/mcp-server:latest

echo "✅ OMI MCP Server started on http://localhost:8000"