from framework.factories import new_user


def test_register_user(api):
    user = new_user()

    response = api.users.register(user)

    assert response.status_code == 201, response.text
    assert response.json()["user"]["email"] == user["email"]


def test_login_returns_token(api, registered_user):
    response = api.users.login(registered_user["email"], registered_user["password"])

    assert response.status_code == 200, response.text
    assert response.json()["user"]["token"]


def test_login_with_wrong_password_is_rejected(api, registered_user):
    response = api.users.login(registered_user["email"], "wrong-password")

    assert response.status_code == 401, response.text
    assert response.json() == {"errors": {"credentials": ["invalid"]}}


def test_registered_user_is_stored_with_hashed_password(api, db):
    user = new_user()
    api.users.register(user).raise_for_status()

    row = db.find_user(user["email"])

    assert row is not None
    assert row["username"] == user["username"]
    assert row["password"].startswith("pbkdf2_sha256$")
    assert user["password"] not in row["password"]
