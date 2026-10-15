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


def test_update_article_body(user_api, article):
    response = user_api.articles.update(article["slug"], {"body": "Updated body"})

    assert response.status_code == 200, response.text
    assert response.json()["article"]["body"] == "Updated body"


def test_delete_article(user_api, api, article):
    response = user_api.articles.delete(article["slug"])

    assert response.status_code == 204, response.text
    assert api.articles.get(article["slug"]).status_code == 404


def test_created_article_is_stored_in_db(user_api, db):
    article = new_article()
    slug = user_api.articles.create(article).json()["article"]["slug"]

    row = db.find_article(slug)

    assert row is not None
    assert row["title"] == article["title"]
    assert row["summary"] == article["description"]
    assert row["content"] == article["body"]


def test_deleted_article_is_removed_from_db(user_api, db, article):
    user_api.articles.delete(article["slug"]).raise_for_status()

    assert db.find_article(article["slug"]) is None
