#!/bin/bash
# Run demo using cloud backend (no Docker required)

echo "🚀 Running NeuroHub Demo with Cloud Backend"
echo "   No Docker required!"
echo ""

# Export cloud backend URL
export OMI_API_BASE_URL=https://neurohub-workshop.fly.dev
export OMI_API_KEY=neurohub_workshop_2024

# Run the demo
uv run python demo_simple.py