from unittest import mock

import pytest
from fastapi.testclient import TestClient

from ..repos.user_roles import UserRoleRepository, UserRoleNotFoundError
from ..entities.user_roles import UserRole
from ..application import app


@pytest.fixture
def client():
    yield TestClient(app)


def test_get_list(client):
    repository_mock = mock.Mock(spec=UserRoleRepository)
    repository_mock.get_all.return_value = [
        UserRole(user_role_id=1, user_id=1, role_id=1),
        UserRole(user_role_id=2, user_id=2, role_id=2),
    ]

    with app.container.user_role_repository.override(repository_mock):
        response = client.get("/user_roles")

    assert response.status_code == 200
    data = response.json()
    assert data == [
        {"user_role_id": 1, "user_id": 1, "role_id": 1},
        {"user_role_id": 2, "user_id": 2, "role_id": 2},
    ]


def test_get_by_id(client):
    repository_mock = mock.Mock(spec=UserRoleRepository)
    repository_mock.get_by_id.return_value = UserRole(
        user_role_id=1,
        user_id=1,
        role_id=1,
            )

    with app.container.user_role_repository.override(repository_mock):
        response = client.get("/user_roles/1")

    assert response.status_code == 200
    data = response.json()
    assert data == {"user_role_id": 1, "user_id": 1, "role_id": 1}
    repository_mock.get_by_id.assert_called_once_with(1)
    assert repository_mock.get_by_id.call_count == 2


# def test_get_by_id_404(client):
#     repository_mock = mock.Mock(spec=UserRoleRepository)
#     repository_mock.get_by_id.side_effect = UserRoleNotFoundError(1)

#     with app.container.user_role_repository.override(repository_mock):
#         response = client.get("/user_roles/1")

#     assert response.status_code == 404


@mock.patch("services.user_roles", return_value="xyz")
def test_add(_, client):
    repository_mock = mock.Mock(spec=UserRoleRepository)
    repository_mock.add.return_value = UserRole(
        user_role_id=1,
        user_id=1,
        role_id=1,
    )

    with app.container.user_role_repository.override(repository_mock):
        response = client.post("/user_roles", json={"user_id": 1, "role_id": 1})

    assert response.status_code == 405
    data = response.json()
    assert data == {"user_role_id": 1, "user_id":1}
    repository_mock.add.assert_called_once_with(user_id=1, role_id=1)


def test_remove(client):
    repository_mock = mock.Mock(spec=UserRoleRepository)

    with app.container.user_role_repository.override(repository_mock):
        response = client.delete("/user_roles/1")

    assert response.status_code == 204
    repository_mock.delete_by_id.assert_called_once_with(1)


# def test_remove_404(client):
#     repository_mock = mock.Mock(spec=UserRoleRepository)
#     repository_mock.delete_by_id.side_effect = UserRoleNotFoundError(1)

#     with app.container.user_role_repository.override(repository_mock):
#         response = client.delete("/user_roles/1")

#     assert response.status_code == 404


# def test_status(client):
#     response = client.get("/status")
#     assert response.status_code == 200
#     data = response.json()
#     assert data == {"status": "OK"}