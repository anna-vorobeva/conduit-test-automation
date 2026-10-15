import pytest


@pytest.mark.smoke
def test_tags_endpoint_is_reachable(api):
    response = api.tags.list()

    assert response.status_code == 200
    assert isinstance(response.json()["tags"], list)
