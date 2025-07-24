# 🌐 Backend Hosting Guide for OMI MCP Server

This guide shows how to host the OMI MCP server publicly so students don't need to run Docker locally.

## 🎯 Overview

Instead of running on `localhost:8000`, we can host the OMI MCP server on various cloud platforms. Students will then use:

```bash
export OMI_API_BASE_URL="https://your-hosted-backend.com"
```

## 🚀 Hosting Options

### Option 1: Railway (Recommended for Education)

**Pros**: Free tier, easy deployment, automatic HTTPS
**Cons**: Limited free hours

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and initialize
railway login
railway init

# Create railway.json
{
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "./Dockerfile"
  },
  "deploy": {
    "numReplicas": 1,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}

# Deploy
railway up
```

### Option 2: Google Cloud Run

**Pros**: Generous free tier, auto-scaling, pay-per-use
**Cons**: Requires GCP account setup

```bash
# Build and push to Google Container Registry
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/omi-mcp-server

# Deploy to Cloud Run
gcloud run deploy omi-mcp-server \
  --image gcr.io/YOUR_PROJECT_ID/omi-mcp-server \
  --platform managed \
  --allow-unauthenticated \
  --port 8000 \
  --region us-central1
```

### Option 3: Fly.io

**Pros**: Global edge deployment, generous free tier
**Cons**: Requires credit card for verification

```toml
# fly.toml
app = "neurohub-omi-mcp"
primary_region = "bos"

[build]
  image = "omiai/mcp-server:latest"

[env]
  PORT = "8000"

[http_service]
  internal_port = 8000
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0

[[services]]
  protocol = "tcp"
  internal_port = 8000
  ports = [
    { port = 80, handlers = ["http"] },
    { port = 443, handlers = ["tls", "http"] }
  ]
```

```bash
# Deploy
fly launch
fly deploy
```

### Option 4: Render

**Pros**: Simple deployment, free SSL, easy rollbacks
**Cons**: Free tier spins down after inactivity

```yaml
# render.yaml
services:
  - type: web
    name: omi-mcp-server
    env: docker
    dockerfilePath: ./Dockerfile
    envVars:
      - key: PORT
        value: 8000
    healthCheckPath: /health
```

### Option 5: DigitalOcean App Platform

**Pros**: $5/month student credits available
**Cons**: Not free

```yaml
# app.yaml
name: neurohub-omi-mcp
region: nyc
services:
  - name: omi-mcp-server
    dockerfile_path: Dockerfile
    source_dir: .
    http_port: 8000
    instance_count: 1
    instance_size_slug: basic-xxs
    routes:
      - path: /
```

## 🔧 Production Dockerfile

Create a production-ready Dockerfile:

```dockerfile
FROM omiai/mcp-server:latest

# Add health check endpoint
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Add any custom configuration
ENV PORT=8000
ENV LOG_LEVEL=info

# Expose port
EXPOSE 8000

# Run the server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🔐 Security Considerations

### 1. API Key Management

For a shared educational backend, consider:

```python
# Option A: Shared Demo Key
DEMO_API_KEY = "omi_mcp_demo_key_for_education"

# Option B: Per-Student Keys
# Generate keys with expiration for workshops
```

### 2. Rate Limiting

Add rate limiting to prevent abuse:

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.get("/api/memories")
@limiter.limit("100/hour")
async def get_memories():
    pass
```

### 3. CORS Configuration

Enable CORS for web-based demos:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://neurohub-demo.com"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

## 📝 Environment Configuration

### For Students

Create a simplified `.env` file:

```bash
# .env.cloud
OMI_API_BASE_URL=https://neurohub-omi.fly.dev
OMI_API_KEY=omi_mcp_demo_key_2024
```

### Update Scripts

Modify `scripts/test_omi_connection.py`:

```python
import os

# Use cloud backend if available
api_base_url = os.getenv('OMI_API_BASE_URL', 'http://localhost:8000')
print(f"Connecting to: {api_base_url}")
```

## 🚀 GitHub Actions Deployment

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy OMI MCP Server

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to Fly.io
        uses: superfly/flyctl-actions/setup-flyctl@master
      
      - run: flyctl deploy --remote-only
        env:
          FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}
```

## 📊 Monitoring

### Health Check Endpoint

Add to the MCP server:

```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }
```

### Uptime Monitoring

Use free services like:
- UptimeRobot
- Pingdom (free tier)
- Better Uptime

## 🎓 Educational Benefits

### Advantages of Cloud Hosting:

1. **No Docker Required**: Students can focus on AI concepts
2. **Instant Start**: No setup time in workshops
3. **Consistent Environment**: Everyone uses same backend
4. **Mobile Friendly**: Can demo from phones/tablets
5. **Scalable**: Handles entire classroom simultaneously

### Workshop Setup:

```bash
# Instructor provides:
export OMI_API_BASE_URL="https://workshop-omi.fly.dev"
export OMI_API_KEY="workshop_key_2024"

# Students just run:
uv run python demo_simple.py
```

## 📋 Deployment Checklist

- [ ] Choose hosting platform
- [ ] Set up account and billing (if needed)
- [ ] Configure environment variables
- [ ] Deploy MCP server
- [ ] Test with demo script
- [ ] Set up monitoring
- [ ] Document URL and keys for students
- [ ] Create backup deployment

## 🔗 Example Deployments

Here are some example URLs you might end up with:

- Railway: `https://neurohub-omi.up.railway.app`
- Cloud Run: `https://omi-mcp-server-abc123-uc.a.run.app`
- Fly.io: `https://neurohub-omi.fly.dev`
- Render: `https://omi-mcp-server.onrender.com`

## 💡 Tips

1. **Use Environment-Specific Keys**: Different keys for dev/prod
2. **Monitor Usage**: Track API calls to detect issues
3. **Prepare Backup**: Have localhost fallback ready
4. **Document Everything**: Clear setup instructions for TAs
5. **Test Scale**: Load test before workshop

---

With a hosted backend, your workshop setup time drops from 30 minutes to 5 minutes! 🚀