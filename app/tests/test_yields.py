#Test for yields
import pytest
from app.services.defi import get_top_yields, detect_risks

def test_get_top_yields(client):
    response = client.post("/yields/top-yields", json={"tokens": ["ETH", "BTC"]})
    assert response.status_code == 200
    assert "results" in response.json()

def test_detect_risks(client):
    response = client.post("/yields/risk", json={"pools": [
        {"apy": 35, "tvlUsd": 500000, "project": "HighRiskProject"},
        {"apy": 5, "tvlUsd": 2000000, "project": "LowRiskProject"},
        {"apy": 20, "tvlUsd": 1000000, "project": "UnknownProject"}
    ]})
    assert response.status_code == 200
    assert "results" in response.json() 