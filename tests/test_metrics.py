from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    
def test_get_metrics_returns_200():
    response = client.get("/metrics/")
    assert response.status_code == 200
    
def test_get_metrics_filter_by_state():
    response = client.get("/metrics/?state=KS")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    for item in data:
        assert item["state"] == "KS"

def test_get_metrics_filter_by_measure():
    response = client.get("/metrics/?measure_id=OP_18b")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    for item in data:
        assert item["measure_id"] == "OP_18b" 

def test_get_metrics_limit():
    response = client.get("/metrics/?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data) <= 5

# intentionally bad request
def test_aggregate_requires_measure_id():
    response = client.get("/metrics/aggregate")
    assert response.status_code == 422

def test_aggregate_returns_data():
    response = client.get("/metrics/aggregate?measure_id=OP_18b")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    



    
    

