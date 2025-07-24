#!/usr/bin/env python3
"""Start the OMI Gateway Agent."""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set environment variables
os.environ["GATEWAY_AGENT_PORT"] = "8001"
os.environ["A2A_AGENT_PORT"] = "8000"
os.environ["OMI_API_URL"] = os.environ.get("OMI_API_URL", "http://localhost:8000")
os.environ["OMI_API_KEY"] = os.environ.get("OMI_API_KEY", "omi_mcp_da4ca036a2d6b21febcb3b99ad2b49da")

# Import and run
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "agents.omi_gateway.agent:app",
        host="0.0.0.0",
        port=8001,
        reload=False
    )