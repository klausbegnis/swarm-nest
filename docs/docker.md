# Docker

## Quick Start

### Build and Run

```bash
# Build image
docker-compose build

# Run container
docker-compose up

# Run in background
docker-compose up -d

# Stop container
docker-compose down
```

## Docker Commands

### Build Image

```bash
docker build -t fastapi-template .
```

### Run Container

```bash
docker run -p 8000:8000 --env-file .env fastapi-template
```

### With Environment Variables

```bash
docker run -p 8000:8000 \
  -e APP_NAME="My API" \
  -e DEBUG=True \
  -e LOG_LEVEL=DEBUG \
  fastapi-template
```

## Docker Compose

### Development Mode

```yaml
# docker-compose.yml includes hot reload with volumes
docker-compose up
```

### Production Mode

Remove volume mounts from `docker-compose.yml` for production:

```yaml
services:
  api:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    restart: unless-stopped
```

## Health Check

Container includes health check at `/health` endpoint:

```bash
# Check container health
docker ps

# View health check logs
docker inspect --format='{{json .State.Health}}' fastapi-template
```

## Environment Variables

All settings from `.env` are supported. Key variables:

- `APP_NAME` - Application name
- `DEBUG` - Debug mode (True/False)
- `LOG_LEVEL` - Logging level (DEBUG, INFO, WARNING, ERROR)
- `HOST` - Server host (default: 0.0.0.0 in Docker)
- `PORT` - Server port (default: 8000)

## Multi-Stage Build

Dockerfile uses multi-stage build for smaller image size:
- Builder stage: Installs dependencies
- Runtime stage: Only includes necessary files

## Troubleshooting

### Container won't start

```bash
# Check logs
docker-compose logs api

# Check if port is already in use
lsof -i :8000
```

### Hot reload not working

Ensure volumes are mounted in `docker-compose.yml`:
```yaml
volumes:
  - ./app:/code/app
```

