# 🚀 OMI Multi-Agent Demo - Quick Reference Card

## 🎯 Essential Commands

### Setup (One Time Only)
```bash
# 1. Clone the repository
git clone https://github.com/YourRepo/omi.git
cd omi/a2a-demo

# 2. Install UV package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# 3. Install dependencies
uv venv
uv pip install -e ".[dev]"

# 4. Configure API keys
cp .env.example .env.local
```

### Running the Demo
```bash
# Terminal 1: Start OMI Server
./scripts/start_omi_mcp.sh

# Terminal 2: Run Demo
uv run python demo_simple.py
```

## 🔧 Common Fixes

| Problem | Solution |
|---------|----------|
| `venv/bin/activate not found` | Use `uv run python` instead |
| `Connection refused` | Start OMI server first |
| `Module not found` | Make sure you're in `a2a-demo` folder |
| `Permission denied` | Run `chmod +x scripts/*.sh` |

## 🏗️ Architecture

```
OMI Device → Gateway Agent → Multiple Specialized Agents
                ↓
    ┌───────────┴───────────┐
    │                       │
Context Agent        Action Agent
(What's happening?)  (What needs doing?)
```

## 📁 Key Files

- `demo_simple.py` - Main demo script
- `.env.local` - Your configuration
- `agents/` - Individual agent code
- `scripts/` - Helper scripts

## 💡 Quick Tips

1. **Always start OMI server first**
2. **Use UV for all Python commands**: `uv run python [file]`
3. **Keep Docker Desktop running**
4. **Check you're in the right directory**: `pwd` should show `.../a2a-demo`

## 🎓 Learning Path

1. Run the simple demo ✓
2. Modify the conversation transcript
3. Explore individual agent code
4. Try creating your own agent
5. Build something amazing!

---
*Need help? Check STUDENT_GUIDE.md for detailed instructions*