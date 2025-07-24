# 🎓 OMI + Multi-Agent AI Demo - Instructor Presentation

## 📊 Presentation Overview

**Duration**: 45-60 minutes  
**Audience**: Computer Science / AI students  
**Prerequisites**: Basic programming knowledge

---

## 🎯 Learning Objectives

By the end of this session, students will:
1. Understand multi-agent AI systems and their advantages
2. Learn how wearable AI devices can integrate with software systems
3. Experience hands-on deployment of AI agents
4. Appreciate modular architecture in AI applications

---

## 📋 Session Outline

### Part 1: Introduction (10 minutes)
- What are multi-agent systems?
- Real-world applications
- Today's demo overview

### Part 2: Architecture Deep Dive (15 minutes)
- OMI device and its capabilities
- Agent specialization concept
- A2A protocol explained

### Part 3: Live Demo (20 minutes)
- Running the simple demo
- Code walkthrough
- Modifying the demo

### Part 4: Discussion & Q&A (15 minutes)
- Potential applications
- Challenges and limitations
- Future directions

---

## 🖼️ Slide 1: Title Slide

# Multi-Agent AI Systems
## Building the Future of Collaborative AI

**Demo**: OMI Wearable + A2A Protocol  
**Instructor**: [Your Name]  
**Date**: [Today's Date]

---

## 🖼️ Slide 2: The Problem

### Traditional AI Approach
```
User → Single AI Model → Response
```

**Limitations**:
- One model must be good at everything
- Difficult to scale
- Hard to maintain and update
- Single point of failure

---

## 🖼️ Slide 3: Multi-Agent Solution

### Multi-Agent Approach
```
         ┌─────────────┐
User ───►│ Orchestrator│
         └──────┬──────┘
                │
    ┌───────────┼───────────┐
    ▼           ▼           ▼
┌─────────┐ ┌─────────┐ ┌─────────┐
│ Agent 1 │ │ Agent 2 │ │ Agent 3 │
│(Context)│ │(Actions)│ │(Comms)  │
└─────────┘ └─────────┘ └─────────┘
```

**Benefits**:
- Specialized agents for specific tasks
- Easy to add new capabilities
- Fault tolerance
- Parallel processing

---

## 🖼️ Slide 4: Real-World Example

### Meeting Assistant Scenario

**Input**: 30-minute team meeting recording

**Agent Breakdown**:
1. **Transcription Agent**: Converts speech to text
2. **Context Agent**: Identifies meeting type, participants
3. **Action Agent**: Extracts todo items and decisions
4. **Calendar Agent**: Schedules follow-ups
5. **Email Agent**: Sends meeting summary

Each agent is an expert in ONE thing!

---

## 🖼️ Slide 5: OMI Device

### The Hardware Component

```
┌─────────────────┐
│   OMI Device    │
│  ┌───────────┐  │
│  │ Microphone │  │──── Bluetooth ────►
│  └───────────┘  │
│  ┌───────────┐  │
│  │ Processor │  │
│  └───────────┘  │
└─────────────────┘
```

**Features**:
- Wearable form factor (pendant/glasses)
- Real-time audio capture
- Bluetooth connectivity
- 24-hour battery life
- Privacy-first design

---

## 🖼️ Slide 6: A2A Protocol

### Agent-to-Agent Communication

**What is A2A?**
- Standardized protocol for AI agent communication
- Like HTTP for web, but for AI agents
- Enables agent discovery and collaboration

**Key Concepts**:
```python
# Agent announces its capabilities
capabilities = [
    "extract_actions",
    "analyze_sentiment",
    "summarize_text"
]

# Agents can discover each other
available_agents = discover_agents()

# Agents can delegate tasks
result = await agent.send_task(
    to="action_agent",
    task="extract_actions",
    data=transcript
)
```

**Note**: MCP (Model Context Protocol) is OMI's official API for memory and conversation management

---

## 🖼️ Slide 7: Architecture Diagram

### Complete System Architecture

```
┌─────────────┐     ┌─────────────────┐     ┌──────────────────┐
│ OMI Device  │────►│  Gateway Agent  │────►│ Context Analysis │
│ (Wearable)  │     │  (Port 8000)   │     │   (Port 8001)    │
└─────────────┘     └────────┬────────┘     └──────────────────┘
                             │
                             │               ┌──────────────────┐
                             ├──────────────►│ Action Planning  │
                             │               │   (Port 8002)    │
                             │               └──────────────────┘
                             │
                             │               ┌──────────────────┐
                             └──────────────►│ Communication    │
                                            │   (Port 8003)    │
                                            └──────────────────┘
```

---

## 🖼️ Slide 8: Demo Time!

### Live Demonstration

**Step 1**: Start OMI Server
```bash
./scripts/start_omi_mcp.sh
```

**Step 2**: Run Simple Demo
```bash
uv run python demo_simple.py
```

**Step 3**: Examine Output
- Connection confirmation
- Simulated agent responses
- Action items extracted

---

## 🖼️ Slide 9: Code Walkthrough

### Key Components

**1. OMI Connection**:
```python
# Connect to OMI MCP server
async with MCPClient(server_url, api_key) as client:
    # Process conversation
    result = await client.process_transcript(text)
```

**2. Agent Simulation**:
```python
# Simulate multi-agent analysis
agents = {
    "context": analyze_context,
    "actions": extract_actions,
    "knowledge": find_relevant_info
}
```

**3. Results Aggregation**:
```python
# Combine results from all agents
final_analysis = combine_agent_results(results)
```

---

## 🖼️ Slide 10: Hands-On Activity

### Student Exercise

**Task**: Modify the demo to analyze a different conversation

1. Open `demo_simple.py`
2. Find the `SAMPLE_TRANSCRIPT` variable
3. Replace with your own conversation
4. Run the demo again
5. Observe how agents adapt

**Discussion Questions**:
- What types of conversations work best?
- What limitations did you notice?
- How would you improve the agents?

---

## 🖼️ Slide 11: Real-World Applications

### Where Multi-Agent AI Shines

**Healthcare**:
- Patient monitoring agent
- Medication reminder agent
- Emergency detection agent

**Education**:
- Note-taking agent
- Question extraction agent
- Study guide creation agent

**Business**:
- Meeting summarization
- Task management
- Customer service routing

**Personal Productivity**:
- Calendar management
- Email drafting
- Research assistance

---

## 🖼️ Slide 12: Challenges & Limitations

### Current Limitations

**Technical Challenges**:
- Agent coordination complexity
- Network latency between agents
- Standardization needs

**Practical Challenges**:
- Privacy concerns with always-on devices
- Battery life constraints
- Cost of running multiple AI models

**Ethical Considerations**:
- Data ownership
- Consent in conversations
- Potential for misuse

---

## 🖼️ Slide 13: Future Directions

### What's Next?

**Near Term (1-2 years)**:
- More specialized agents
- Better inter-agent communication
- Edge computing integration

**Medium Term (3-5 years)**:
- Autonomous agent orchestration
- Cross-platform agent markets
- Standardized protocols

**Long Term (5+ years)**:
- AGI-level coordination
- Swarm intelligence
- Brain-computer interfaces

---

## 🖼️ Slide 14: Key Takeaways

### Remember These Points

1. **Specialization > Generalization**
   - Many focused agents beat one general agent

2. **Modularity Enables Innovation**
   - Easy to add new capabilities

3. **Standards Enable Ecosystems**
   - A2A protocol allows interoperability

4. **Privacy Must Be Built-In**
   - Not an afterthought

5. **The Future is Collaborative**
   - AI agents working together, not alone

---

## 🖼️ Slide 15: Resources & Next Steps

### Continue Learning

**Documentation**:
- OMI Docs: https://docs.omi.me
- A2A Spec: https://a2a-project.github.io

**Tutorials**:
- Build Your First Agent: `/docs/guides/create-agent.md`
- A2A Protocol Deep Dive: `/docs/guides/a2a-protocol.md`

**Community**:
- Discord: [Join Link]
- GitHub: [Repository]

**Your Assignment**:
- Design a multi-agent system for a problem in your field
- Identify what agents you'd need
- Draw the architecture diagram

---

## 📝 Instructor Notes

### Before Class
1. Test the demo on the classroom computer
2. Ensure Docker Desktop is running
3. Have backup slides ready if demo fails
4. Prepare 2-3 conversation examples

### During Class
1. Start Docker before the presentation
2. Have two terminal windows ready
3. Keep `demo_simple.py` open in editor
4. Monitor student progress during hands-on

### Common Student Questions

**Q: Why not use one powerful AI model?**
A: Specialization allows for better performance, easier updates, and fault tolerance. Think of it like a hospital - you want specialists, not just general practitioners.

**Q: How do agents discover each other?**
A: The A2A protocol includes a discovery mechanism where agents announce their capabilities and can query for available services.

**Q: What about privacy?**
A: OMI processes audio locally when possible, uses encryption for transmission, and allows users to control what data is shared.

**Q: Can I build my own agent?**
A: Yes! Check the create-agent guide. You just need to implement the A2A protocol interface.

### Troubleshooting Tips

**If Docker won't start**:
- Use the simple demo only
- Explain Docker conceptually
- Show pre-recorded demo video

**If students have different OS**:
- Focus on Mac/Windows primarily
- Have Linux commands ready
- Pair students with same OS

**If API errors occur**:
- Explain these are normal in development
- Focus on the successful parts
- Discuss error handling in production

### Assessment Ideas

1. **Quiz Questions**:
   - What are the advantages of multi-agent systems?
   - Name three types of agents in our demo
   - What does A2A stand for?

2. **Project Ideas**:
   - Design a multi-agent system for campus safety
   - Create an agent for student study groups
   - Propose new agent types for OMI

3. **Discussion Topics**:
   - Ethics of always-on recording devices
   - Privacy vs. convenience trade-offs
   - Future of human-AI collaboration

---

## 🎬 Demo Script

### Opening (2 minutes)
"Today we're exploring how AI agents can work together like a team. Instead of one AI trying to do everything, we'll see how specialized agents collaborate to analyze conversations from a wearable device."

### Technical Demo (10 minutes)
1. "First, let's start the OMI server - this simulates the wearable device backend"
2. "Now we'll run our demo that connects to this server"
3. "Notice how different agents analyze different aspects"
4. "Let's modify the conversation and see what happens"

### Code Review (5 minutes)
1. "Here's how we connect to the OMI server"
2. "This section simulates our different agents"
3. "Notice the modular structure - easy to add new agents"

### Closing (3 minutes)
"We've seen how breaking down AI tasks into specialized agents creates a more flexible, scalable system. Think about how you might apply this pattern to problems in your field of study."

---

## 📊 Additional Resources

### Presentation Assets
- Download slides: `docs/slides/multi-agent-demo.pptx`
- Demo video backup: `docs/videos/demo-backup.mp4`
- Student handout: `STUDENT_QUICK_REFERENCE.md`

### Extension Activities
1. Compare with single-agent approach
2. Design custom agents for specific domains
3. Implement a simple agent using the template

### Related Topics to Explore
- Distributed systems
- Microservices architecture
- Edge computing
- Federated learning

---

*Remember: The goal is to inspire students about the possibilities of collaborative AI, not to overwhelm them with technical details. Keep it engaging and interactive!*