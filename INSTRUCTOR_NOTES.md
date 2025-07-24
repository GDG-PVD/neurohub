# 👨‍🏫 Instructor Notes - OMI Multi-Agent Demo

## 📋 Pre-Class Checklist

### Technical Requirements
- [ ] Verify all machines have Python 3.11+ installed
- [ ] Docker Desktop installed and tested
- [ ] Internet connectivity for package downloads
- [ ] Test the demo on instructor machine
- [ ] Have backup slides ready in case of technical issues

### Materials to Prepare
- [ ] Print copies of `QUICK_REFERENCE.md` for students
- [ ] Have the visual architecture diagrams ready to project
- [ ] Prepare example conversation scenarios
- [ ] Test API keys are working

## 🎯 Learning Objectives

By the end of this session, students will:
1. **Understand** multi-agent AI systems and their advantages
2. **Experience** running a real AI agent system
3. **Analyze** how conversations are processed by specialized agents
4. **Identify** potential applications in their field

## ⏱️ Suggested Timeline (90-minute class)

### Introduction (15 minutes)
1. **Hook** (5 min): "What if you had a team of AI assistants in your pocket?"
2. **Context** (5 min): Wearable AI devices and their potential
3. **Demo preview** (5 min): What we'll build today

### Conceptual Overview (20 minutes)
1. **Traditional AI vs Multi-Agent** (10 min)
   - Use the visual from `ARCHITECTURE_VISUAL.md`
   - Analogy: One person doing everything vs. a specialized team
   
2. **A2A Protocol Introduction** (5 min)
   - "Like a common language for AI agents"
   - Similar to how apps communicate via APIs

3. **OMI Device Explanation** (5 min)
   - Wearable that captures conversations
   - Privacy and consent considerations

### Hands-On Setup (25 minutes)
1. **Environment Setup** (15 min)
   - Follow `STUDENT_GUIDE.md` Step 1-3
   - Common issues: Python version, Docker not running
   
2. **Configuration** (5 min)
   - Setting up `.env.local`
   - Explain API keys briefly

3. **Start Services** (5 min)
   - Start OMI server
   - Verify it's running

### Running the Demo (20 minutes)
1. **Simple Demo** (10 min)
   - Run `demo_simple.py`
   - Walk through the output
   - Explain what each part means

2. **Modify and Experiment** (10 min)
   - Change the conversation in the demo
   - Show how different conversations produce different results
   - Let students try their own conversations

### Discussion & Applications (10 minutes)
1. **Real-world applications**:
   - Healthcare: Doctor-patient conversations
   - Education: Classroom discussions
   - Business: Meeting automation
   
2. **Ethical considerations**:
   - Privacy concerns
   - Consent for recording
   - Data ownership

## 🎓 Teaching Tips

### For Non-Technical Students
- Use analogies liberally (orchestrator = conductor, agents = orchestra members)
- Focus on concepts over code
- Emphasize real-world applications
- Keep terminal commands simple

### Common Stumbling Blocks
1. **Virtual Environment**: 50% of issues
   - Solution: Always remind to activate before running commands
   
2. **Docker Not Running**: 20% of issues
   - Solution: Show Docker Desktop icon in system tray
   
3. **Wrong Directory**: 20% of issues
   - Solution: Use `pwd` command frequently
   
4. **Copy-Paste Errors**: 10% of issues
   - Solution: Encourage exact copy-paste

### Debugging Strategies
```bash
# Quick diagnostic commands
python --version          # Check Python
docker ps                # Check Docker
pwd                      # Check directory
ls                       # List files
cat .env.local          # Check configuration (careful with keys!)
```

## 💡 Advanced Topics (If Time Permits)

### Creating a Custom Agent
Show the basic structure:
```python
class CustomAgent(A2AAgent):
    def __init__(self):
        super().__init__(
            agent_id="custom-agent",
            name="My Custom Agent"
        )
```

### Modifying Agent Behavior
- Show where agent logic lives
- Discuss how to add new capabilities
- Talk about training vs. programming

## 📊 Assessment Ideas

### Quick Understanding Check
Ask students to:
1. Draw the flow of a conversation through the system
2. Identify which agent handles what task
3. Propose a new type of agent and its purpose

### Hands-On Challenge
Have students:
1. Modify the demo conversation
2. Predict what the agents will find
3. Run it and compare results

### Discussion Questions
1. "What other types of conversations could benefit from this?"
2. "What privacy concerns should we consider?"
3. "How might this technology change meetings/classes/healthcare?"

## 🚨 Troubleshooting Guide

### If Demo Won't Start
1. Check Docker: `docker ps`
2. Check Python: `python --version`
3. Check directory: `pwd`
4. Check virtual env: `which python`

### If Connection Fails
1. Is OMI server running? Check first terminal
2. Correct port? Should be 8000
3. Firewall issues? Try `localhost` instead of `127.0.0.1`

### Emergency Backup Plan
If technical issues persist:
1. Use pre-recorded demo video
2. Walk through architecture conceptually
3. Discuss applications and implications
4. Show code structure without running

## 📚 Additional Resources

### For Curious Students
- Point to `docs/guides/development.md`
- Suggest exploring individual agent code
- Recommend A2A protocol documentation

### For Advanced Students
- Challenge: Create a new agent type
- Explore WebSocket real-time features
- Look into AgentDB integration

## 🎯 Key Takeaways to Emphasize

1. **Multi-agent systems are more flexible** than monolithic AI
2. **Specialization leads to better results** (like human teams)
3. **Standards (like A2A) enable interoperability**
4. **Wearable AI is here now**, not science fiction
5. **Privacy and ethics** must be considered

## 📝 Post-Class Follow-Up

### Suggested Homework
1. Read one ADR document and summarize it
2. Propose a new agent type with justification
3. Research one real-world application

### Extended Project Ideas
1. Design a multi-agent system for their field
2. Create a new conversation scenario
3. Write a simple agent (with guidance)

---

## 🎪 Making It Engaging

### Live Demonstrations
- Have students suggest conversations
- Run them live and analyze results
- Show how changing words changes outcomes

### Interactive Elements
- "Pair and share": Discuss applications
- "Think-pair-share": Design new agents
- Quick polls: "Who has used AI before?"

### Storytelling
- Start with a story about forgetting meeting actions
- Use the "team of specialists" narrative throughout
- End with future possibilities

---

*Remember: The goal is to demystify AI agents, not to make everyone a programmer. Focus on concepts, applications, and possibilities!* 🚀