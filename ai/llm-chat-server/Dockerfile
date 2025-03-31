## ------------------------------- Builder Stage ------------------------------ ##
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=0

WORKDIR /app

# Install dependencies using uv sync
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# Copy application code
COPY . /app

# Sync again with the full project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

## ------------------------------- Runtime Stage ------------------------------ ##
FROM python:3.12-slim-bookworm AS runtime

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="/app" \
    PORT=8000

# Create non-root user for security
RUN adduser --disabled-password --gecos "" appuser

WORKDIR /app

# Copy the application from the builder and fix permissions
COPY --from=builder --chown=appuser:appuser /app /app
RUN chmod -R 755 /app/.venv

# Switch to non-root user
USER appuser

# Expose port
EXPOSE $PORT

# Start the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
