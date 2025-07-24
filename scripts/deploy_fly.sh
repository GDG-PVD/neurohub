#!/bin/bash
# Deploy OMI MCP Server to Fly.io

set -e

echo "🚀 Deploying OMI MCP Server to Fly.io..."

# Check if fly CLI is installed
if ! command -v fly &> /dev/null; then
    echo "❌ Fly CLI not found. Installing..."
    curl -L https://fly.io/install.sh | sh
    export FLYCTL_INSTALL="/home/$USER/.fly"
    export PATH="$FLYCTL_INSTALL/bin:$PATH"
fi

# Check if logged in
if ! fly auth whoami &> /dev/null; then
    echo "📝 Please log in to Fly.io..."
    fly auth login
fi

# Create fly.toml if it doesn't exist
if [ ! -f fly.toml ]; then
    echo "📄 Creating fly.toml configuration..."
    cat > fly.toml << 'EOF'
app = "neurohub-omi-mcp"
primary_region = "bos"
kill_signal = "SIGINT"
kill_timeout = "5s"

[experimental]
  auto_rollback = true

[build]
  image = "omiai/mcp-server:latest"

[env]
  PORT = "8000"
  LOG_LEVEL = "info"

[[services]]
  protocol = "tcp"
  internal_port = 8000
  processes = ["app"]

  [[services.ports]]
    port = 80
    handlers = ["http"]
    force_https = true

  [[services.ports]]
    port = 443
    handlers = ["tls", "http"]

  [services.concurrency]
    type = "connections"
    hard_limit = 25
    soft_limit = 20

  [[services.tcp_checks]]
    interval = "15s"
    timeout = "2s"
    grace_period = "1s"
    restart_limit = 0

  [[services.http_checks]]
    interval = "10s"
    timeout = "2s"
    grace_period = "5s"
    restart_limit = 0
    method = "get"
    path = "/health"

[metrics]
  port = 9091
  path = "/metrics"
EOF
fi

# Set secrets
echo "🔐 Setting API key secret..."
if [ -z "$OMI_API_KEY" ]; then
    # Use demo key if not set
    fly secrets set OMI_API_KEY=omi_mcp_demo_key_2024
else
    fly secrets set OMI_API_KEY="$OMI_API_KEY"
fi

# Launch or deploy
if fly status &> /dev/null; then
    echo "📦 Deploying update to existing app..."
    fly deploy --ha=false
else
    echo "🆕 Launching new app..."
    fly launch --copy-config --yes --ha=false
fi

# Get the app URL
APP_URL=$(fly status --json | jq -r '.Hostname // empty')
if [ -z "$APP_URL" ]; then
    APP_URL="neurohub-omi-mcp.fly.dev"
fi

echo "✅ Deployment complete!"
echo ""
echo "🌐 Your OMI MCP Server is available at:"
echo "   https://$APP_URL"
echo ""
echo "📝 Update your .env.local file:"
echo "   OMI_API_BASE_URL=https://$APP_URL"
echo ""
echo "🧪 Test the deployment:"
echo "   curl https://$APP_URL/health"
echo ""
echo "📊 View logs:"
echo "   fly logs"
echo ""
echo "🔧 SSH into the container:"
echo "   fly ssh console"