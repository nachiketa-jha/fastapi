
from contextlib import contextmanager
from unittest import mock
from sqlalchemy import create_engine
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from repos.users import UserNotFoundError, UserRepository
from schemas.user import User
from application import app
from services.users import UserService

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

# repo
@pytest.fixture
def user_repo():
    User.metadata.drop_all(bind=engine)
    User.metadata.create_all(bind=engine)
    return UserRepository(session_factory=get_test_session)

@pytest.fixture
def sample_user(user_repo):
    if not user_repo.get_all():  # Add user only if table is empty
        user_repo.add(user_id=1, uname="testuser", password="testpass")
    return user_repo.get_by_id(1)

@pytest.fixture
def client():
    yield TestClient(app)

def test_get_all(user_repo, sample_user):
    users = user_repo.get_all()
    assert len(users) == 1
    assert users[0].uname == "testuser"
    assert users[0].user_id == 1

def test_get_by_id(user_repo, sample_user):
    user = user_repo.get_by_id(1)
    assert user.uname == "testuser"
    assert user.user_id == 1
    with pytest.raises(UserNotFoundError):
        user_repo.get_by_id(999)

def test_add_user(user_repo):
    response = user_repo.add(user_id=2, uname="newuser", password="newpass")
    assert response.uname == "newuser"
    assert response.user_id == 2

def test_delete_by_id(user_repo, sample_user):
    user_repo.delete_by_id(1)
    with mock.patch.object(user_repo, 'delete_by_id') as mock_delete_user:
        user_repo.delete_by_id(0)
        mock_delete_user.assert_called_once()
    with pytest.raises(UserNotFoundError):
        user_repo.delete_by_id(999)


def test_update_user(user_repo, sample_user):
    response = user_repo.update_user(1, uname="updateduser", password="updatedpass")
    assert response.uname == "updateduser"
    with pytest.raises(UserNotFoundError):
        user_repo.update_user(999)

# Test for getting all users

def test_create_users():
    mock_repo = mock.Mock(spec=UserRepository)
    mock_repo.add.return_value = {"user_id": 1, "uname": "testuser","created_at":"now"}
    user_service = UserService(mock_repo)
    
    users = user_service.create_user(user_id=1,uname="testuser",password="Valid@1234")
    
    assert users["uname"] == "testuser"
    assert users["user_id"] == 1


def test_get_users():
    mock_repo = mock.Mock(spec=UserRepository)
    mock_repo.get_all.return_value = [{"user_id": 1, "uname": "testuser"}]
    
    user_service = UserService(mock_repo)
    
    users = user_service.get_users()
    
    assert len(users) == 1
    assert users[0]["uname"] == "testuser"
    assert users[0]["user_id"] == 1

def test_get_user_by_id():
    mock_repo = mock.Mock(spec=UserRepository)
    mock_repo.get_by_id.return_value = {"user_id": 1, "uname": "testuser"}
    
    user_service = UserService(mock_repo)
    
    user = user_service.get_user_by_id(1)
    
    assert user["uname"] == "testuser"
    assert user["user_id"] == 1

def test_update_user_service():
    mock_repo = mock.Mock(spec=UserRepository)
    mock_repo.update_user.return_value = {"user_id": 1, "uname": "updateduser", "updated_at": "now"}
    
    user_service = UserService(mock_repo)
    
    result = user_service.update_user_service(1, "updateduser", "NewPass123!")
    
    assert result["user_id"] == 1
    assert result["uname"] == "updateduser"
    mock_repo.update_user.assert_called_once_with(1, "updateduser", mock.ANY)

def test_delete_user_by_id():
    mock_repo = mock.Mock(spec=UserRepository)
    
    user_service = UserService(mock_repo)
    
    user_service.delete_user_by_id(1)
    
    mock_repo.delete_by_id.assert_called_once_with(1)

# def test_login_user():
#     mock_repo = mock.Mock(spec=UserRepository)
    
#     user_service = UserService(mock_repo)

#     user_service.login_user(1,"newpass")
