#!/usr/bin/env python3
"""Run the OMI Gateway Agent locally for testing."""

import asyncio
import sys
from pathlib import Path

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

from agents.omi_gateway.agent import main

if __name__ == "__main__":
    print("Starting OMI Gateway Agent locally...")
    asyncio.run(main())