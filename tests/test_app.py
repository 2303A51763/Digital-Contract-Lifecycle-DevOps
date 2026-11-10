import os
import tempfile
import pytest
from app import app, init_db

@pytest.fixture()
def client():
    fd, path = tempfile.mkstemp()
    os.close(fd)
    app.config["TESTING"] = True
    import app as app_module
    app_module.DB_PATH = path
    init_db()
    with app.test_client() as client:
        yield client
    os.unlink(path)

def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "healthy"

def test_create_and_approve_contract(client):
    response = client.post("/contracts/new", data={
        "title": "NDA", "department": "Legal", "owner": "Asha",
        "description": "Confidentiality agreement"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"NDA" in response.data
    response = client.post("/contracts/1/decision",
                           data={"action": "Approved", "note": "Reviewed"},
                           follow_redirects=True)
    assert b"Approved" in response.data
