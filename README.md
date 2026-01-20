# DRISHTI-AI (Reality Gap AI Platform) v2.0

**Integrity-First AI Platform for Public Scheme Delivery**

DRISHTI-AI is a comprehensive platform designed to bridge the gap between reported data and on-the-ground reality in public scheme delivery. It leverages audio ingestion, causal AI, and clustering to detect anomalies, identify root causes, and propose interventions.

## 🚀 Key Features

*   **Multi-Modal Ingestion**: Upload voice reports (mock supported for demo) and process them.
*   **Causal Intelligence**: Visualize causal relationships between failure archetypes (e.g., Biometric Failure -> Pension Denial).
*   **Dynamic Clustering**: Real-time clustering of incoming reports to identify "Hot Clusters" of issues.
*   **Hardened Security**:
    *   **Authentication**: JWT with Refresh Tokens, Secure Cookies, and RBAC.
    *   **Inputs**: Strict Pydantic validation and sanitization.
    *   **Data Governance**: PII redaction (email, phone, aadhaar) and Chain of Custody logging.
    *   **Export**: Secure export of evidence with watermarking.
*   **Scalability**:
    *   **Performance**: Redis-backed rate limiting, incremental clustering, and ASR worker pool.
    *   **Deployment**: Docker-ready, Helm charts included, and CI/CD workflows.

## 🛠️ Technology Stack

*   **Backend**: FastAPI, Python 3.10
*   **Frontend**: Next.js 14, Tailwind CSS, Shadcn/UI, Recharts, Leaflet
*   **Data/ML**: FAISS/Milvus (Vector DB), HDBSCAN, UMAP, Faster-Whisper
*   **Infrastructure**: Docker, Redis, Prometheus (Metrics)

## ⚡ Quick Start (Demo Mode)

1.  **Prerequisites**: Docker & Docker Compose installed.
2.  **Run All Services**:
    ```bash
    make run
    ```
    This starts Backend (Port 8000), Frontend (Port 3000), Redis, and other services.

3.  **Access Dashboard**: Open `http://localhost:3000`
4.  **API Documentation**: Open `http://localhost:8000/docs`

## 🔐 Security & Testing

*   **Run Tests**:
    ```bash
    # Backend
    cd backend && pytest
    # Frontend
    cd frontend && npm test
    ```
*   **Export Evidence**: Securely download complaint data via the API (Analyst role required).

## 📂 Project Structure

*   `backend/`: FastAPI application, ML pipeline, and API endpoints.
*   `frontend/`: Next.js dashboard and visualization components.
*   `infra/`: Docker compose, Prometheus config, and Helm charts.
*   `deployment/`: K8s manifests (if applied).

## 🛡️ License
MIT License
