import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture(scope="module")
def created_submission():
    # Create a submission test
    payload = {
        "user_id":123,
        "code":"print('hello test')",
        "result":"OK"
    }
    res = client.post("/submissions/", json=payload)
    assert res.status_code == 201
    data = res.json()
    # Store the object for later use
    return data

def test_list_submissions(created_submission):
    # List all submissions
    res = client.get("/submissions/")
    assert res.status_code == 200
    lst = res.json()
    assert any(s["submission_id"] == created_submission["submission_id"] for s in lst)

def test_get_submission(created_submission):
    # Get the created submission by ID
    sub_id = created_submission["submission_id"]
    res = client.get(f"/submissions/{sub_id}")
    assert res.status_code == 200
    data = res.json()
    assert data["user_id"] == created_submission["user_id"]
    assert data["code"] == created_submission["code"]

def test_update_submission(created_submission):
    # Updata only field 'result'
    sub_id = created_submission["submission_id"]
    update = {"result": "FAIL"}
    res = client.put(f"/submissions/{sub_id}", json=update)
    assert res.status_code == 200
    data = res.json()
    assert data["result"] == "FAIL"

def test_delete_submission(created_submission):
    # Delete the created submission
    sub_id = created_submission["submission_id"]
    res = client.delete(f"/submissions/{sub_id}")
    assert res.status_code == 204

    # Verify that the submission is deleted
    res = client.get(f"/submissions/{sub_id}")
    assert res.status_code == 404

def test_create_multiple_submissions():
    submissions = []
    for i in range(3):
        payload = {
            "user_id": 200 + i,
            "code": f"print('Test submission {i}')",
            "result": "PENDING"
        }
        res = client.post("/submissions/", json=payload)
        assert res.status_code == 201
        data = res.json()
        submissions.append(data)
    
    res = client.get("/submissions/")
    assert res.status_code == 200
    all_submissions = res.json()

    created_ids = [s["submission_id"] for s in submissions]
    existing_ids = [s["submission_id"] for s in all_submissions]
    
    for sub_id in created_ids:
        assert sub_id in existing_ids
    

    for submission in submissions:
        sub_id = submission["submission_id"]
        res = client.delete(f"/submissions/{sub_id}")
        assert res.status_code == 204