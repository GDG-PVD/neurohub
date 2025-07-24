#!/bin/bash
# Create a clean repository with just the a2a-demo content

echo "🧹 Creating clean NeuroHub repository..."

# Create a temporary directory
TEMP_DIR="/tmp/neurohub-clean"
rm -rf $TEMP_DIR
mkdir -p $TEMP_DIR

# Copy only the a2a-demo content
echo "📦 Copying project files..."
cp -r . $TEMP_DIR/
cd $TEMP_DIR

# Remove any git history
rm -rf .git

# Initialize fresh git repo
git init
git config user.email "you@example.com"  # Use a generic email to avoid privacy issues
git config user.name "GDG-PVD"

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: NeuroHub educational multi-agent AI demo

- Complete workshop materials and documentation
- OMI MCP integration with cloud deployment support  
- Simple demo for teaching multi-agent concepts
- Instructor guides and student handouts
- One-click deployment scripts for workshops
- Comprehensive troubleshooting guides"

# Add remote
git remote add origin git@github.com:GDG-PVD/neurohub.git

# Force push
echo "🚀 Pushing to GitHub..."
git push -f origin main

echo "✅ Done! Clean repository pushed to https://github.com/GDG-PVD/neurohub"
echo ""
echo "Next steps:"
echo "1. Go to: https://github.com/GDG-PVD/neurohub/settings"
echo "2. Add description: Educational demonstration of multi-agent AI systems using OMI wearable device"
echo "3. Add topics: ai, multi-agent, education, omi, workshop, python"