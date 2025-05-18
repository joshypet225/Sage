def test_rebalance_portfolio(client):
    data = {"user": "0xabc23", "token": ["ETH", "BTC"], "amount": [0.5, 0.5]}
    response = client.get("/rebalance"), json=data
    assert response.status_code == 200
    assert "portfolio" in response.json()

