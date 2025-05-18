#Test pricing

def test_get_token_prices(client):
    response = client.get("/pricing/token-prices")
    assert response.status_code == 200
    assert "prices" in response.json()