FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml ./
COPY README.md ./
COPY a2a_sdk.py ./
COPY demo_simple.py ./
COPY workshop_server.py ./
COPY workshop_server_enhanced.py ./
COPY agents ./agents/
COPY core ./core/
COPY config ./config/
COPY integrations ./integrations/
COPY static ./static/

# Install UV and dependencies
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"
RUN uv venv && uv pip install -e .

# Set Python path
ENV PYTHONPATH=/app

# Expose port
EXPOSE 8000

# Run the workshop server
CMD ["uv", "run", "python", "workshop_server.py"]