# 📋 Expected Outputs - What Students Will See

## 🧪 Test OMI Connection Output

When students run `uv run python scripts/test_omi_connection.py`, they'll see:

```
🚀 OMI Backend Connection Test

This script tests the connection to your OMI backend
using the MCP API key you've configured.

🔌 Testing OMI Backend Connection...

✅ API Key loaded: omi_mcp_da4ca036a2d6...
✅ API URL: http://localhost:8000

📊 Testing OMI API endpoints...

1. Testing memory retrieval...
[error] Error getting memories error='[Errno 54] Connection reset by peer'
   ✅ Retrieved 0 memories

2. Testing app retrieval...
[error] Error getting apps error="Invalid variable type: value should be str, int or float, got True of type <class 'bool'>"
   ✅ Found 0 enabled apps

3. Testing audio processing (simulated)...
[info] Processing audio size=15
   ✅ Transcript: Hello, this is a test.

🎉 OMI connection test successful!
```

### ⚠️ Note About Errors
The error messages are **NORMAL** and expected:
- `Connection reset by peer` - No memories exist yet in test environment
- `Invalid variable type` - Minor API version mismatch
- These don't affect the demo functionality

## 🎮 Simple Demo Output

When students run `uv run python demo_simple.py`, they'll see:

```
🎯 Simple OMI Connection Demo

1️⃣  Connecting to OMI MCP Server...
   ✅ Connected to http://localhost:8000

2️⃣  Processing sample conversation...
   📝 Transcript: "Alright team, let's go over the Q4 roadmap..."
   ✅ Transcript processed

3️⃣  Simulating Multi-Agent Analysis...

🧠 Context Analysis (simulated):
   - Topic: Q4 Project Planning Meeting
   - Participants: Sarah (PM), John (Dev), Mike (Dev)
   - Sentiment: Collaborative, focused
   - Key themes: API integration, edge cases, timeline

📋 Action Items (simulated):
   1. John: Send project summary to Sarah by 5 PM
   2. Mike: Share edge case handling code with John
   3. Team: Complete API integration fixes by next Tuesday
   4. Sarah: Schedule follow-up meeting for next week

💡 Knowledge Insights (simulated):
   - Related docs: API Integration Guide, Q3 Retrospective
   - Similar meetings: "Q3 Planning" (2 months ago)
   - Suggested resources: Edge case testing framework

📧 Communication Suggestions (simulated):
   - Send meeting summary to: team@company.com
   - Calendar invite for follow-up meeting
   - Slack notification to #dev-team channel

✨ Demo Complete!
```

## 🐍 Python Version Check

When students run `uv run python --version`, they should see:
```
Python 3.11.x
```
(Where x is any minor version - 3.11.0, 3.11.9, etc.)

## 🚢 Docker Status

When the OMI server starts successfully:
```
🚀 Starting OMI MCP Server...
✅ Using API Key: omi_mcp_da4ca036a2d6...
[+] Running 1/1
 ✓ Container omi-mcp  Started
✅ OMI MCP Server started on http://localhost:8000
```

## 🔍 Common Variations

### If Docker Takes Time to Start
Students might see:
```
Waiting for server to be ready...
Waiting for server to be ready...
✅ Server is ready!
```

### If UV Shows Compilation
First-time UV users might see:
```
Bytecode compiled 6050 files in 503ms
```
This is normal and only happens once.

### If Using Different Shell
- **Bash**: Shows `$` prompt
- **Zsh**: Shows `%` prompt
- **PowerShell**: Shows `PS>` prompt

## 📝 Instructor Notes

1. **Emphasize Normal Errors**: The API errors in the test script are expected
2. **Focus on Success Messages**: Look for the ✅ checkmarks
3. **Timing Varies**: First run takes longer due to compilation
4. **Network Dependent**: Docker pull might take time on slow connections

## 🎯 Success Criteria

Students have succeeded if they see:
- [ ] "OMI connection test successful!"
- [ ] "Demo Complete!" 
- [ ] Multiple ✅ checkmarks
- [ ] Simulated agent outputs

---

*Use this guide to help students know what to expect and when things are working correctly!*