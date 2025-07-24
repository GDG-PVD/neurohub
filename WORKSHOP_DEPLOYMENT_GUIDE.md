# 🎯 Workshop Deployment Guide

This guide helps instructors deploy the OMI MCP backend for workshops and classes.

## 🚀 Quick Deployment (15 minutes)

### Option 1: One-Click Deploy to Fly.io (Recommended)

```bash
# Clone the repo
git clone git@github.com:GDG-PVD/neurohub.git
cd neurohub

# Deploy to Fly.io
./scripts/deploy_fly.sh
```

Your backend will be available at: `https://neurohub-omi-mcp.fly.dev`

### Option 2: Deploy to Railway

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template)

1. Click the button above
2. Add environment variable: `OMI_API_KEY=omi_mcp_workshop_2024`
3. Deploy!

## 📋 Pre-Workshop Checklist

### 1 Week Before
- [ ] Deploy backend to chosen platform
- [ ] Test with demo scripts
- [ ] Generate workshop API key
- [ ] Create backup deployment
- [ ] Test with expected number of students

### 1 Day Before
- [ ] Verify backend is running
- [ ] Test from different network
- [ ] Prepare offline backup
- [ ] Update student guide with URL

### Day Of Workshop
- [ ] Check backend health: `curl https://your-backend/health`
- [ ] Monitor logs: `fly logs` (if using Fly.io)
- [ ] Have local Docker ready as backup
- [ ] Share credentials with students

## 🔐 API Key Management

### For Workshops

Create time-limited keys:

```python
# workshop_keys.py
import secrets
from datetime import datetime, timedelta

def generate_workshop_key(workshop_name, hours=4):
    """Generate a workshop-specific API key"""
    key = f"omi_mcp_{workshop_name}_{secrets.token_hex(8)}"
    expiry = datetime.now() + timedelta(hours=hours)
    return key, expiry

# Example
key, expiry = generate_workshop_key("gdg_workshop_jan15")
print(f"Key: {key}")
print(f"Expires: {expiry}")
```

### Setting Keys

```bash
# For Fly.io
fly secrets set OMI_API_KEY="omi_mcp_workshop_2024"

# For Railway
railway variables set OMI_API_KEY="omi_mcp_workshop_2024"

# For Cloud Run
gcloud run services update omi-mcp-server \
  --set-env-vars OMI_API_KEY="omi_mcp_workshop_2024"
```

## 📊 Capacity Planning

### Expected Load

| Workshop Size | Recommended Platform | Configuration |
|--------------|---------------------|---------------|
| < 30 students | Fly.io (free) | 1 instance, 256MB |
| 30-100 students | Railway/Render | 2 instances, 512MB |
| 100+ students | Cloud Run | Auto-scaling 2-10 |

### Load Testing

```bash
# Test with expected load
ab -n 1000 -c 30 https://your-backend/health

# Or use k6
k6 run scripts/load-test.js
```

## 🛠️ Platform-Specific Tips

### Fly.io
- **Pros**: Great free tier, global edge
- **Watch**: Cold starts after inactivity
- **Fix**: Set `min_machines_running = 1`

### Railway
- **Pros**: Easy deployment, good UI
- **Watch**: Limited free hours
- **Fix**: Upgrade to starter plan ($5)

### Google Cloud Run
- **Pros**: Auto-scaling, pay-per-use
- **Watch**: Cold starts
- **Fix**: Set minimum instances to 1

### Render
- **Pros**: Simple, good free tier
- **Watch**: Spins down after 15 min
- **Fix**: Use cron job to ping every 10 min

## 📱 Student Instructions Template

Share this with students:

```markdown
# Workshop Backend Access

## Connection Details
- **Backend URL**: https://neurohub-omi.fly.dev
- **API Key**: omi_mcp_workshop_jan15_2024
- **Valid Until**: 5:00 PM today

## Setup
1. Update your .env.local:
   ```
   OMI_API_BASE_URL=https://neurohub-omi.fly.dev
   OMI_API_KEY=omi_mcp_workshop_jan15_2024
   ```

2. Test connection:
   ```bash
   uv run python scripts/test_omi_connection.py
   ```

3. Run demo:
   ```bash
   uv run python demo_simple.py
   ```
```

## 🚨 Emergency Procedures

### If Cloud Backend Fails

1. **Immediate**: Switch to backup deployment
2. **Fallback**: Use local Docker
3. **Last Resort**: Use mock responses

### Backup Commands

```bash
# Quick local deployment
docker run -d -p 8000:8000 \
  -e OMI_API_KEY=omi_mcp_local \
  omiai/mcp-server:latest

# Update student environments
echo "Please update your .env.local:"
echo "OMI_API_BASE_URL=http://localhost:8000"
```

### Mock Mode

If all else fails, update `demo_simple.py`:

```python
# Add at top of file
MOCK_MODE = True

if MOCK_MODE:
    print("⚠️  Running in mock mode (no backend)")
    # Return fake responses
```

## 📈 Monitoring During Workshop

### Real-time Monitoring

```bash
# Fly.io
fly logs --tail

# View metrics
fly status

# SSH to debug
fly ssh console
```

### Key Metrics to Watch
- Response time (should be < 500ms)
- Error rate (should be < 1%)
- Active connections
- Memory usage

## 💡 Best Practices

1. **Deploy Early**: Set up 2-3 days before
2. **Test Thoroughly**: From different networks
3. **Have Backups**: Multiple deployment options
4. **Monitor Actively**: Watch logs during workshop
5. **Communicate**: Keep students informed

## 🎓 Post-Workshop

1. **Collect Metrics**: Number of requests, errors
2. **Gather Feedback**: What worked, what didn't
3. **Clean Up**: Remove workshop keys
4. **Document**: Update guide with lessons learned

## 📚 Resources

- [Fly.io Dashboard](https://fly.io/dashboard)
- [Railway Dashboard](https://railway.app/dashboard)
- [Cloud Run Console](https://console.cloud.google.com/run)
- [Backend Hosting Guide](BACKEND_HOSTING_GUIDE.md)

---

**Remember**: A smooth workshop deployment lets students focus on learning AI, not fighting with infrastructure! 🚀