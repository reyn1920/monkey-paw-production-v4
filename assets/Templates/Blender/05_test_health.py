from fastapi.testclient import (
    TestClient,
)

# Fixed incomplete statement  # Fixed incomplete statement  # Fixed incomplete statement  # Fixed incomplete statement
from app.main import (
    app,
)

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert (
        "timestamp" in data
    )  # Fixed incomplete statement  # Fixed incomplete statement  # Fixed incomplete statement  # Fixed incomplete statement
    assert (
        "service" in data
    )  # Fixed incomplete statement  # Fixed incomplete statement  # Fixed incomplete statement  # Fixed incomplete statement
