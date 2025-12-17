# Docker Deployment Guide

This guide explains how to deploy the Store Clothing Flask application using Docker and Docker Compose.

## Prerequisites

- Docker Engine 20.10+ installed
- Docker Compose v2.0+ installed

## Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Store-Clothing
```

### 2. Configure Environment Variables (Optional)

Copy the example environment file and customize it:

```bash
cp .env.example .env
```

Edit `.env` file to set your custom values:
- `SECRET_KEY`: Your secret key for Flask session management (change in production!)
- `ADMIN_PASSWORD`: Password for admin panel access
- `PORT`: Port to expose the application (default: 5000)
- `FLASK_ENV`: Environment mode (production/development)

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

- Main site: http://localhost:5000
- Shop: http://localhost:5000/shop
- Admin panel: http://localhost:5000/admin/login

Default admin password: `1` (change via `ADMIN_PASSWORD` environment variable)

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

### Stop and Remove Volumes (Warning: This will delete your database!)

```bash
docker-compose down -v
```

### Rebuild the Image

If you make changes to the application code:

```bash
docker-compose up -d --build
```

## Docker Architecture

### Dockerfile

The application uses a multi-stage build approach:

1. **Base Stage**: Installs system dependencies and Python packages
2. **Production Stage**: Creates a minimal runtime image with only necessary components

Key features:
- Based on Python 3.11 slim image for reduced size
- Multi-stage build for optimization
- Health checks configured
- Database directory pre-created

### Docker Compose Configuration

The `docker-compose.yml` file defines:

- **Service**: `web` - The Flask application
- **Port Mapping**: Host port to container port 5000
- **Environment Variables**: Application configuration
- **Volume**: `db-data` - Persistent storage for SQLite database
- **Health Check**: Automated application health monitoring
- **Restart Policy**: `unless-stopped` - Ensures high availability

### Volume Management

The SQLite database is stored in a Docker volume (`db-data`) mounted at `/app/data` inside the container. This ensures:

- Data persistence across container restarts
- Data separation from application code
- Easy backup and restore capabilities

## Database Backup and Restore

### Backup Database

```bash
docker-compose exec web sqlite3 /app/data/db.sqlite .dump > backup.sql
```

Or copy the database file directly:

```bash
docker cp store-clothing-web:/app/data/db.sqlite ./backup-db.sqlite
```

### Restore Database

```bash
docker cp ./backup-db.sqlite store-clothing-web:/app/data/db.sqlite
docker-compose restart web
```

## Health Checks

The application includes health checks that:
- Run every 30 seconds
- Verify the application responds to HTTP requests
- Allow 3 retries before marking as unhealthy
- Have a 5-second startup grace period

Check health status:

```bash
docker-compose ps
```

## Troubleshooting

### Container Won't Start

Check logs:
```bash
docker-compose logs web
```

### Database Permission Issues

If you encounter permission issues with the database:

```bash
docker-compose down
docker volume rm store-clothing_db-data
docker-compose up -d
```

### Port Already in Use

Change the port in `.env` file or use:

```bash
PORT=8080 docker-compose up -d
```

### Rebuild from Scratch

```bash
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

## Production Deployment Recommendations

1. **Change Default Secrets**: Always set custom values for `SECRET_KEY` and `ADMIN_PASSWORD`
2. **Use Environment Variables**: Never commit sensitive data to version control
3. **Regular Backups**: Schedule automated database backups
4. **Monitor Logs**: Set up log aggregation and monitoring
5. **Update Images**: Regularly update base images for security patches
6. **Resource Limits**: Consider adding resource limits in docker-compose.yml:

```yaml
services:
  web:
    # ... other config
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
```

## Development Mode

For development with live code reloading:

1. Create `.env` with `FLASK_ENV=development`
2. Mount source code as volume:

```yaml
services:
  web:
    volumes:
      - .:/app
      - db-data:/app/data
```

3. Run with docker-compose:

```bash
docker-compose up
```

## Advanced Configuration

### Using External Database

To use a different database (e.g., PostgreSQL, MySQL), modify:
1. Update `requirements.txt` with appropriate database driver
2. Modify `models.py` to support the new database
3. Add database service to `docker-compose.yml`
4. Update environment variables accordingly

### Nginx Reverse Proxy

For production deployment with Nginx:

```yaml
services:
  web:
    # Remove ports section
    expose:
      - "5000"
  
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - web
```

## Support

For issues or questions:
- Check the logs: `docker-compose logs -f`
- Verify Docker and Docker Compose versions
- Review environment variable configuration
- Check Docker volume permissions

## License

See the main README.md for license information.
