from contextlib import contextmanager
from unittest import mock
from sqlalchemy import create_engine
import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from schemas.user import UserResponse
from ..repos.users import UserRepository, UserNotFoundError
from ..entities.users import User
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
def user_repo():
    User.metadata.drop_all(bind=engine)
    User.metadata.create_all(bind=engine)
    return UserRepository(session_factory=get_test_session)

@pytest.fixture
def sample_user(user_repo):
    if not user_repo.get_all():  # Add user only if table is empty
        user_repo.add(user_id=1, username="testuser", password="testpass")
    return user_repo.get_by_id(1)

@pytest.fixture
def client():
    yield TestClient(app)


def test_get_all(user_repo, sample_user):
    users = user_repo.get_all()
    assert len(users) == 1
    assert users[0].username == "testuser"

def test_get_by_id(user_repo, sample_user):
    user = user_repo.get_by_id(1)
    assert user.username == "testuser"

    with pytest.raises(UserNotFoundError):
        user_repo.get_by_id(999)

def test_add_user(user_repo):
    response = user_repo.add(user_id=2, username="newuser", password="newpass")
    assert response["Added Successfully!"].username == "newuser"

def test_delete_by_id(user_repo, sample_user):
    user_repo.delete_by_id(1)
    with pytest.raises(UserNotFoundError):
        user_repo.get_by_id(1)

def test_update_user(user_repo, sample_user):
    response = user_repo.update_user(1, username="updateduser", password="updatedpass")
    assert response["Updated Successfully!"].username == "updateduser"
    
    with pytest.raises(ValueError):
        user_repo.update_user(999, username="nonexistent")