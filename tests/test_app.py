import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Helper to reset in-memory DB (if needed)
def reset_db():
    app.activities = {
        "chess": {"participants": []},
        "robotics": {"participants": []},
        "painting": {"participants": []},
    }
    app.participants = {}


def test_root_redirect():
    response = client.get("/")
    assert response.status_code == 200 or response.status_code == 307
    # Accepts either direct serve or redirect


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "chess" in data
    assert "robotics" in data
    assert "painting" in data


def test_signup_and_unregister():
    reset_db()
    email = "student@example.com"
    activity = "chess"
    # Signup
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert email in response.json()["participants"]
    # Unregister
    response = client.delete(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert email not in response.json()["participants"]


def test_signup_invalid_activity():
    reset_db()
    email = "student@example.com"
    response = client.post(f"/activities/invalid/signup?email={email}")
    assert response.status_code == 404


def test_unregister_invalid_activity():
    reset_db()
    email = "student@example.com"
    response = client.delete(f"/activities/invalid/signup?email={email}")
    assert response.status_code == 404
