FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY pyproject.toml ./
COPY README.md ./
COPY a2a_sdk.py ./
COPY agents/__init__.py ./agents/
COPY agents/action_planning ./agents/action_planning/
COPY core ./core/
COPY config ./config/

# Install dependencies
RUN pip install --no-cache-dir -e .

# Set working directory and Python path
WORKDIR /app
ENV PYTHONPATH=/app

# Expose port
EXPOSE 8003

# Run the agent
CMD ["python", "-m", "agents.action_planning.agent"]