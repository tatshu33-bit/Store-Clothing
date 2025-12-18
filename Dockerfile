# Multi-stage build for optimized image size
FROM python:3.11-slim AS base

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.11-slim

WORKDIR /app

# Copy installed packages from base stage
COPY --from=base /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=base /usr/local/bin /usr/local/bin

# Copy application code
COPY . .

# Create directory for database
RUN mkdir -p /app/data

# Set environment variables
ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1
ENV DB_PATH=/app/data/db.sqlite

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000').read()" || exit 1

# Run the application
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]
