# 🏗️ Visual Architecture Guide

## System Overview - The Big Picture

```
┌────────────────────────────────────────────────────────────────┐
│                     OMI Multi-Agent System                     │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  👤 Human with OMI Device                                      │
│         │                                                      │
│         ▼                                                      │
│  ┌─────────────┐                                              │
│  │ OMI Wearable│ ─── Audio ──────┐                           │
│  └─────────────┘                 │                           │
│                                  ▼                           │
│  ┌────────────────────────────────────────────┐             │
│  │        🌐 OMI Gateway Agent                 │             │
│  │  "The Orchestra Conductor"                  │             │
│  │  • Receives audio/transcripts               │             │
│  │  • Coordinates other agents                 │             │
│  │  • Returns combined results                 │             │
│  └───────────────┬────────────────────────────┘             │
│                  │                                           │
│     ┌────────────┴────────────┬───────────┬──────────┐     │
│     ▼                         ▼           ▼          ▼     │
│ ┌────────┐             ┌────────┐   ┌────────┐  ┌────────┐ │
│ │Context │             │ Action │   │Knowledge│  │ Comm.  │ │
│ │Analysis│             │Planning│   │  Agent  │  │ Agent  │ │
│ └────────┘             └────────┘   └────────┘  └────────┘ │
│     🧠                      📋           📚          📨     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## How Conversations Flow Through the System

```
1️⃣ CAPTURE
   👤 "Let's meet Thursday to discuss the API changes"
   └─> 🎙️ OMI Device records

2️⃣ TRANSMIT
   🎙️ OMI Device
   └─> 📡 Sends audio to Gateway

3️⃣ ORCHESTRATE
   🌐 Gateway Agent receives audio
   ├─> 🧠 "Hey Context Agent, what's this about?"
   ├─> 📋 "Action Agent, find any tasks!"
   └─> 📚 "Knowledge Agent, any relevant info?"

4️⃣ PROCESS (Parallel)
   🧠 Context: "It's a meeting request about technical work"
   📋 Action: "Task: Schedule meeting for Thursday about API"
   📚 Knowledge: "Last API discussion was 2 weeks ago"

5️⃣ COMBINE & RETURN
   🌐 Gateway combines all responses
   └─> 📱 Sends summary back to user
```

## Agent Communication (A2A Protocol)

```
How Agents Talk to Each Other:

┌─────────────┐     "What can you do?"      ┌─────────────┐
│   Agent A   │ ─────────────────────────> │   Agent B   │
│             │ <───────────────────────── │             │
└─────────────┘   "I can analyze context"  └─────────────┘

┌─────────────┐     "Please analyze this"   ┌─────────────┐
│   Gateway   │ ─────────────────────────> │   Context   │
│             │ <───────────────────────── │   Agent     │
└─────────────┘   "Here's my analysis"     └─────────────┘
```

## Real-World Example Flow

```
Meeting Scenario:

Sarah: "John, can you send me the project summary by 5 PM?"
John: "Sure, I'll include the test results too."

┌────────────────────────────────────────────────┐
│ 1. OMI Device captures this conversation       │
└────────────────────┬───────────────────────────┘
                     ▼
┌────────────────────────────────────────────────┐
│ 2. Gateway Agent receives transcript           │
└────────────────────┬───────────────────────────┘
                     ▼
        ┌────────────┴────────────┐
        ▼                         ▼
┌─────────────────┐      ┌─────────────────┐
│ Context Agent   │      │ Action Agent    │
│ Finds:          │      │ Finds:          │
│ • 2 participants│      │ • Task for John │
│ • Work topic    │      │ • Due: 5 PM     │
│ • Positive tone │      │ • Deliverable:  │
└─────────────────┘      │   summary+tests │
                         └─────────────────┘
                     ▼
┌────────────────────────────────────────────────┐
│ 3. Combined Result:                            │
│ 📊 Meeting Analysis:                           │
│ • Participants: Sarah (requestor), John        │
│ • Topic: Project status                        │
│ • Action: John to send summary by 5 PM        │
└────────────────────────────────────────────────┘
```

## Component Details

### 🎙️ OMI Device
- **What**: Wearable AI device
- **Does**: Records conversations
- **Output**: Audio stream → Gateway

### 🌐 Gateway Agent (Port 8001)
- **What**: Main coordinator
- **Does**: Orchestrates all other agents
- **Like**: A project manager delegating tasks

### 🧠 Context Analysis Agent (Port 8002)
- **What**: Understanding specialist
- **Does**: Figures out conversation meaning
- **Finds**: Topics, participants, sentiment

### 📋 Action Planning Agent (Port 8003)
- **What**: Task extractor
- **Does**: Finds todos and deadlines
- **Output**: Structured action items

### 📚 Knowledge Agent (Port 8004)
- **What**: Information retriever
- **Does**: Finds relevant past info
- **Like**: Your personal assistant's memory

### 📨 Communication Agent (Port 8005)
- **What**: Message sender
- **Does**: Drafts and sends follow-ups
- **Output**: Emails, messages, notifications

## Benefits of Multi-Agent Architecture

```
❌ Traditional: One Big AI              ✅ Multi-Agent: Specialized Team

┌─────────────────────┐                ┌──────┐ ┌──────┐ ┌──────┐
│                     │                │Agent1│ │Agent2│ │Agent3│
│   Monolithic AI     │   vs.          └──┬───┘ └──┬───┘ └──┬───┘
│   (Jack of all      │                   └────────┼────────┘
│    trades)          │                        Coordinator
└─────────────────────┘

Problems:                              Benefits:
• Hard to update                       • Easy to add new agents
• Single point of failure              • Fault tolerant
• Resource intensive                   • Efficient specialists
• Difficult to scale                   • Highly scalable
```

## Technical Flow Diagram

```
┌─────────────────────────────────────────────────────┐
│                  USER INTERACTION                    │
└─────────────────┬───────────────────────────────────┘
                  │ WebSocket/HTTP
┌─────────────────▼───────────────────────────────────┐
│              GATEWAY AGENT (:8001)                  │
│  ┌────────────────────────────────────────────┐    │
│  │ • FastAPI Server                           │    │
│  │ • WebSocket Handler                        │    │
│  │ • A2A Orchestrator                         │    │
│  │ • Task Router                              │    │
│  └────────────────────────────────────────────┘    │
└─────────────────┬───────────────────────────────────┘
                  │ A2A Protocol (HTTP/JSON)
     ┌────────────┼────────────┬─────────────┐
     ▼            ▼            ▼             ▼
┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
│CONTEXT  │ │ACTION   │ │KNOWLEDGE│ │COMM.    │
│:8002    │ │:8003    │ │:8004    │ │:8005    │
└─────────┘ └─────────┘ └─────────┘ └─────────┘
     │            │            │             │
     └────────────┴────────────┴─────────────┘
                        │
                  ┌─────▼─────┐
                  │   Redis    │
                  │  (Cache)   │
                  └───────────┘
```

---

*These diagrams show how the OMI device works with multiple AI agents to understand and act on conversations. Each agent is like a specialist on a team, working together to help you!* 🎯