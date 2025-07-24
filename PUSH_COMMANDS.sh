#!/bin/bash
# Commands to push to GitHub

# Add the GitHub remote (if not already added)
git remote add origin git@github.com:GDG-PVD/neurohub.git 2>/dev/null || echo "Remote already exists"

# Create initial commit
git commit -m "Initial commit: NeuroHub educational multi-agent AI demo

- Complete workshop materials and documentation
- OMI MCP integration with cloud deployment support  
- Simple demo for teaching multi-agent concepts
- Instructor guides and student handouts
- One-click deployment scripts for workshops
- Comprehensive troubleshooting guides"

# Push to GitHub
git push -u origin main

echo "✅ Pushed to https://github.com/GDG-PVD/neurohub"
echo ""
echo "Next steps:"
echo "1. Go to: https://github.com/GDG-PVD/neurohub/settings"
echo "2. Add description: Educational demonstration of multi-agent AI systems using OMI wearable device"
echo "3. Add topics: ai, multi-agent, education, omi, workshop, python"
echo "4. Create initial release if desired"