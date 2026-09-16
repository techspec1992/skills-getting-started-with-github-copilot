def test_get_activities_returns_activity_data(client):
    response = client.get("/activities")

    assert response.status_code == 200
    payload = response.json()
    assert "Chess Club" in payload
    assert payload["Chess Club"]["participants"] == [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]


def test_signup_adds_student_to_activity(client):
    response = client.post("/activities/Chess%20Club/signup", params={"email": "student@mergington.edu"})

    assert response.status_code == 200
    assert response.json()["message"] == "Signed up student@mergington.edu for Chess Club"

    payload = client.get("/activities").json()
    assert "student@mergington.edu" in payload["Chess Club"]["participants"]


def test_duplicate_signup_is_rejected(client):
    response = client.post("/activities/Chess%20Club/signup", params={"email": "michael@mergington.edu"})

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_removes_student_from_activity(client):
    client.post("/activities/Chess%20Club/signup", params={"email": "newstudent@mergington.edu"})

    response = client.delete("/activities/Chess%20Club/signup", params={"email": "newstudent@mergington.edu"})

    assert response.status_code == 200
    assert response.json()["message"] == "Unregistered newstudent@mergington.edu from Chess Club"

    payload = client.get("/activities").json()
    assert "newstudent@mergington.edu" not in payload["Chess Club"]["participants"]


def test_signup_for_unknown_activity_returns_404(client):
    response = client.post("/activities/Unknown%20Club/signup", params={"email": "student@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
