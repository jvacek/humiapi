FROM astral/uv:0.11-python3.13-alpine

# Set environment variables
ENV UV_LINK_MODE=copy
ENV UV_PYTHON_INSTALL_DIR=/python
# Only use the managed Python version
ENV UV_PYTHON_PREFERENCE=only-managed
RUN uv python install 3.13

# Create app directory
WORKDIR /app
ENV PATH="/app/.venv/bin:$PATH"
# Copy dependency files first for better caching
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-dev

# Set production environment variables
ENV HOST=0.0.0.0 \
    PORT=8080 \
    PYTHONPATH=/app

# Expose the port that Cloud Run expects
EXPOSE ${PORT}
# Copy application code
COPY . .
# Use uv to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
