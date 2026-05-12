from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_anomalies_returns_200():
    response = client.get("/insights/anomalies")
    assert response.status_code == 200
    
def test_anomalies_returns_lists():
    response = client.get("/insights/anomalies")
    data = response.json()
    assert isinstance(data, list)
    
def test_anomalies_filter_by_state():
    response = client.get("/insights/anomalies?state=KS")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    for item in data:
        assert item["state"] == "KS"

# schema validation
def test_anomalies_have_required_fields():
    response = client.get("/insights/anomalies")
    data = response.json()
    for item in data:
        assert "facility_name" in item
        assert "score" in item
        assert "anomaly_score" in item
        assert "state" in item
        
