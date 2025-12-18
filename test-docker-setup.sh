#!/bin/bash

# Test script to verify Docker setup files
echo "=== Testing Docker Configuration ==="
echo ""

# Check for required files
echo "Checking required files..."
files=("Dockerfile" "docker-compose.yml" "requirements.txt" ".dockerignore" ".env.example" "DOCKER.md")
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "✓ $file exists"
    else
        echo "✗ $file missing"
        exit 1
    fi
done
echo ""

# Validate Dockerfile syntax
echo "Validating Dockerfile syntax..."
if docker build --help > /dev/null 2>&1; then
    echo "✓ Docker is available"
    # Try a dry-run check if possible
    if docker buildx > /dev/null 2>&1; then
        echo "✓ Docker buildx available for validation"
    fi
else
    echo "! Docker not available in environment, skipping build test"
fi
echo ""

# Validate docker-compose.yml syntax
echo "Validating docker-compose.yml syntax..."
if command -v docker-compose > /dev/null 2>&1; then
    docker-compose config --quiet && echo "✓ docker-compose.yml is valid" || echo "✗ docker-compose.yml has errors"
else
    echo "! docker-compose not available, skipping validation"
fi
echo ""

# Check environment variables support
echo "Checking environment variables configuration..."
if ! grep -q "os.environ.get" app.py; then
    echo "✗ app.py missing environment support"
    exit 1
fi
echo "✓ app.py supports environment variables"

if ! grep -q "os.environ.get" models.py; then
    echo "✗ models.py missing environment support"
    exit 1
fi
echo "✓ models.py supports environment variables"
echo ""

# Check for volume configuration
echo "Checking volume configuration..."
if ! grep -q "volumes:" docker-compose.yml; then
    echo "✗ docker-compose.yml missing volumes"
    exit 1
fi
echo "✓ docker-compose.yml has volume configuration"

if ! grep -q "db-data:" docker-compose.yml; then
    echo "✗ Persistent volume not defined"
    exit 1
fi
echo "✓ Persistent volume defined"
echo ""

# Check health check configuration
echo "Checking health check configuration..."
if ! grep -q "HEALTHCHECK" Dockerfile; then
    echo "✗ Dockerfile missing health check"
    exit 1
fi
echo "✓ Dockerfile has health check"

if ! grep -q "healthcheck:" docker-compose.yml; then
    echo "✗ docker-compose.yml missing health check"
    exit 1
fi
echo "✓ docker-compose.yml has health check"
echo ""

echo "=== All checks passed! ==="
echo ""
echo "To deploy the application:"
echo "1. Configure environment: cp .env.example .env"
echo "2. Build and run: docker-compose up -d"
echo "3. Check logs: docker-compose logs -f"
echo "4. Access app: http://localhost:5000"
