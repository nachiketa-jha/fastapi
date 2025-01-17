from unittest import mock

import pytest
from fastapi.testclient import TestClient

from ..repos.users import UserRepository, UserNotFoundError
from ..entities.users import User
from ..application import app


@pytest.fixture
def client():
    yield TestClient(app)


def test_get_list(client):
    repository_mock = mock.Mock(spec=UserRepository)
    repository_mock.get_all.return_value = [
        User(user_id=1, username="test1", password="pwd"),
        User(user_id=2, username="test2", password="pwd"),
    ]

    with app.container.user_repository.override(repository_mock):
        response = client.get("/users")

    assert response.status_code == 200
    data = response.json()
    assert data == [
        {"user_id": 1, "username": "test1", "password": "pwd"},
        {"user_id": 2, "username": "test2", "password": "pwd"},
    ]


def test_get_by_id(client):
    repository_mock = mock.Mock(spec=UserRepository)
    repository_mock.get_by_id.return_value = User(
        user_id=1,
        username="xyz",
        password="pwd",
            )

    with app.container.user_repository.override(repository_mock):
        response = client.get("/users/1")

    assert response.status_code == 200
    data = response.json()
    assert data == {"user_id": 1, "username": "xyz", "password": "pwd"}
    repository_mock.get_by_id.assert_called_once_with(1)
    assert repository_mock.get_by_id.call_count == 2


# def test_get_by_id_404(client):
#     repository_mock = mock.Mock(spec=UserRepository)
#     repository_mock.get_by_id.side_effect = UserNotFoundError(1)

#     with app.container.user_repository.override(repository_mock):
#         response = client.get("/users/1")

#     assert response.status_code == 404


@mock.patch("services.users", return_value="xyz")
def test_add(_, client):
    repository_mock = mock.Mock(spec=UserRepository)
    repository_mock.add.return_value = User(
        user_id=1,
        username="xyz",
        password="pwd",
    )

    with app.container.user_repository.override(repository_mock):
        response = client.post("/users", json={"username": "xyz", "password": "pwd"})

    assert response.status_code == 405
    data = response.json()
    assert data == {"user_id": 1, "username": "xyz"}
    repository_mock.add.assert_called_once_with(username="xyz", password="pwd")


def test_remove(client):
    repository_mock = mock.Mock(spec=UserRepository)

    with app.container.user_repository.override(repository_mock):
        response = client.delete("/users/1")

    assert response.status_code == 204
    repository_mock.delete_by_id.assert_called_once_with(1)


# def test_remove_404(client):
#     repository_mock = mock.Mock(spec=UserRepository)
#     repository_mock.delete_by_id.side_effect = UserNotFoundError(1)

#     with app.container.user_repository.override(repository_mock):
#         response = client.delete("/users/1")

#     assert response.status_code == 404


def test_status(client):
    response = client.get("/status")
    assert response.status_code == 200
    data = response.json()
    assert data == {"status": "OK"}