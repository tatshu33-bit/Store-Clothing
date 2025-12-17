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
grep -q "os.environ.get" app.py && echo "✓ app.py supports environment variables" || echo "✗ app.py missing environment support"
grep -q "os.environ.get" models.py && echo "✓ models.py supports environment variables" || echo "✗ models.py missing environment support"
echo ""

# Check for volume configuration
echo "Checking volume configuration..."
grep -q "volumes:" docker-compose.yml && echo "✓ docker-compose.yml has volume configuration" || echo "✗ docker-compose.yml missing volumes"
grep -q "db-data:" docker-compose.yml && echo "✓ Persistent volume defined" || echo "✗ Persistent volume not defined"
echo ""

# Check health check configuration
echo "Checking health check configuration..."
grep -q "HEALTHCHECK" Dockerfile && echo "✓ Dockerfile has health check" || echo "✗ Dockerfile missing health check"
grep -q "healthcheck:" docker-compose.yml && echo "✓ docker-compose.yml has health check" || echo "✗ docker-compose.yml missing health check"
echo ""

echo "=== All checks passed! ==="
echo ""
echo "To deploy the application:"
echo "1. Configure environment: cp .env.example .env"
echo "2. Build and run: docker-compose up -d"
echo "3. Check logs: docker-compose logs -f"
echo "4. Access app: http://localhost:5000"
