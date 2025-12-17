# Docker Deployment Guide

This guide provides comprehensive instructions for running the Store Clothing application in Docker containers.

## Prerequisites

- Docker Engine 20.10 or higher
- Docker Compose 2.0 or higher

> **Note**: This guide uses `docker-compose` commands (Compose V1). If you have Docker Compose V2, you can use `docker compose` (without hyphen) instead. Both versions work identically.

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/tatshu33-bit/Store-Clothing.git
cd Store-Clothing
```

### 2. Configure Environment Variables

Copy the example environment file and customize it:

```bash
cp .env.example .env
```

Edit `.env` with your preferred values:

```env
FLASK_ENV=production
PORT=5000
SECRET_KEY=your_very_secure_secret_key_here
ADMIN_PASSWORD=your_secure_admin_password
DB_PATH=/app/data/db.sqlite
```

**Important**: Change `SECRET_KEY` and `ADMIN_PASSWORD` to secure values in production!

### 3. Build and Run with Docker Compose

```bash
docker-compose up -d
```

This command will:
- Build the Docker image
- Create a persistent volume for the SQLite database
- Start the application container
- Expose the application on port 5000 (or your configured port)

### 4. Access the Application

- **Main Store**: http://localhost:5000
- **Admin Panel**: http://localhost:5000/admin/login
- **Health Check**: http://localhost:5000/health

Default admin password is set in your `.env` file.

## Docker Commands

### View Running Containers

```bash
docker-compose ps
```

### View Application Logs

```bash
docker-compose logs -f web
```

### Stop the Application

```bash
docker-compose down
```

### Stop and Remove Volumes (⚠️ This will delete the database)

```bash
docker-compose down -v
```

### Rebuild the Image

```bash
docker-compose build --no-cache
docker-compose up -d
```

### Access Container Shell

```bash
docker-compose exec web /bin/bash
```

## Docker Configuration Details

### Dockerfile Features

- **Multi-stage build**: Reduces final image size
- **Python 3.11 slim**: Minimal base image
- **Virtual environment**: Isolated Python dependencies
- **Health check**: Automatic container health monitoring
- **Non-root user**: Enhanced security (planned)

### Docker Compose Configuration

- **Port mapping**: Host port to container port 5000
- **Environment variables**: Configurable application settings
- **Volume persistence**: SQLite database data survives container restarts
- **Health checks**: Ensures application is running correctly
- **Restart policy**: Automatically restarts on failure

### Volume Management

The SQLite database is stored in a Docker volume named `sqlite_data`. This ensures data persistence across container restarts and rebuilds.

To backup the database:

```bash
docker-compose exec web cp /app/data/db.sqlite /tmp/backup.sqlite
docker cp store-clothing-app:/tmp/backup.sqlite ./db_backup.sqlite
```

To restore a database:

```bash
docker cp ./db_backup.sqlite store-clothing-app:/tmp/restore.sqlite
docker-compose exec web cp /tmp/restore.sqlite /app/data/db.sqlite
docker-compose restart web
```

## Health Checks

The application includes a health check endpoint at `/health` that:
- Verifies the Flask application is running
- Checks database connectivity
- Returns JSON status information

Docker uses this endpoint to monitor container health:
- **Interval**: Checks every 30 seconds
- **Timeout**: 10 seconds per check
- **Retries**: 3 failed checks before marking unhealthy
- **Start period**: 5 seconds grace period on startup

View health status:

```bash
docker-compose ps
# or
docker inspect store-clothing-app | grep -A 10 Health
```

## Environment Variables Reference

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Flask environment mode | `production` |
| `PORT` | Application port | `5000` |
| `SECRET_KEY` | Flask session encryption key | `default_secret_key_change_in_production` |
| `ADMIN_PASSWORD` | Admin panel password | `adminpass` |
| `DB_PATH` | SQLite database file path | `/app/data/db.sqlite` |

## Troubleshooting

### Container Won't Start

Check logs:
```bash
docker-compose logs web
```

### Port Already in Use

Change the port in `.env`:
```env
PORT=8080
```

Then restart:
```bash
docker-compose down
docker-compose up -d
```

### Database Issues

Reset the database (⚠️ deletes all data):
```bash
docker-compose down -v
docker-compose up -d
```

### Health Check Failing

Check the health endpoint manually:
```bash
curl http://localhost:5000/health
```

View detailed health status:
```bash
docker inspect store-clothing-app --format='{{json .State.Health}}' | python -m json.tool
```

## Production Deployment

### Security Recommendations

1. **Use strong secret key**: Generate with `python -c "import secrets; print(secrets.token_hex(32))"`
2. **Set secure admin password**: Use a password manager to generate
3. **Use HTTPS**: Deploy behind a reverse proxy (nginx, Traefik)
4. **Disable debug mode**: Ensure `FLASK_ENV=production`
5. **Regular backups**: Backup the database volume regularly
6. **Update dependencies**: Keep base image and packages updated

### Reverse Proxy Example (nginx)

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Docker Compose Production Override

Create `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  web:
    restart: always
    environment:
      - FLASK_ENV=production
```

Run with:
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## Development Mode

For local development with hot-reload:

```bash
docker-compose run --rm -p 5000:5000 -v $(pwd):/app web python app.py
```

## Image Optimization

The Dockerfile uses several optimization techniques:

1. **Multi-stage build**: Only runtime dependencies in final image
2. **Slim base image**: python:3.11-slim instead of full python image
3. **No cache**: `pip install --no-cache-dir` reduces image size
4. **Virtual environment**: Isolates dependencies and allows easy copying
5. **Layer optimization**: Dependencies installed before code copy

To check image size:
```bash
docker images store-clothing-web
```

## Support

For issues or questions:
- Check application logs: `docker-compose logs -f web`
- Review this documentation
- Check GitHub issues: https://github.com/tatshu33-bit/Store-Clothing/issues
