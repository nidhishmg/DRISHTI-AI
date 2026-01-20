# Deployment Guide: Reality Gap AI

## Local Development (Docker Compose)
The easiest way to run the full stack (Frontend + Backend + DBs) is via Docker Compose.

### Prerequisites
- Docker & Docker Compose
- Node.js 18+ (for local frontend dev)
- Python 3.10+ (for local backend dev)

### Quick Start
```bash
make up
```
This command builds the images and starts all services.
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/docs
- **Grafana**: http://localhost:3001
- **MinIO**: http://localhost:9001
- **Neo4j**: http://localhost:7474

### Stopping
```bash
make down
```

## Production Deployment (Kubernetes)
Manifests are located in the `k8s/` directory.

### Deploying
```bash
kubectl apply -f k8s/deployment.yaml
```

### Configuration
- Ensure Secrets are managed (e.g., via K8s Secrets or Vault).
- Update `ENV` variables in `deployment.yaml` for production values.
- Configure Ingress for external access (not included in basic manifests).

## Troubleshooting
- **Frontend can't connect to Backend**: Ensure `NEXT_PUBLIC_API_URL` is set correctly. In Docker, it's set to `http://localhost:8000` for client-side fetches (browser to API).
- **Database Connection Failures**: Check `docker-compose logs backend` to see if it's waiting for Postgres/Redis.
