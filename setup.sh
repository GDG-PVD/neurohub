#!/bin/bash

# OMI A2A Multi-Agent Demo Setup Script

echo ""
echo "====================================="
echo "OMI A2A Multi-Agent Demo Setup"
echo "====================================="
echo ""

# Check if Python 3.11+ is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3.11+ is required but not installed."
    exit 1
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is required but not installed."
    echo "Please install Docker Desktop from https://www.docker.com/products/docker-desktop"
    exit 1
fi

# Check if UV is installed
if command -v uv &> /dev/null; then
    echo "🚀 Using UV for package management..."
    
    # Create virtual environment with UV
    echo "📦 Creating Python virtual environment..."
    uv venv
    
    # Install dependencies
    echo "📥 Installing Python dependencies with UV..."
    uv pip install -e ".[dev]"
else
    echo "📦 UV not found, using standard pip..."
    echo "Tip: Install UV for faster package management: https://github.com/astral-sh/uv"
    
    # Create virtual environment
    python3 -m venv venv
    source venv/bin/activate
    
    # Install dependencies
    echo "📥 Installing Python dependencies..."
    pip install --upgrade pip
    pip install -e ".[dev]"
fi

# Create .env file from template
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo ""
    echo "⚠️  Please edit .env file with your API keys:"
    echo "   - OMI_API_KEY"
    echo "   - OPENAI_API_KEY (for context analysis)"
    echo ""
fi

# Build Docker images
echo "🔨 Building Docker images..."
docker-compose build

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your API keys"
echo "2. Run 'docker-compose up' to start all agents"
echo "3. Run 'python demo/scenarios/meeting_assistant.py' to see the demo"
echo ""
echo "For development:"
echo "- Activate virtual environment: source venv/bin/activate"
echo "- Run individual agents: python -m agents.<agent_name>.agent"
echo ""