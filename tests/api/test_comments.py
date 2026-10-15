from framework.factories import new_comment


def test_add_comment_to_article(user_api, article, registered_user):
    comment = new_comment()

    response = user_api.comments.add(article["slug"], comment)

    assert response.status_code == 201, response.text
    created = response.json()["comment"]
    assert created["body"] == comment["body"]
    assert created["author"]["username"] == registered_user["username"]


def test_added_comment_appears_in_article_comments(user_api, api, article):
    created = user_api.comments.add(article["slug"], new_comment()).json()["comment"]

    response = api.comments.list(article["slug"])

    assert response.status_code == 200, response.text
    comment_ids = [comment["id"] for comment in response.json()["comments"]]
    assert created["id"] in comment_ids


def test_add_comment_without_token_is_rejected(api, article):
    response = api.comments.add(article["slug"], new_comment())

    assert response.status_code == 401, response.text
    assert response.json() == {"errors": {"token": ["is missing"]}}
