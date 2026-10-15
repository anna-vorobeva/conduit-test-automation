import httpx

from framework.factories import new_article


def test_create_article(settings, registered_user):
    article = new_article()
    headers = {"Authorization": f"Token {registered_user['token']}"}

    response = httpx.post(
        f"{settings.api_base_url}/articles", json={"article": article}, headers=headers
    )

    assert response.status_code == 201, response.text
    created = response.json()["article"]
    assert created["title"] == article["title"]
    assert sorted(created["tagList"]) == sorted(article["tagList"])
    assert created["author"]["username"] == registered_user["username"]


def test_create_article_without_token_is_rejected(settings):
    response = httpx.post(f"{settings.api_base_url}/articles", json={"article": new_article()})

    assert response.status_code == 401, response.text
