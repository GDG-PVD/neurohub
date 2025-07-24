# OMI A2A Multi-Agent System Documentation

## Quick Links

- 🚀 **[Quick Start Guide](../QUICK_START.md)** - Get running in 5 minutes
- 📐 **[Architecture](architecture/README.md)** - System design and components
- 📊 **[C4 Diagrams](architecture/c4-diagrams.md)** - Visual architecture
- 📝 **[ADRs](adr/README.md)** - Architecture decisions
- 🔌 **[API Reference](api/README.md)** - Agent APIs
- 📚 **[Development Guide](guides/development.md)** - Contributing guide

## Documentation Structure

```
docs/
├── README.md              # This file
├── adr/                   # Architecture Decision Records
│   ├── README.md         # ADR registry
│   ├── template.md       # ADR template
│   └── *.md              # Individual ADRs
├── architecture/          # Architecture documentation
│   ├── README.md         # Architecture overview
│   ├── c4-diagrams.md    # C4 model diagrams
│   └── *.md              # Other architecture docs
├── api/                   # API documentation
│   └── *.md              # API references
└── guides/                # How-to guides
    ├── development.md    # Development guide
    ├── deployment.md     # Deployment guide
    └── *.md              # Other guides
```

## About This Project

The OMI A2A Multi-Agent System demonstrates how to build sophisticated AI systems where multiple specialized agents collaborate using Google's Agent2Agent (A2A) protocol. The system processes conversations from OMI wearable devices through a pipeline of AI agents that:

- Analyze context and extract insights
- Plan and execute actions
- Retrieve relevant knowledge
- Communicate results

## Key Design Principles

1. **Modular Documentation**: Each component has its own focused docs
2. **Decision Tracking**: All architectural decisions recorded in ADRs
3. **Visual Architecture**: C4 diagrams show system at multiple levels
4. **Living Documentation**: Docs updated alongside code changes
5. **AI-Assisted Development**: Following best practices for AI-powered coding

## Contributing to Documentation

When adding new features or making changes:

1. Update relevant component README files
2. Create ADRs for significant decisions
3. Update architecture diagrams if structure changes
4. Add API documentation for new endpoints
5. Include examples and use cases

## Documentation Standards

- Use Markdown for all documentation
- Include diagrams where helpful (Mermaid preferred)
- Cross-link between related documents
- Keep language clear and concise
- Update the ADR registry when adding new ADRs

## Automation

This project includes:

- Documentation linting (markdown style)
- Link checking (ensure no broken links)
- ADR registry validation
- Auto-generated API docs from code

See [Development Guide](guides/development.md) for details.

## Questions?

For questions about:
- **Architecture**: See [Architecture Overview](architecture/README.md)
- **Decisions**: Check [ADR Registry](adr/README.md)
- **Implementation**: Read [Development Guide](guides/development.md)
- **Usage**: Start with [Quick Start](../QUICK_START.md)