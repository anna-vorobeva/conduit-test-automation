from framework.factories import new_article


def test_create_article(user_api, registered_user):
    article = new_article()

    response = user_api.articles.create(article)

    assert response.status_code == 201, response.text
    created = response.json()["article"]
    assert created["title"] == article["title"]
    assert sorted(created["tagList"]) == sorted(article["tagList"])
    assert created["author"]["username"] == registered_user["username"]


def test_create_article_without_token_is_rejected(api):
    response = api.articles.create(new_article())

    assert response.status_code == 401, response.text
