from contextlib import contextmanager
from unittest import mock
from sqlalchemy import create_engine
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from repos.user_roles import UserRoleRepository, UserRoleNotFoundError
from schemas.user_roles import UserRole
from application import app
from services.user_roles import UserRoleService

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
    if not user_role_repo.get_all():
        user_role_repo.add_user_role(user_role_id=0, user_id=0, role_id=0)
    return user_role_repo.getUserRole(0)

@pytest.fixture
def client():
    yield TestClient(app)


def test_get_all(user_role_repo, sample_user_role):
    user_roles = user_role_repo.get_all()
    assert len(user_roles) == 1
    assert user_roles[0].user_role_id == 0

def test_get_by_id(user_role_repo, sample_user_role):
    user_roles = user_role_repo.getUserRole(0)
    assert user_roles.user_role_id == 0
    with pytest.raises(UserRoleNotFoundError):
        user_role_repo.getUserRole(999)

def test_add_user_role(user_role_repo):
    response = user_role_repo.add_user_role(user_role_id=1, user_id=1, role_id=1)
    assert response.user_role_id == 1

def test_delete_by_id(user_role_repo, sample_user_role):
    with mock.patch.object(user_role_repo, 'delete_user_role') as mock_delete_user_role:
        user_role_repo.delete_user_role(0)
        mock_delete_user_role.assert_called_once()
    with pytest.raises(UserRoleNotFoundError):
        user_role_repo.delete_user_role(999)

def test_update_user(user_role_repo, sample_user_role):
    response = user_role_repo.update_user_role(user_role_id=0, user_id=2, role_id=2)
    assert response.user_role_id == 0
    assert response.user_id == 2
    with pytest.raises(UserRoleNotFoundError):
        user_role_repo.update_user_role(999,999,999)

def test_get_user_roles():
    mock_repo = mock.Mock(spec=UserRoleRepository)
    mock_repo.get_all.return_value = [{"user_id": 1, "user_role_id": 1,"role_id":1}]
    
    user_role_service = UserRoleService(mock_repo)
    
    user_roles = user_role_service.get_all()
    
    assert len(user_roles) == 1
    assert user_roles[0]["user_role_id"] == 1
    assert user_roles[0]["user_id"] == 1
    assert user_roles[0]["role_id"] == 1

def test_get_user_role_by_id():
    mock_repo = mock.Mock(spec=UserRoleRepository)
    mock_repo.getUserRole.return_value = {"user_id": 1, "user_role_id": 1,"role_id":1}
    
    user_role_service = UserRoleService(mock_repo)
    
    user_roles = user_role_service.get_userRole(1)
    
    assert user_roles["user_role_id"] == 1
    assert user_roles["user_id"] == 1
    assert user_roles["role_id"] == 1
    

def test_update_user_role_service():
    mock_repo = mock.Mock(spec=UserRoleRepository)
    mock_repo.update_user_role.return_value = {"user_id": 2, "user_role_id": 2,"role_id":1}
    
    user_role_service = UserRoleService(mock_repo)
    
    result = user_role_service.update_user_role(2,2,1)
    
    assert result["user_role_id"] == 2
    assert result["user_id"] == 2
    assert result["role_id"] == 1

def test_delete_user_role_by_id():
    mock_repo = mock.Mock(spec=UserRoleRepository)
    
    user_role_service = UserRoleService(mock_repo)
    
    user_role_service.delete_user_role(1)
    
    mock_repo.delete_user_role.assert_called_once_with(1)