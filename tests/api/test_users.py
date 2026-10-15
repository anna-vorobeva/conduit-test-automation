from uuid import uuid4

import httpx


def test_register_user(settings):
    suffix = uuid4().hex[:8]
    payload = {
        "user": {
            "username": f"user_{suffix}",
            "email": f"user_{suffix}@example.com",
            "password": "Secret-123",
        }
    }

    response = httpx.post(f"{settings.api_base_url}/users", json=payload)

    assert response.status_code == 201, response.text
    assert response.json()["user"]["email"] == payload["user"]["email"]


def test_login_returns_token(settings, registered_user):
    payload = {"user": {"email": registered_user["email"], "password": registered_user["password"]}}

    response = httpx.post(f"{settings.api_base_url}/users/login", json=payload)

    assert response.status_code == 200, response.text
    assert response.json()["user"]["token"]


def test_login_with_wrong_password_is_rejected(settings, registered_user):
    payload = {"user": {"email": registered_user["email"], "password": "wrong-password"}}

    response = httpx.post(f"{settings.api_base_url}/users/login", json=payload)

    assert response.status_code == 401, response.text
    assert response.json() == {"errors": {"credentials": ["invalid"]}}
