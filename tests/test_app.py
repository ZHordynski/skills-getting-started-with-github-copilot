from src.app import activities


def test_root_redirects_to_static_index(client):
    # Arrange
    expected_location = "/static/index.html"

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code in (302, 307)
    assert response.headers["location"] == expected_location


def test_get_activities_returns_activity_dictionary(client):
    # Arrange
    expected_keys = set(activities.keys())

    # Act
    response = client.get("/activities")
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert isinstance(payload, dict)
    assert set(payload.keys()) == expected_keys


def test_signup_for_existing_activity_adds_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "aaa_test_student@mergington.edu"
    original_count = len(activities[activity_name]["participants"])

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert len(activities[activity_name]["participants"]) == original_count + 1
    assert activities[activity_name]["participants"][-1] == email


def test_signup_for_missing_activity_returns_404(client):
    # Arrange
    activity_name = "Nonexistent Club"
    email = "aaa_missing_activity@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
