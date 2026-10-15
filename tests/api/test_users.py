import httpx

from framework.factories import new_user


def test_register_user(settings):
    user = new_user()

    response = httpx.post(f"{settings.api_base_url}/users", json={"user": user})

    assert response.status_code == 201, response.text
    assert response.json()["user"]["email"] == user["email"]


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
