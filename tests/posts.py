from unittest import mock

import pytest
from fastapi.testclient import TestClient

from ..repos.posts import PostRepository, PostNotFoundError
from ..entities.posts import Post
from ..application import app


@pytest.fixture
def client():
    yield TestClient(app)


def test_get_list(client):
    repository_mock = mock.Mock(spec=PostRepository)
    repository_mock.get_all.return_value = [
        Post(post_id=1, post_text="test1", user_id=1),
        Post(post_id=2, post_text="test2", user_id=2),
    ]

    with app.container.post_repository.override(repository_mock):
        response = client.get("/posts")

    assert response.status_code == 200
    data = response.json()
    assert data == [
        {"post_id": 1, "post_text": "test1", "user_id": 1},
        {"post_id": 2, "post_text": "test2", "user_id": 2},
    ]


def test_get_by_id(client):
    repository_mock = mock.Mock(spec=PostRepository)
    repository_mock.get_by_id.return_value = Post(
        post_id=1,
        post_text="xyz",
        user_id=1,
            )

    with app.container.post_repository.override(repository_mock):
        response = client.get("/posts/1")

    assert response.status_code == 200
    data = response.json()
    assert data == {"post_id": 1, "post_text": "xyz", "user_id": 1}
    repository_mock.get_by_id.assert_called_once_with(1)
    assert repository_mock.get_by_id.call_count == 2


def test_get_by_id_404(client):
    repository_mock = mock.Mock(spec=PostRepository)
    repository_mock.get_by_id.side_effect = PostNotFoundError(1)

    with app.container.post_repository.override(repository_mock):
        response = client.get("/posts/1")

    assert response.status_code == 404


@mock.patch("services.users", return_value="xyz")
def test_add(_, client):
    repository_mock = mock.Mock(spec=PostRepository)
    repository_mock.add.return_value = Post(
        post_id=1,
        post_text="xyz",
        user_id="pwd",
    )

    with app.container.post_repository.override(repository_mock):
        response = client.post("/posts", json={"post_text": "xyz", "user_id": 1})

    assert response.status_code == 405
    data = response.json()
    assert data == {"post_id": 1, "post_text": "xyz"}
    repository_mock.add.assert_called_once_with(post_text="xyz", user_id=1)


def test_remove(client):
    repository_mock = mock.Mock(spec=PostRepository)

    with app.container.post_repository.override(repository_mock):
        response = client.delete("/posts/1")

    assert response.status_code == 204
    repository_mock.delete_by_id.assert_called_once_with(1)


def test_remove_404(client):
    repository_mock = mock.Mock(spec=PostRepository)
    repository_mock.delete_by_id.side_effect = PostNotFoundError(1)

    with app.container.post_repository.override(repository_mock):
        response = client.delete("/posts/1")

    assert response.status_code == 404


def test_status(client):
    response = client.get("/status")
    assert response.status_code == 200
    data = response.json()
    assert data == {"status": "OK"}