FROM python:3.11-slim-bookworm

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Copy project metadata, dependencies, and source code
COPY pyproject.toml requirements.txt README.md ./
COPY src/ ./src/

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -e .
# Create directory for credentials and tokens
RUN mkdir -p /app/data

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Expose port for HTTP mode
EXPOSE 8000

# Default command (can be overridden in docker-compose)
CMD ["python", "-m", "gdrive_mcp_server.server", "--http", "--token", "/app/data/tokens.json"]

