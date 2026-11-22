from fastapi.testclient import TestClient
from app.main import app
def test_health_and_mock_source():
    client=TestClient(app)
    assert client.get("/health").status_code==200
    response=client.get("/mock-source?page=1&page_size=5")
    assert response.status_code==200 and len(response.json()["items"])==5
