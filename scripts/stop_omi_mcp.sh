#!/bin/bash
# Stop OMI MCP Server

echo "🛑 Stopping OMI MCP Server..."

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    echo "❌ Docker is not running."
    exit 1
fi

# Check if container is running
if docker ps --format '{{.Names}}' | grep -q "^omi-mcp-server$"; then
    docker stop omi-mcp-server
    echo "✅ OMI MCP Server stopped"
else
    echo "ℹ️  OMI MCP Server was not running"
fi