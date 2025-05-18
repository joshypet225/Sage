def test_detect_risks(client):
    response = client.get("/risks/detect")
    assert response.status_code == 200
    assert "risks" in response.json()