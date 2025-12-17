# Multi-stage build for optimized image size
FROM python:3.11-slim as builder

# Set working directory
WORKDIR /app

# Install dependencies in a virtual environment
COPY requirements.txt .
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

# Final stage - minimal runtime image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Copy application code
COPY . .

# Create directory for SQLite database
RUN mkdir -p /app/data

# Set environment variables
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app.py \
    DB_PATH=/app/data/db.sqlite

# Expose port
EXPOSE 5000

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health').read()" || exit 1

# Run the application
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
