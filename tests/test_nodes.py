from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_register_user():
    response = client.post(
        "/register", json={"username": "testuser", "password": "testpass"}
    )

    assert response.status_code in (200, 400)


def test_login_user():
    response = client.post(
        "/login", json={"username": "testuser", "password": "testpass"}
    )

    assert response.status_code == 200
    assert "access_token" in response.json()


def get_token():
    response = client.post(
        "/login", json={"username": "testuser", "password": "testpass"}
    )
    return response.json()["access_token"]


def test_create_note():
    token = get_token()

    response = client.post(
        "/notes",
        json={"content": "hello test note"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["content"] == "hello test note"


def test_get_notes():
    token = get_token()

    response = client.get("/notes", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_delete_note():
    token = get_token()

    create = client.post(
        "/notes",
        json={"content": "to delete"},
        headers={"Authorization": f"Bearer {token}"},
    )

    note_id = create.json()["id"]

    delete = client.delete(
        f"/notes/{note_id}", headers={"Authorization": f"Bearer {token}"}
    )

    assert delete.status_code == 200
