# Reality Gap AI (DRISHTI-AI)

## Overview
Reality Gap AI is a robust intelligence platform designed to uncover discrepancies between government scheme allocations and on-the-ground reality. It processes voice complaints, social media signals, and news reports to identify "Failure Clusters" and generate causal interventions.

## Phases
- **Phase 1: Foundation**: Ingestion Engine, PostgreSQL/Milvus/Neo4j setup.
- **Phase 2: Intelligence**: Causal Inference, Clustering, Intervention Generation.
- **Phase 3: Experience**: Next.js Frontend, Real-time Dashboard, Policy Simulator.

## Quick Start (Phase 3)
1. **Infrastructure**:
   ```bash
   make up
   ```
2. **Access**:
   - Frontend: [http://localhost:3000](http://localhost:3000)
   - API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)
   - Grafana: [http://localhost:3001](http://localhost:3001)

## Architecture
See [architecture.mmd](architecture.mmd) for the full system diagram.

## Documentation
- [Backend README](backend/README.md)
- [Frontend README](frontend/README.md)
- [Deployment Guide](deployment/README.md)
- [Demo Script](DEMO.md)
