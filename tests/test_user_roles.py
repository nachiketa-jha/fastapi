from contextlib import contextmanager
from unittest import mock
from sqlalchemy import create_engine
import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from ..schemas.user_roles import UserRoleResponse
from ..repos.user_roles import UserRoleRepository, UserRoleNotFoundError, userRole_NotFoundError
from ..entities.user_roles import UserRole
from ..application import app

engine = create_engine("sqlite:///:memory:", echo=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_test_session():
    session = TestingSessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

@pytest.fixture
def user_role_repo():
    UserRole.metadata.drop_all(bind=engine)
    UserRole.metadata.create_all(bind=engine)
    return UserRoleRepository(session_factory=get_test_session)

@pytest.fixture
def sample_user_role(user_role_repo):
    user_role_repo.add_user_role(user_role_id=1, user_id=21, role_id=41)
    return user_role_repo.getUserRole(1)

@pytest.fixture
def client():
    yield TestClient(app)


def test_get_all(user_role_repo, sample_user_role):
    users = user_role_repo.get_all()
    assert len(users) == 1
    assert users[0].user_id == 21

def test_get_by_id(user_role_repo, sample_user_role):
    user_role = user_role_repo.getUserRole(1)
    assert user_role.user_id == 21
    with pytest.raises(userRole_NotFoundError):
        user_role_repo.getUserRole(999)

def test_add_user_role(user_role_repo):
    response = user_role_repo.add_user_role(user_role_id=2, user_id=23, role_id=43)
    user_role_response = response["Added successfully"]
    assert user_role_response.user_id == 23
    assert user_role_response.role_id == 43
    assert user_role_response.user_role_id == 2

def test_delete_by_id(user_role_repo, sample_user_role):
    user_role_repo.delete_user_role(21)
    with pytest.raises(UserRoleNotFoundError):
        user_role_repo.getUserRole(1)

def test_update_user_role(user_role_repo, sample_user_role):
    response = user_role_repo.update_user_role(1, user_id=22, role_id=42)
    user_role_response = response["Updated Successfully"]
    assert user_role_response.user_id == 22
    assert user_role_response.role_id == 42
    with pytest.raises(ValueError):
        user_role_repo.update_user_role(999, user_id=100, role_id=200)