from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():
	response = client.get("/health")
	assert response.status_code == 200
	assert response.json()["status"] == "ok"


def test_profile_validation():
	response = client.post("/profiles", json={"name": "", "age": 12})
	assert response.status_code == 422