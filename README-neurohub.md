# 🧠 NeuroHub - OMI + Multi-Agent AI Demo

> An educational demonstration of multi-agent AI systems using OMI wearable device and the A2A protocol

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/Docker-Required-blue.svg)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-green.svg)](https://www.python.org/)

## 🎯 What is NeuroHub?

NeuroHub demonstrates how wearable AI devices (like OMI) can work with multiple specialized AI agents to analyze conversations in real-time. This educational project shows the future of collaborative AI systems.

### 🌟 Key Features

- **Real OMI Integration**: Connect to actual OMI wearable device APIs
- **Multi-Agent Simulation**: See how specialized AI agents can work together
- **Educational Focus**: Perfect for students learning about AI systems
- **Easy Setup**: Simplified installation with UV package manager

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or newer
- Docker Desktop
- Git

### Installation

```bash
# Clone the repository
git clone git@github.com:GDG-PVD/neurohub.git
cd neurohub

# Install UV package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv venv
uv pip install -e ".[dev]"

# Copy environment configuration
cp .env.example .env.local
```

### Running the Demo

```bash
# Terminal 1: Start OMI Server
./scripts/start_omi_mcp.sh

# Terminal 2: Run Demo
uv run python demo_simple.py
```

## 📚 Documentation

- **[Student Guide](STUDENT_GUIDE.md)** - Complete walkthrough for students
- **[Instructor Presentation](INSTRUCTOR_PRESENTATION.md)** - Teaching materials and slides
- **[Quick Reference](STUDENT_QUICK_REFERENCE.md)** - Command cheat sheet
- **[UV Commands Guide](UV_COMMANDS_GUIDE.md)** - Understanding UV package manager

## 🏗️ Architecture

```
┌─────────────┐     ┌─────────────────┐     ┌──────────────────┐
│ OMI Device  │────▶│  Gateway Agent  │────▶│ Context Analysis │
│ (Wearable)  │     │  (Orchestrator) │     │     Agent        │
└─────────────┘     └────────┬────────┘     └──────────────────┘
                             │
                             └──────────────▶│ Action Planning  │
                                            │     Agent        │
                                            └──────────────────┘
```

## 🎓 Learning Objectives

After completing this demo, you'll understand:

1. How AI agents can work together to solve complex problems
2. The basics of distributed AI systems
3. How wearable devices integrate with AI services
4. The importance of modular architecture in AI systems

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Ways to Contribute

- 🐛 Report bugs
- 💡 Suggest new features
- 📝 Improve documentation
- 🧪 Add tests
- 🎨 Enhance UI/UX

## 📖 Resources

- [OMI Documentation](https://docs.omi.me)
- [MCP Protocol Reference](OMI_MCP_OFFICIAL_REFERENCE.md)
- [A2A Protocol Overview](MCP_VS_A2A_EXPLANATION.md)

## 🛠️ Troubleshooting

### Common Issues

| Problem | Solution |
|---------|----------|
| `venv/bin/activate not found` | Use `uv run python` instead |
| `Connection refused` | Start OMI server first |
| Docker issues | Check [Demo Backup Plan](docs/classroom/DEMO_BACKUP_PLAN.md) |

## 📊 Project Status

- ✅ Basic OMI integration
- ✅ Simple demo working
- ✅ Educational documentation
- 🚧 Full multi-agent deployment
- 📋 Additional agent types

## 👥 Team

Created by [GDG Providence](https://github.com/GDG-PVD) for educational purposes.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Based Hardware](https://github.com/BasedHardware) for the OMI device
- [A2A Project](https://github.com/a2a-project) for the agent protocol
- All contributors and students who help improve this demo

---

**Note**: This is an educational project demonstrating multi-agent AI concepts. The A2A protocol integration is simulated for teaching purposes. For production OMI integration, refer to the [official OMI documentation](https://docs.omi.me).

<p align="center">Made with ❤️ for AI education</p>