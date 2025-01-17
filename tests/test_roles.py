from unittest import mock

import pytest
from fastapi.testclient import TestClient

from ..repos.roles import RoleRepository, RoleNotFoundError
from ..entities.roles import Role
from ..application import app


@pytest.fixture
def client():
    yield TestClient(app)


def test_get_list(client):
    repository_mock = mock.Mock(spec=RoleRepository)
    repository_mock.get_all.return_value = [
        Role(role_id=1, role_name="test1", is_admin=True),
        Role(role_id=2, role_name="test2", is_admin=False),
    ]

    with app.container.Role_repository.override(repository_mock):
        response = client.get("/roles")

    assert response.status_code == 200
    data = response.json()
    assert data == [
        {"role_id": 1, "role_name": "test1", "is_admin": True},
        {"role_id": 2, "role_name": "test2", "is_admin": False},
    ]


def test_get_by_id(client):
    repository_mock = mock.Mock(spec=RoleRepository)
    repository_mock.get_by_id.return_value = Role(
        role_id=1,
        role_name="xyz",
        is_admin=True,
            )

    with app.container.Role_repository.override(repository_mock):
        response = client.get("/roles/1")

    assert response.status_code == 200
    data = response.json()
    assert data == {"role_id": 1, "role_name": "xyz", "is_admin": True}
    repository_mock.get_by_id.assert_called_once_with(1)
    assert repository_mock.get_by_id.call_count == 2


# def test_get_by_id_404(client):
#     repository_mock = mock.Mock(spec=RoleRepository)
#     repository_mock.get_by_id.side_effect = RoleNotFoundError(1)

#     with app.container.Role_repository.override(repository_mock):
#         response = client.get("/roles/1")

#     assert response.status_code == 404


@mock.patch("services.roles", return_value="xyz")
def test_add(_, client):
    repository_mock = mock.Mock(spec=RoleRepository)
    repository_mock.add.return_value = Role(
        role_id=1,
        role_name="xyz",
        is_admin=True,
    )

    with app.container.Role_repository.override(repository_mock):
        response = client.post("/roles", json={"role_name": "xyz", "is_admin": True})

    assert response.status_code == 405
    data = response.json()
    assert data == {"role_id": 1, "role_name": "xyz"}
    repository_mock.add.assert_called_once_with(role_name="xyz", is_admin=True)


def test_remove(client):
    repository_mock = mock.Mock(spec=RoleRepository)

    with app.container.Role_repository.override(repository_mock):
        response = client.delete("/roles/1")

    assert response.status_code == 204
    repository_mock.delete_by_id.assert_called_once_with(1)


# def test_remove_404(client):
#     repository_mock = mock.Mock(spec=RoleRepository)
#     repository_mock.delete_by_id.side_effect = RoleNotFoundError(1)

#     with app.container.Role_repository.override(repository_mock):
#         response = client.delete("/roles/1")

#     assert response.status_code == 404


# def test_status(client):
#     response = client.get("/status")
#     assert response.status_code == 200
#     data = response.json()
#     assert data == {"status": "OK"}