from contextlib import contextmanager
from unittest import mock
from sqlalchemy import create_engine
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from repos.roles import RoleRepository, RoleNotFoundError
from schemas.roles import Role
from application import app
from services.roles import RoleService

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
def role_repo():
    Role.metadata.drop_all(bind=engine)
    Role.metadata.create_all(bind=engine)
    return RoleRepository(session_factory=get_test_session)

@pytest.fixture
def sample_user(role_repo):
    if not role_repo.get_all():  # Add user only if table is empty
        role_repo.add_role(role_id=0, role_name="testRole", is_admin=True)
    return role_repo.get_role_fromRepo_by_id(0)

@pytest.fixture
def client():
    yield TestClient(app)


def test_get_all(role_repo, sample_user):
    role = role_repo.get_all()
    assert len(role) == 1
    assert role[0].role_name == "testRole"

def test_get_by_id(role_repo, sample_user):
    role = role_repo.get_role_fromRepo_by_id(0)
    assert role.role_name == "testRole"
    with pytest.raises(RoleNotFoundError):
        role_repo.get_role_fromRepo_by_id(999)

def test_add_user(role_repo):
    response = role_repo.add_role(role_id=0, role_name="testRole", is_admin=True)
    assert response.role_name == "testRole"

def test_delete_by_id(role_repo, sample_user):
    role_repo.delete_role_by_role_id(0)
    with mock.patch.object(role_repo, 'delete_role_by_role_id') as mock_delete_role:
        role_repo.delete_role_by_role_id(0)
        mock_delete_role.assert_called_once()
    with pytest.raises(RoleNotFoundError):
        role_repo.delete_role_by_role_id(999)


def test_update_role(role_repo, sample_user):
    response = role_repo.update_role_roleRepo(role_id=0, role_name="testRole2", is_admin=False)
    assert response.role_name == "testRole2"
    assert response.is_admin == False
    with pytest.raises(RoleNotFoundError):
        role_repo.update_role_roleRepo(999,"Non-existing",False)

def test_get_roles():
    mock_repo = mock.Mock(spec=RoleRepository)
    mock_repo.get_all.return_value = [{"role_id": 1, "role_name": "testrole","is_admin":True}]
    
    role_service = RoleService(mock_repo)
    
    users = role_service.get_all_roleService()
    
    assert len(users) == 1
    assert users[0]["role_id"] == 1
    assert users[0]["role_name"] == "testrole"

def test_get_role_by_id():
    mock_repo = mock.Mock(spec=RoleRepository)
    mock_repo.get_role_fromRepo_by_id.return_value = [{"role_id": 1, "role_name": "testrole","is_admin":True}]
    role_service = RoleService(mock_repo)
    
    role = role_service.get_role(1)
    
    assert len(role) == 1
    assert role[0]["role_id"] == 1
    assert role[0]["role_name"] == "testrole"

def test_update_role_service():
    mock_repo = mock.Mock(spec=RoleRepository)
    mock_repo.update_role_roleRepo.return_value = [{"role_id": 1, "role_name": "updaterole","is_admin":True}]
    
    role_service = RoleService(mock_repo)
    
    result = role_service.update_role_roleService(1, "updaterole", True)
    
    assert result[0]["role_id"] == 1
    assert result[0]["role_name"] == "updaterole"

def test_delete_role_by_id():
    mock_repo = mock.Mock(spec=RoleRepository)
    
    role_service = RoleService(mock_repo)
    
    role_service.delete_role_by_id(1)
    
    mock_repo.delete_role_by_role_id.assert_called_once_with(1)