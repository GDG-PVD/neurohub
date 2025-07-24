# 🎯 Working Demo Commands - Quick Summary

## What's Currently Working

### ✅ Simple Demo (Fully Working)
This demonstrates the OMI connection and simulates multi-agent analysis:

```bash
# Terminal 1: Start OMI Server
./scripts/start_omi_mcp.sh

# Terminal 2: Run Demo
uv run python demo_simple.py
```

**Output**: Shows successful OMI connection and simulated agent analysis

### ⚠️ Full Multi-Agent Demo (Docker Issues)
The full Docker-based multi-agent system has some startup issues. For classroom demos, use the simple demo above.

## Common Student Errors & Quick Fixes

| Error | Quick Fix |
|-------|-----------|
| `venv/bin/activate not found` | Use: `uv run python demo_simple.py` |
| `Module not found` | Make sure you're in the right directory: `cd a2a-demo` |
| `Connection refused` | Start OMI server: `./scripts/start_omi_mcp.sh` |

## For Instructors

### Classroom Demo Script (5 minutes)
1. **Show OMI Server Starting** (Terminal 1):
   ```bash
   ./scripts/start_omi_mcp.sh
   ```
   - Explain: "This simulates the wearable device backend"

2. **Run Simple Demo** (Terminal 2):
   ```bash
   uv run python demo_simple.py
   ```
   - Walk through each output section
   - Explain what each "agent" would do

3. **Modify the Demo**:
   - Open `demo_simple.py`
   - Change the conversation transcript
   - Run again to show different results

### Key Teaching Points
- OMI device captures conversations
- Multiple AI agents analyze different aspects
- Each agent specializes in one task
- They work together through the A2A protocol

### If Docker Works Later
Once Docker issues are resolved:
```bash
docker-compose up  # Starts all agents
uv run python demo/scenarios/meeting_assistant.py  # Full demo
```

---

**Remember**: The simple demo (`demo_simple.py`) is sufficient to demonstrate all concepts! The Docker complexity can be discussed conceptually.