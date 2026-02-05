# Multi-stage build for FastAPI application with uv

# Stage 1: Builder
FROM python:3.14-slim AS builder

WORKDIR /code

# Install uv
RUN pip install --no-cache-dir uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies to .venv (without dev dependencies)
RUN uv sync --frozen --no-dev


# Stage 2: Runtime
FROM python:3.14-slim

WORKDIR /code

# Copy virtual environment from builder
COPY --from=builder /code/.venv /code/.venv

# Copy application code
COPY ./app ./app
COPY ./main.py ./

# Set default environment variables
ENV HOST=0.0.0.0
ENV PORT=8000

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD /code/.venv/bin/python -c "import httpx; httpx.get('http://localhost:8000/health')" || exit 1

# Run application using venv python
CMD ["/code/.venv/bin/python", "main.py"]

