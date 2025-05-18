import pytest
from fastapi.testclient import TestClient
from mcp_server import app

@pytest.fixture(scope="module")
def client():
    """
    Create a test client for the FastAPI app.
    """
    with TestClient(app) as client:
        yield client

def test_root(client):
    """
    Test the root endpoint.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Sage, your DeFi assistant!"}