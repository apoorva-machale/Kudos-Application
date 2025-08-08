import pytest
from fastapi.testclient import TestClient
from kudos.main import app

client = TestClient(app)

def test_login_and_me_flow():
    # Login
    response = client.post("/login", data={"username": "demo", "password": "demo"})
    assert response.status_code == 200
    token = response.json()["access_token"]

    # Get me
    headers = {"Authorization": f"Bearer {token}"}
    me_response = client.get("/me", headers=headers)
    assert me_response.status_code == 200
    data = me_response.json()
    assert "username" in data
    assert "organization" in data
