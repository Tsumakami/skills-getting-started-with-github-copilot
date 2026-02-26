import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

# Helper to reset activities state between tests
def reset_activities():
    for activity in activities.values():
        activity['participants'].clear()

@pytest.fixture(autouse=True)
def run_before_and_after_tests():
    reset_activities()
    yield
    reset_activities()

def test_get_activities():
    # Arrange
    # (Nada a preparar, pois atividades já existem)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert all('description' in v for v in data.values())

def test_signup_success():
    # Arrange
    activity = list(activities.keys())[0]
    email = "student1@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert email in activities[activity]['participants']
    assert "Signed up" in response.json()['message']

def test_signup_duplicate():
    # Arrange
    activity = list(activities.keys())[0]
    email = "student2@mergington.edu"
    activities[activity]['participants'].append(email)
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert response.json()['detail'] == "Student already signed up"

def test_signup_activity_not_found():
    # Arrange
    email = "student3@mergington.edu"
    # Act
    response = client.post(f"/activities/NonExistent/signup?email={email}")
    # Assert
    assert response.status_code == 404
    assert response.json()['detail'] == "Activity not found"
