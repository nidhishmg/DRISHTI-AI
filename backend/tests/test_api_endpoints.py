import pytest
from httpx import AsyncClient
from src.main import app
from src.core.security import create_access_token
from datetime import timedelta

# Test Fixtures
@pytest.fixture
def anyio_backend():
    return 'asyncio'

@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture
def auth_header():
    token = create_access_token(
        data={"sub": "testadmin", "role": "admin"},
        expires_delta=timedelta(minutes=30)
    )
    return {"Authorization": f"Bearer {token}"}

# Tests

@pytest.mark.anyio
async def test_get_hot_clusters(async_client):
    response = await async_client.get("/api/v1/clusters/hot")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if len(data) > 0:
        assert "confidence_score" in data[0]

@pytest.mark.anyio
async def test_get_causal_graph(async_client):
    response = await async_client.get("/api/v1/graph/archetypes")
    assert response.status_code == 200
    data = response.json()
    assert "nodes" in data
    assert "edges" in data

@pytest.mark.anyio
async def test_simulate_intervention(async_client):
    response = await async_client.post(
        "/api/v1/intervention/simulate?cluster_id=123&intensity=0.8"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["confidence"] > 0
    assert data["cost_estimate"] > 0

@pytest.mark.anyio
async def test_login_success(async_client):
    response = await async_client.post(
        "/api/v1/token",
        json={"username": "admin", "role": "admin"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

@pytest.mark.anyio
async def test_rate_limiting_mock(async_client):
    # This test assumes rate limiting is not yet active or we mock it.
    # For now, just ensure it doesn't crash.
    for _ in range(5):
        response = await async_client.get("/api/v1/clusters/hot")
        assert response.status_code in [200, 429]
