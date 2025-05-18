#Test the alerts

def test_subscribe_alert(client):
    response = client.post("/alerts/subscribe", json={"alert_type": "price_drop", "threshold": 10})
    assert response.status_code == 200
    assert response.json() == {"message": "Subscribed to price drop alerts with threshold 10"}

def test_check_alerts(client):
    response = client.get("/alerts/check?threshold=5.0")
    assert response.status_code == 200
    assert "alerts" in response.json()