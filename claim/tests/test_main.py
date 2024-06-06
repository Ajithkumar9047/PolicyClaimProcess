from fastapi.testclient import TestClient
import pytest

from main import app


@pytest.fixture(scope="module")
def client():
    with TestClient(app=app, base_url="http://localhost") as client:
        yield client


def test_submit_data_success(client: TestClient):
    data = [
        {
            "service_date": "2024-06-03",
            "submitted_procedure": "D1234",
            "quadrant": "",
            "plan_group": "PPO-ABC",
            "subscriber": "1234567890",
            "provider_npi": "1112223333",
            "provider_fees": "$150.00",
            "allowed_fees": "$100.00",
            "member_coinsurance": "$25.00",
            "member_copay": "$10.00"
        }
    ]
    response = client.post("/submit-data", json=data)
    assert response.status_code == 200
    assert response.json() == {"message": "Data successfully saved"}
