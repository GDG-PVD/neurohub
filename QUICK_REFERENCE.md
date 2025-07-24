# 🚀 Quick Reference Card - OMI Multi-Agent Demo

## 🎯 Essential Commands

### Initial Setup (One Time Only)
```bash
# 1. Clone the repository
git clone https://github.com/YourRepo/omi.git
cd omi/a2a-demo

# 2. Install UV package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# 3. Set up Python environment
uv venv
uv pip install -e ".[dev]"

# 4. Configure API keys
cp .env.example .env.local
# Edit .env.local with your keys
```

### Running the Demo (Every Time)
```bash
# Terminal 1: Start OMI Server
./scripts/start_omi_mcp.sh

# Terminal 2: Run Demo
# Option A - With UV (Easier!):
uv run python demo_simple.py

# Option B - Traditional way:
source .venv/bin/activate  # Note the dot!
python demo_simple.py
```

---

## 📁 Project Structure
```
a2a-demo/
├── 📄 demo_simple.py         # ⭐ Main demo script
├── 📁 agents/                # AI agent implementations
├── 📁 docs/                  # Documentation
├── 📄 .env.local            # Your API keys (private)
└── 📄 scripts/              # Helper scripts
```

---

## 🔑 Key Files for Students

| File | Purpose | When to Use |
|------|---------|-------------|
| `demo_simple.py` | Simple working demo | First demo to run |
| `STUDENT_GUIDE.md` | Detailed instructions | When you need help |
| `.env.local` | API key configuration | During setup |
| `scripts/test_omi_connection.py` | Test OMI connection | Troubleshooting |

---

## ⚡ Common Tasks

### Check if Everything is Working
```bash
# Test OMI connection
python scripts/test_omi_connection.py

# Check Docker
docker ps

# Check Python
python --version
```

### Restart Services
```bash
# Stop everything
docker-compose down
pkill -f start_omi_mcp.sh

# Start fresh
./scripts/start_omi_mcp.sh
```

### View Logs
```bash
# OMI server logs
docker logs omi-mcp-server

# Demo output is shown directly in terminal
```

---

## 🚨 Quick Fixes

| Problem | Solution |
|---------|----------|
| "Module not found" | Run: `source .venv/bin/activate` |
| "Connection refused" | Start OMI server: `./scripts/start_omi_mcp.sh` |
| "Docker not found" | Start Docker Desktop application |
| "Permission denied" | Run: `chmod +x <script-name>` |

---

## 💡 Tips for Success

1. **Always use two terminals**: One for OMI server, one for demos
2. **Check Docker Desktop** is running before starting
3. **Activate virtual environment** in new terminal windows
4. **Read error messages** - they usually tell you what's wrong
5. **Keep the OMI server running** while running demos

---

## 🎓 For Instructors

### Classroom Setup Checklist
- [ ] Docker Desktop installed on all machines
- [ ] Python 3.11+ installed
- [ ] Internet connection for package downloads
- [ ] Test API keys working
- [ ] UV package manager installed

### Time Estimates
- Initial setup: 15-20 minutes
- Running first demo: 5 minutes
- Explaining architecture: 10-15 minutes
- Troubleshooting buffer: 10 minutes

### Common Student Issues
1. Forgetting to activate virtual environment (80% of issues)
2. Docker Desktop not running (10% of issues)
3. Wrong directory when running commands (10% of issues)

---

## 📞 Getting Help

```bash
# 1. Check the guides
ls docs/guides/

# 2. Read the student guide
open STUDENT_GUIDE.md  # Mac
start STUDENT_GUIDE.md # Windows

# 3. Test your setup
python scripts/test_omi_connection.py
```

---

*Remember: Copy-paste commands to avoid typos! 📋*