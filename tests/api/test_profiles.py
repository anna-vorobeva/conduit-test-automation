from framework.models import Profile


def test_follow_user(user_api, another_user):
    response = user_api.profiles.follow(another_user["username"])

    assert response.status_code == 200, response.text
    assert Profile.model_validate(response.json()["profile"]).following is True
    profile_response = user_api.profiles.get(another_user["username"])
    assert Profile.model_validate(profile_response.json()["profile"]).following is True


def test_unfollow_user(user_api, another_user):
    user_api.profiles.follow(another_user["username"]).raise_for_status()

    response = user_api.profiles.unfollow(another_user["username"])

    assert response.status_code == 200, response.text
    assert Profile.model_validate(response.json()["profile"]).following is False
