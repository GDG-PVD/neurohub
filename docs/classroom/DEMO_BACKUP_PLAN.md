# 🚨 Demo Backup Plan - When Things Go Wrong

## 🎯 Quick Decision Tree

```
Is Docker running?
├─ NO → Use Backup Plan A (Simple Demo Only)
└─ YES → Is OMI server starting?
    ├─ NO → Use Backup Plan B (Mock Server)
    └─ YES → Is demo connecting?
        ├─ NO → Use Backup Plan C (Connection Issues)
        └─ YES → Continue with main demo
```

## 📋 Backup Plan A: No Docker

### What to do:
1. Focus on conceptual explanation
2. Show code structure
3. Use pre-recorded demo video

### Script:
```python
# Show this code and explain each part
print("🎯 Multi-Agent System Simulation")
print("\n1. OMI Device captures audio")
print("2. Gateway Agent receives transcript")
print("3. Context Agent analyzes: Meeting about Q4 planning")
print("4. Action Agent extracts: 3 todo items found")
print("5. Communication Agent: Sending summary email")
```

### Key Points to Cover:
- Agent specialization benefits
- Modular architecture
- Real-world applications

## 📋 Backup Plan B: OMI Server Won't Start

### Quick Fix Attempt (30 seconds):
```bash
# Try direct Docker command
docker run -d -p 8000:8000 omi-mcp:latest

# Or use mock server
uv run python scripts/mock_omi_server.py
```

### If that fails:
Create a mock server file quickly:

```python
# mock_demo.py
print("🚀 Mock OMI Multi-Agent Demo")
print("\nSimulating agent responses...")

agents = {
    "Context Analysis": "Team meeting about project deadline",
    "Action Items": ["Review code", "Update docs", "Deploy v2"],
    "Sentiment": "Positive, collaborative"
}

for agent, result in agents.items():
    print(f"\n{agent}: {result}")
```

## 📋 Backup Plan C: Connection Issues

### Common Fixes (try in order):

1. **Port conflict**:
```bash
# Check if port 8000 is in use
lsof -i :8000
# Kill the process if needed
kill -9 [PID]
```

2. **Wrong API key**:
```bash
# Use the default test key
export OMI_API_KEY=omi_mcp_test_key_12345
```

3. **Network issues**:
```bash
# Try localhost instead of 127.0.0.1
export OMI_API_URL=http://localhost:8000
```

## 🎬 Pre-Recorded Demo Option

### Have ready:
- Screenshot of successful demo output
- 2-minute screen recording
- Backup slides with output examples

### Narration script:
"Let me show you what this looks like when running properly. Here we can see the OMI server starting up, and now we're connecting from our demo script..."

## 💡 Interactive Alternatives

### Option 1: Code Review Session
- Open `demo_simple.py` in editor
- Walk through code line by line
- Ask students to predict output

### Option 2: Whiteboard Architecture
- Draw the system architecture
- Have students design their own agents
- Discuss use cases

### Option 3: Group Exercise
```python
# Have students write pseudo-code for an agent
class StudentAgent:
    def analyze_lecture(self, transcript):
        # What would you extract?
        # - Key concepts?
        # - Homework assignments?
        # - Exam dates?
        pass
```

## 🛠️ Emergency Fixes

### Fix 1: Python Environment
```bash
# If UV isn't working, try pip directly
python -m pip install mcp-client httpx rich
```

### Fix 2: Manual Demo
```python
# Copy-paste this into Python REPL
import asyncio

async def demo():
    print("🤖 Multi-Agent Demo (Manual)")
    await asyncio.sleep(1)
    print("✅ Agent 1: Context understood")
    await asyncio.sleep(1)
    print("✅ Agent 2: Actions extracted")
    await asyncio.sleep(1)
    print("✅ Agent 3: Summary generated")

asyncio.run(demo())
```

### Fix 3: Use Online Playground
- replit.com/new/python3
- Copy the simple demo code
- Run in browser (no local setup needed)

## 📝 Minimum Viable Demo

If all else fails, this 5-minute talk covers the essentials:

1. **Concept** (2 min):
   - "Imagine Siri, but instead of one AI, it's a team"
   - "Each team member is an expert"
   - "They work together to help you"

2. **Architecture** (2 min):
   - Draw on whiteboard
   - Show specialization
   - Explain benefits

3. **Applications** (1 min):
   - Healthcare monitoring
   - Educational assistance
   - Business productivity

## ✅ Success Metrics

Even if the technical demo fails, ensure students understand:
- [ ] What multi-agent systems are
- [ ] Why they're better than single agents
- [ ] How agents communicate (A2A protocol)
- [ ] Real-world applications
- [ ] The potential of this technology

## 🎯 Remember

**The goal is inspiration, not perfection!**

Students will remember:
- Your enthusiasm about the technology
- The big picture concepts
- The potential applications

They won't remember:
- Minor technical glitches
- Exact command syntax
- Perfect demo execution

## 💬 Backup Discussion Questions

Use these if you need to fill time:

1. "What agents would you add to make this system better?"
2. "What privacy concerns might users have?"
3. "How could this technology help in your field of study?"
4. "What's the difference between this and ChatGPT?"
5. "What challenges do you see in building this?"

---

*"The best teachers are those who show you where to look but don't tell you what to see." - Keep inspiring!*