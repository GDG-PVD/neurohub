# ☁️ Cloud Quick Start - NeuroHub (No Docker Required!)

This guide gets you running with NeuroHub using cloud services - no Docker or complex setup needed!

## 🚀 5-Minute Setup

### 1. Install UV (if not already installed)
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Install Dependencies
```bash
cd /Users/stephenszermer/Dev/neurohub
uv venv
uv pip install -e ".[dev]"
```

### 3. Run the Demo
```bash
uv run python demo_simple.py
```

That's it! The demo will:
- ✅ Connect to cloud OMI backend
- ✅ Process sample conversations
- ✅ Show multi-agent analysis

## 🧪 Test Your APIs

### Test Airtable Integration
```bash
uv run python scripts/test_airtable_integration.py
```

### Test Research APIs
```bash
uv run python -c "
import os
from dotenv import load_dotenv
load_dotenv('.env.local')

# Test OpenAI
api_key = os.getenv('OPENAI_API_KEY')
print(f'✅ OpenAI API Key: {"Configured" if api_key else "Missing"}')

# Test other APIs
apis = ['GEMINI_API_KEY', 'PUBMED_API_KEY', 'FUTUREHOUSE_API_KEY']
for api in apis:
    key = os.getenv(api)
    print(f'✅ {api}: {"Configured" if key else "Missing"}')
"
```

## 📊 Using Airtable

Your data is stored in Airtable base: `app32q1DcjeioyeaO`

1. **View your data**: [Open in Airtable](https://airtable.com/app32q1DcjeioyeaO)
2. **Create tables** (if not exists):
   - Conversations
   - Actions
   - Knowledge

## 🎯 Common Tasks

### Process a Conversation
```python
# demo_conversation.py
from integrations.omi_connector import OmiConnector
from integrations.airtable_connector import AirtableConnector, AirtableConfig
import asyncio

async def process_conversation():
    # Connect to services
    omi = OmiConnector("https://neurohub-workshop.fly.dev")
    airtable = AirtableConnector(AirtableConfig.from_env())
    
    # Process conversation
    result = await omi.process_audio(b"sample audio data")
    
    # Save to Airtable
    conv_id = await airtable.save_conversation({
        "timestamp": result["timestamp"],
        "summary": "Sample conversation processed",
        "topics": ["demo", "test"]
    })
    
    print(f"✅ Saved conversation: {conv_id}")

asyncio.run(process_conversation())
```

### Extract Action Items
```python
# extract_actions.py
from demo_simple import extract_action_items

text = "John needs to send the report by Friday. Sarah will review the code tomorrow."
actions = extract_action_items(text)

for action in actions:
    print(f"📋 {action}")
```

## 🔧 Configuration

All settings are in `.env.local`:
- ✅ Cloud OMI backend (no Docker needed)
- ✅ Airtable integration configured
- ✅ All API keys ready

## 📱 Using with OMI Device

When you have an actual OMI device:
1. Configure device to use: `https://neurohub-workshop.fly.dev`
2. Use API key: Your OMI API key from `.env.local`
3. Conversations automatically flow to your agents

## 🚫 No Longer Needed

With cloud setup, you DON'T need:
- ❌ Docker Desktop
- ❌ Local MCP server
- ❌ Complex networking setup
- ❌ Container management

## 💡 Tips

1. **Monitor Usage**: Check API usage for OpenAI, Airtable
2. **Rate Limits**: Cloud backend handles rate limiting
3. **Security**: Never commit `.env.local` to git

## 🆘 Troubleshooting

### "Connection refused"
- Cloud backend is always available
- Check your internet connection
- Verify `.env.local` exists

### "API key invalid"
- Check key in `.env.local`
- Ensure no extra spaces
- Verify key permissions

## 🎉 Next Steps

1. **Customize agents** in `agents/*/agent.py`
2. **Build dashboards** in Airtable
3. **Add new integrations** in `integrations/`
4. **Deploy your own** cloud backend

Enjoy building with NeuroHub - now simpler than ever! 🚀