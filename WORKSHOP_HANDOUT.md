# 🧠 NeuroHub Workshop - Quick Start

Welcome to the Multi-Agent AI Workshop! This guide gets you coding in 5 minutes.

## 🚀 Setup (One Time)

### 1. Clone the Repository
```bash
git clone git@github.com:GDG-PVD/neurohub.git
cd neurohub
```

### 2. Install Dependencies
```bash
# Install UV if needed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Python packages
uv venv
uv pip install -e ".[dev]"
```

### 3. Configure Backend Access
```bash
# Create your config file
cp .env.example .env.local

# Add these lines to .env.local:
OMI_API_BASE_URL=https://neurohub-workshop.fly.dev
OMI_API_KEY=neurohub_workshop_2024
```

## 🎮 Running the Demo

```bash
# Test the connection
uv run python scripts/test_omi_connection.py

# Run the simple demo
uv run python demo_simple.py
```

## 🏗️ Workshop Tasks

### Task 1: Understand the Architecture
Look at `demo_simple.py` and identify:
- How it connects to OMI
- What agents are simulated
- How results are displayed

### Task 2: Modify the Conversation
Change the sample transcript in `demo_simple.py`:
- Try a different type of conversation
- See how agent responses change
- Think about what each agent extracts

### Task 3: Add Your Own Agent
Create a new analysis type:
- Sentiment analysis
- Topic extraction  
- Language detection
- Your creative idea!

### Task 4: Build Something New
Ideas to explore:
- Meeting summarizer
- Study note generator
- Task prioritizer
- Conversation insights

## 📝 Code Examples

### Connect to OMI Backend
```python
from integrations.omi import OMIClient

client = OMIClient(
    api_url="https://neurohub-workshop.fly.dev",
    api_key="neurohub_workshop_2024"
)
```

### Process a Conversation
```python
result = await client.process_transcript(
    "Your conversation text here"
)
```

### Create a Custom Agent
```python
def analyze_emotions(transcript):
    # Your code here
    emotions = ["happy", "curious", "focused"]
    return emotions
```

## 🆘 Need Help?

### Common Issues

**"Connection refused"**
- Check your internet connection
- Verify the URL in .env.local

**"Module not found"**
- Make sure you ran: `uv pip install -e ".[dev]"`
- Are you in the neurohub directory?

**"API key invalid"**
- Check for typos in .env.local
- Ask instructor for current key

### Quick Commands
```bash
# Where am I?
pwd

# What's in this directory?
ls

# View my config
cat .env.local

# Run with UV
uv run python your_script.py
```

## 🎯 Learning Goals

By the end of this workshop, you'll understand:
- ✅ How wearable AI devices work
- ✅ Multi-agent system architecture
- ✅ Real-time conversation processing
- ✅ Building AI-powered applications

## 🔗 Resources

- **Documentation**: See `STUDENT_GUIDE.md`
- **Examples**: Check `demo_simple.py`
- **Architecture**: Read `MCP_VS_A2A_EXPLANATION.md`

---

**Remember**: Focus on understanding concepts, not perfect code. Ask questions and experiment! 🚀