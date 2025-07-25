# NeuroHub Workshop: 2-Week AI Agent Hackathon

## 🎯 Workshop Overview

**Format**: 2-week hackathon with 20 students in 5 teams  
**Equipment**: Each team gets 1 OMI device  
**Goal**: Build innovative AI agent applications using OMI's open-source platform

## 🚀 What You'll Build

Teams will extend the OMI device with AI agents that solve real-world problems using:
- **MCP (Model Context Protocol)** for LLM integration
- **A2A Protocol** for agent communication
- **Real APIs** like FutureHouse for specialized capabilities
- **OMI SDK** for device integration

## 📋 Workshop Structure

### Week 1: Foundation & Exploration
- Day 1-2: Platform overview, team formation, use case selection
- Day 3-4: Agent architecture, MCP/A2A protocols
- Day 5: API integrations, build first functional agent

### Week 2: Build & Demo
- Day 6-8: Rapid development, agent collaboration
- Day 9: Testing, refinement, documentation
- Day 10: Demo day & presentations

## 🛠️ Technical Stack

### Core Platform
- **OMI Device**: Capture conversations and context
- **NeuroHub Gateway**: Orchestrate agent communication
- **Agent Framework**: Build on our A2A/MCP templates

### Available APIs & Services
1. **FutureHouse Platform** - Scientific research agents
2. **Mem0** - Memory and context storage
3. **OpenAI/Claude** - General purpose AI
4. **Custom APIs** - Integrate any service you need

## 🎨 Example Use Cases

### 1. Research Assistant (Using FutureHouse)
Help researchers capture ideas and instantly access scientific literature
```python
# Capture research discussion with OMI
# → CROW agent finds relevant papers
# → PHOENIX agent suggests molecular structures
# → Results saved to team's knowledge base
```

### 2. Medical Consultation Helper
Support doctors with real-time information during patient consultations
```python
# OMI captures symptoms discussion
# → Medical terminology agent extracts key terms
# → Research agent finds latest treatments
# → Privacy-first local processing
```

### 3. Learning Companion
Personalized educational support that adapts to student needs
```python
# Student explains concept they're struggling with
# → Concept analysis agent identifies gaps
# → Teaching agent provides explanations
# → Progress tracked over time
```

### 4. Team Collaboration Tool
Enhance team meetings with AI-powered insights
```python
# OMI records team standup
# → Action extraction agent identifies tasks
# → Priority agent suggests focus areas
# → Integration with project management
```

### 5. Mental Health Support
Provide gentle, privacy-focused emotional support
```python
# User shares daily reflections
# → Mood pattern agent tracks trends
# → Wellness agent suggests activities
# → All processing stays local
```

## 🏗️ Agent Development Framework

### 1. Basic Agent Template
```python
from core.a2a_client import A2AAgent
from integrations.mcp_client import MCPClient

class YourCustomAgent(A2AAgent):
    """Template for building your own agent"""
    
    def __init__(self):
        super().__init__(
            name="your-agent",
            capabilities=["analyze", "generate", "search"]
        )
        self.mcp = MCPClient()  # For LLM integration
        
    async def process_task(self, task_data: dict) -> dict:
        # Your agent logic here
        pass
```

### 2. FutureHouse Integration Example
```python
from integrations.futurehouse_client import FutureHouseClient

class ResearchAgent(A2AAgent):
    """Scientific research agent using FutureHouse"""
    
    def __init__(self):
        super().__init__(name="research-agent")
        self.fh_client = FutureHouseClient(api_key=os.getenv("FH_API_KEY"))
        
    async def find_research(self, query: str) -> dict:
        # Use CROW for quick searches
        response = await self.fh_client.run_task({
            "name": "CROW",
            "query": query
        })
        return self.format_research_results(response)
```

### 3. Multi-Agent Workflow
```python
class TeamWorkflow:
    """Orchestrate multiple agents for complex tasks"""
    
    async def analyze_conversation(self, omi_memory):
        # Step 1: Extract key topics
        topics = await self.topic_agent.extract(omi_memory)
        
        # Step 2: Research each topic
        research_tasks = [
            self.research_agent.find_papers(topic)
            for topic in topics
        ]
        research_results = await asyncio.gather(*research_tasks)
        
        # Step 3: Generate insights
        insights = await self.insight_agent.synthesize(
            topics, research_results
        )
        
        return insights
```

## 📚 Resources & Documentation

### Quick Start Commands
```bash
# Clone the workshop repository
git clone https://github.com/GDG-PVD/neurohub.git
cd neurohub

# Set up your team's environment
./scripts/setup_team.sh TEAM_NAME

# Install dependencies
uv pip install -e ".[dev,demo]"

# Configure API keys
cp .env.example .env.local
# Add your FutureHouse, OpenAI, etc. keys

# Run the development server
uv run python workshop_server_enhanced.py

# Test your first agent
uv run python agents/examples/research_agent.py
```

