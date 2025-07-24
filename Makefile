# Makefile for OMI A2A Demo

.PHONY: help install install-uv dev test lint format clean docker-up docker-down

# Default target
help:
	@echo "OMI A2A Demo - Available commands:"
	@echo "  make install      - Install dependencies (auto-detects UV)"
	@echo "  make install-uv   - Install UV package manager"
	@echo "  make dev          - Run development server"
	@echo "  make test         - Run tests"
	@echo "  make lint         - Run linters"
	@echo "  make format       - Format code"
	@echo "  make clean        - Clean up temporary files"
	@echo "  make docker-up    - Start all agents with Docker"
	@echo "  make docker-down  - Stop all Docker containers"

# Install UV
install-uv:
	@echo "🚀 Installing UV package manager..."
	curl -LsSf https://astral.sh/uv/install.sh | sh
	@echo "✅ UV installed! Restart your shell or run: source $$HOME/.cargo/env"

# Install dependencies
install:
	@if command -v uv >/dev/null 2>&1; then \
		echo "🚀 Installing with UV..."; \
		uv venv; \
		uv pip install -e ".[dev]"; \
	else \
		echo "📦 Installing with pip..."; \
		python -m venv venv; \
		. venv/bin/activate && pip install -e ".[dev]"; \
	fi
	@echo "✅ Dependencies installed!"

# Development server
dev:
	@echo "🚀 Starting Gateway Agent..."
	python -m agents.omi_gateway.agent

# Run tests
test:
	@echo "🧪 Running tests..."
	pytest -v

# Lint code
lint:
	@echo "🔍 Running linters..."
	ruff check .
	mypy .

# Format code
format:
	@echo "🎨 Formatting code..."
	black .
	ruff check --fix .

# Clean temporary files
clean:
	@echo "🧹 Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.coverage" -delete
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .ruff_cache
	rm -rf build dist *.egg-info

# Docker commands
docker-up:
	@echo "🐳 Starting all agents with Docker..."
	docker-compose up -d
	@echo "✅ All agents running! Check status with: docker-compose ps"

docker-down:
	@echo "🛑 Stopping all agents..."
	docker-compose down

# Quick setup for new developers
quickstart: install
	@echo "🏁 Quick setup complete!"
	@echo "Next steps:"
	@echo "1. Copy .env.example to .env.local"
	@echo "2. Add your API keys"
	@echo "3. Run 'make docker-up' to start all agents"