# 🚀 Quick Deploy Guide for Instructors (8 Teams)

This guide will get your workshop backend running in under 10 minutes.

## Step 1: One-Time Setup (5 minutes)

### Install Fly.io CLI
```bash
# On macOS
brew install flyctl

# On Linux/WSL
curl -L https://fly.io/install.sh | sh

# On Windows
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
```

### Login to Fly.io
```bash
fly auth login
# This opens a browser - create a free account
```

## Step 2: Deploy the Backend (5 minutes)

```bash
# Clone and enter the directory
git clone git@github.com:GDG-PVD/neurohub.git
cd neurohub

# Run the simplified deployment
./scripts/workshop_deploy.sh
```

That's it! Your backend is now live at: `https://neurohub-workshop.fly.dev`

## Step 3: Share with Students

### Option A: Single Shared Key (Simplest)
Share this with all teams:
```
Backend URL: https://neurohub-workshop.fly.dev
API Key: neurohub_workshop_2024
```

### Option B: Team-Specific Keys
Give each team their own key:
```
Team 1: neurohub_team1_2024
Team 2: neurohub_team2_2024
... etc
```

## 📊 Monitor During Workshop

### View Real-Time Logs
```bash
fly logs -a neurohub-workshop
```

### Check Status
```bash
fly status -a neurohub-workshop
```

### SSH if Needed
```bash
fly ssh console -a neurohub-workshop
```

## 🎯 Workshop Day Checklist

### Before Students Arrive
```bash
# 1. Check backend is running
curl https://neurohub-workshop.fly.dev/health

# 2. Test with demo script
OMI_API_BASE_URL=https://neurohub-workshop.fly.dev \
OMI_API_KEY=neurohub_workshop_2024 \
uv run python demo_simple.py
```

### Share with Students
Write on board or share in chat:
```
1. Clone: git clone git@github.com:GDG-PVD/neurohub.git
2. Setup: cd neurohub && uv pip install -e ".[dev]"
3. Configure: Add to .env.local:
   OMI_API_BASE_URL=https://neurohub-workshop.fly.dev
   OMI_API_KEY=neurohub_workshop_2024
4. Run: uv run python demo_simple.py
```

## 🔧 Quick Fixes

### If backend is slow/unresponsive
```bash
# Restart the app
fly apps restart neurohub-workshop

# Scale up if needed (still free)
fly scale count 2 -a neurohub-workshop
```

### If students can't connect
1. Check they're using HTTPS (not HTTP)
2. Verify the API key is correct
3. Test from your machine

### Emergency Local Fallback
```bash
# If cloud fails, run locally
docker run -d -p 8000:8000 \
  -e OMI_API_KEY=neurohub_workshop_2024 \
  omiai/mcp-server:latest

# Tell students to use
OMI_API_BASE_URL=http://YOUR_IP:8000
```

## 📈 Post-Workshop

### View Usage Stats
```bash
fly logs -a neurohub-workshop | grep "GET\|POST" | wc -l
```

### Clean Up (Optional)
```bash
# Suspend the app (keeps it but stops billing)
fly scale count 0 -a neurohub-workshop

# Or delete completely
fly apps destroy neurohub-workshop
```

## 💡 Pro Tips

1. **Deploy the day before** - Gives you time to test
2. **Use the monitoring** - Keep logs open during workshop
3. **Have backup ready** - Local Docker just in case
4. **Keep it simple** - One shared key works fine for 8 teams

## 📞 Quick Support

- **Fly.io Status**: https://status.fly.io/
- **Community Help**: https://community.fly.io/
- **Our Repo Issues**: https://github.com/GDG-PVD/neurohub/issues

---

**Remember**: The goal is to minimize setup time so teams can focus on building cool AI agents! 🤖