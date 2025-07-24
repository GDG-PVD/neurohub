#!/bin/bash
# Quick deployment script for workshop instructors
# Deploys OMI MCP backend for ~8 teams (32 students)

set -e

echo "🎓 NeuroHub Workshop Deployment Script"
echo "======================================"
echo ""

# Configuration
APP_NAME="neurohub-workshop"
REGION="bos"  # Boston region, change if needed
API_KEY="neurohub_workshop_2024"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if fly CLI is installed
if ! command -v fly &> /dev/null; then
    echo -e "${RED}❌ Fly CLI not found!${NC}"
    echo "Please install it first:"
    echo "  macOS: brew install flyctl"
    echo "  Linux: curl -L https://fly.io/install.sh | sh"
    exit 1
fi

# Check if logged in
if ! fly auth whoami &> /dev/null; then
    echo -e "${YELLOW}📝 Please log in to Fly.io...${NC}"
    fly auth login
fi

echo "🚀 Deploying workshop backend..."
echo ""

# Create minimal fly.toml
cat > fly.toml << EOF
app = "$APP_NAME"
primary_region = "$REGION"
kill_signal = "SIGINT"
kill_timeout = "5s"

[build]
  image = "omiai/mcp-server:latest"

[env]
  PORT = "8000"
  LOG_LEVEL = "info"
  # Single shared key for workshop
  OMI_API_KEY = "$API_KEY"

[[services]]
  protocol = "tcp"
  internal_port = 8000

  [[services.ports]]
    port = 80
    handlers = ["http"]
    force_https = true

  [[services.ports]]
    port = 443
    handlers = ["tls", "http"]

  [services.concurrency]
    type = "connections"
    hard_limit = 100    # Support ~8 teams
    soft_limit = 80

  [[services.http_checks]]
    interval = "30s"
    timeout = "3s"
    grace_period = "5s"
    method = "get"
    path = "/health"
EOF

# Check if app already exists
if fly apps list | grep -q "$APP_NAME"; then
    echo -e "${YELLOW}⚠️  App already exists. Updating...${NC}"
    fly deploy --ha=false -a "$APP_NAME"
else
    echo "🆕 Creating new app..."
    fly launch --name "$APP_NAME" --region "$REGION" --ha=false --now --copy-config --yes
fi

# Get the app URL
APP_URL="https://$APP_NAME.fly.dev"

# Test the deployment
echo ""
echo "🧪 Testing deployment..."
sleep 5  # Give it a moment to start

if curl -s "$APP_URL/health" > /dev/null; then
    echo -e "${GREEN}✅ Backend is running!${NC}"
else
    echo -e "${YELLOW}⚠️  Backend might still be starting...${NC}"
    echo "Check in a minute: curl $APP_URL/health"
fi

# Clean up
rm fly.toml

# Print summary
echo ""
echo "========================================"
echo -e "${GREEN}🎉 Workshop Backend Deployed!${NC}"
echo "========================================"
echo ""
echo "📝 Share with your students:"
echo ""
echo "Backend URL: $APP_URL"
echo "API Key: $API_KEY"
echo ""
echo "📋 Quick Test:"
echo "curl $APP_URL/health"
echo ""
echo "📊 Monitor:"
echo "fly logs -a $APP_NAME"
echo ""
echo "🔧 If needed:"
echo "fly apps restart $APP_NAME"
echo ""
echo "💡 Student instructions:"
echo "1. Add to .env.local:"
echo "   OMI_API_BASE_URL=$APP_URL"
echo "   OMI_API_KEY=$API_KEY"
echo "2. Run: uv run python demo_simple.py"
echo ""
echo "Good luck with your workshop! 🚀"