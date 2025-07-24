FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml ./
COPY README.md ./
COPY a2a_sdk.py ./
COPY agents/__init__.py ./agents/
COPY agents/omi_gateway ./agents/omi_gateway/
COPY core ./core/
COPY config ./config/
COPY integrations ./integrations/

# Install dependencies
RUN pip install --no-cache-dir -e .

# Set Python path
ENV PYTHONPATH=/app

# Expose A2A port
EXPOSE 8000

# Run the agent
CMD ["python", "agents/omi_gateway/agent.py"]