### API Documentation
- **FutureHouse**: [Cookbook](https://futurehouse.gitbook.io/futurehouse-cookbook/)
- **MCP Protocol**: [Spec](https://modelcontextprotocol.io/)
- **A2A Protocol**: See `docs/A2A_PROTOCOL.md`
- **OMI SDK**: See `docs/OMI_SDK.md`

### Development Guides
1. [Building Your First Agent](docs/guides/FIRST_AGENT.md)
2. [Integrating External APIs](docs/guides/API_INTEGRATION.md)
3. [Multi-Agent Workflows](docs/guides/WORKFLOWS.md)
4. [Privacy & Security](docs/guides/SECURITY.md)

## 🏆 Judging Criteria

### Technical Excellence (40%)
- Effective use of MCP/A2A protocols
- Clean agent architecture
- API integration quality
- Code organization

### Innovation (30%)
- Novel use case
- Creative agent combinations
- Unique problem solving

### Impact (20%)
- Real-world applicability
- User experience
- Scalability potential

### Presentation (10%)
- Clear demo
- Documentation
- Team collaboration

## 💡 Tips for Success

### Week 1 Focus
1. **Understand the Stack**: Spend time learning MCP, A2A, and the APIs
2. **Start Simple**: Build one working agent before expanding
3. **Test Early**: Use the OMI device frequently
4. **Document**: Keep notes on what works

### Week 2 Focus
1. **Integrate**: Connect multiple agents for richer functionality
2. **Polish**: Focus on user experience
3. **Optimize**: Ensure good performance
4. **Prepare Demo**: Practice your presentation

### Common Pitfalls to Avoid
- ❌ Trying to build everything from scratch
- ❌ Ignoring privacy/security considerations
- ❌ Not testing with real OMI device data
- ❌ Overcomplicating the architecture

### Best Practices
- ✅ Use existing APIs like FutureHouse
- ✅ Build on provided templates
- ✅ Focus on one strong use case
- ✅ Collaborate with your team

## 🤝 Support & Community

### During the Workshop
- **Slack Channel**: #neurohub-hackathon
- **Office Hours**: Daily 2-3 PM
- **Mentors**: Assigned to each team

### Resources
- **Agent Gallery**: See working examples
- **API Playground**: Test integrations
- **Debug Tools**: Troubleshooting guides

## 🚀 Getting Started Checklist

### Day 1
- [ ] Form your team (4 people)
- [ ] Receive your OMI device
- [ ] Set up development environment
- [ ] Run the example agents
- [ ] Brainstorm use cases

### Day 2
- [ ] Select your primary use case
- [ ] Design agent architecture
- [ ] Set up API accounts (FutureHouse, etc.)
- [ ] Create team repository

### Day 3
- [ ] Build your first agent
- [ ] Test with OMI device
- [ ] Integrate one external API
- [ ] Document your approach

## 📝 Deliverables

By the end of the workshop, each team should have:

1. **Working Prototype**
   - At least 2 functional agents
   - OMI device integration
   - External API usage

2. **Documentation**
   - README with setup instructions
   - Architecture diagram
   - API documentation

3. **Demo Video** (3-5 minutes)
   - Problem statement
   - Solution overview
   - Live demonstration
   - Future potential

4. **Source Code**
   - Clean, commented code
   - Tests where applicable
   - Deployment instructions

## 🎯 Example: Research Team Starter

Here's a complete example to get you started:

```python
# research_team_agent.py
import os
from datetime import datetime
from core.a2a_client import A2AAgent
from integrations.futurehouse_client import FutureHouseClient
from integrations.omi_connector import OMIConnector

class ResearchTeamAgent(A2AAgent):
    """Helps research teams capture and explore ideas"""
    
    def __init__(self):
        super().__init__(
            name="research-team-agent",
            capabilities=["capture", "research", "synthesize"]
        )
        self.omi = OMIConnector()
        self.fh = FutureHouseClient(api_key=os.getenv("FH_API_KEY"))
        
    async def process_conversation(self, omi_memory):
        # Extract research questions from conversation
        questions = await self.extract_research_questions(omi_memory)
        
        # Research each question
        research_results = []
        for question in questions:
            result = await self.fh.run_task({
                "name": "CROW",
                "query": question
            })
            research_results.append(result)
        
        # Synthesize findings
        synthesis = await self.synthesize_findings(
            questions, research_results
        )
        
        # Save to team knowledge base
        await self.save_to_knowledge_base(synthesis)
        
        return synthesis

# Run the agent
if __name__ == "__main__":
    agent = ResearchTeamAgent()
    agent.run()
```

## 🎉 Let's Build Something Amazing!

Remember: The goal is to show how OMI + AI Agents can solve real problems. Focus on building something functional that demonstrates the platform's potential.

**Questions?** Ask in #neurohub-hackathon or during office hours.

**Ready?** Let's hack! 🚀