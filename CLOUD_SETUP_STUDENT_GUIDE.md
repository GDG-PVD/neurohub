# ☁️ Cloud Setup Guide for Students

This guide shows how to use the cloud-hosted OMI backend instead of running Docker locally.

## 🚀 Quick Start (Cloud Version)

### Step 1: Get the Backend URL

Your instructor will provide you with:
- **Backend URL**: `https://neurohub-omi.fly.dev` (example)
- **API Key**: `omi_mcp_workshop_2024` (example)

### Step 2: Configure Your Environment

```bash
# Create your environment file
cp .env.example .env.local

# Edit .env.local and add:
OMI_API_BASE_URL=https://neurohub-omi.fly.dev
OMI_API_KEY=omi_mcp_workshop_2024
```

### Step 3: Run the Demo

```bash
# No need to start Docker!
# Just run:
uv run python demo_simple.py
```

That's it! No Docker required! 🎉

## 🔍 Testing the Connection

Test if the cloud backend is working:

```bash
# Test the health endpoint
curl https://neurohub-omi.fly.dev/health

# Or use the test script
uv run python scripts/test_omi_connection.py
```

Expected output:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "1.0.0"
}
```

## 🆚 Cloud vs Local Comparison

| Feature | Cloud Setup | Local Docker |
|---------|------------|--------------|
| Setup Time | 2 minutes | 15-30 minutes |
| Requirements | Just Python | Python + Docker |
| Internet | Required | Not required |
| Performance | Depends on internet | Fast (local) |
| Reliability | High | Depends on setup |

## 🛠️ Troubleshooting Cloud Setup

### "Connection refused" or timeout
- **Check URL**: Make sure you copied it correctly
- **Check Internet**: Ensure you have internet connection
- **Try browser**: Visit the URL in your browser

### "Unauthorized" or API key errors
- **Check API key**: Make sure you copied it correctly
- **Check quotes**: Remove any extra quotes in .env.local
- **Ask instructor**: They may have updated the key

### Slow responses
- **Normal**: First request may be slow (cold start)
- **Patience**: Cloud services may have slight delays
- **Local fallback**: Can switch to local Docker if needed

## 📝 Environment File Example

Your `.env.local` should look like:

```bash
# Cloud Backend Configuration
OMI_API_BASE_URL=https://neurohub-omi.fly.dev
OMI_API_KEY=omi_mcp_workshop_2024

# Optional: AgentDB (if provided)
AGENTDB_API_KEY=your_agentdb_key_here
```

## 🎯 Benefits of Cloud Setup

1. **Faster Start**: Get coding in minutes, not hours
2. **No Docker Issues**: Avoid Docker installation problems
3. **Consistent Environment**: Everyone uses same backend
4. **Mobile Friendly**: Can even demo from a tablet
5. **Focus on AI**: Spend time learning AI, not DevOps

## 🔄 Switching Between Cloud and Local

You can easily switch between cloud and local:

```bash
# For cloud backend
export OMI_API_BASE_URL=https://neurohub-omi.fly.dev

# For local backend
export OMI_API_BASE_URL=http://localhost:8000
# (Don't forget to start Docker locally)
```

## 📊 Checking Backend Status

Want to see if the backend is working? Try these:

```bash
# Check health
curl https://neurohub-omi.fly.dev/health

# View API documentation (if available)
open https://neurohub-omi.fly.dev/docs

# Test with Python
python -c "
import requests
r = requests.get('https://neurohub-omi.fly.dev/health')
print(f'Status: {r.status_code}')
print(f'Response: {r.json()}')
"
```

## 🎓 Workshop Mode

For workshops and classes, instructors typically:

1. **Pre-deploy** the backend to cloud
2. **Share credentials** at start of class
3. **Monitor usage** during workshop
4. **Provide backup** local setup if needed

This means you can start learning immediately!

## 🚀 Advanced: Deploy Your Own

Want to deploy your own backend? See:
- [Backend Hosting Guide](BACKEND_HOSTING_GUIDE.md)
- [Fly.io Deployment Script](scripts/deploy_fly.sh)

But for workshops, just use the provided URL! 😊

---

**Remember**: The cloud setup is designed to make learning easier. If you have any issues, ask your instructor or TA for help!