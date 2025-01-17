import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from ..entities.roles import Role
from ..repos.roles import RoleRepository, RoleNotFoundError
from ..schemas.roles import RoleResponse

# Mocking the session factory
@pytest.fixture
def mock_session():
    mock_session_factory = MagicMock()
    mock_session_instance = MagicMock()
    mock_session_factory.return_value.__enter__.return_value = mock_session_instance
    return mock_session_factory

# Test for get_all function
def test_get_all(mock_session):
    role_repo = RoleRepository(mock_session)
    mock_session_instance = mock_session.return_value.__enter__.return_value
    
    # Mocking role query result
    mock_session_instance.query.return_value.all.return_value = [
        Role(role_id=1, role_name="Admin", is_admin=True, created_at=datetime.now())
    ]
    
    result = role_repo.get_all()
    
    assert len(result) == 1
    assert result[0].role_name == "Admin"
    assert result[0].is_admin is True

# Test for add_role function
def test_add_role(mock_session):
    role_repo = RoleRepository(mock_session)
    mock_session_instance = mock_session.return_value.__enter__.return_value
    
    # Mocking session operations
    mock_session_instance.add.return_value = None
    mock_session_instance.commit.return_value = None
    mock_session_instance.refresh.return_value = None
    
    result = role_repo.add_role(2, "User", False)
    
    # Using RoleResponse.from_orm to convert Role to RoleResponse
    role = Role(role_id=2, role_name="User", is_admin=False, created_at=datetime.now())
    expected_response = {"Added Successfully!": RoleResponse.from_orm(role)}
    
    assert result == expected_response

# Test for update_role function
def test_update_role(mock_session):
    role_repo = RoleRepository(mock_session)
    mock_session_instance = mock_session.return_value.__enter__.return_value
    
    # Mocking the query to return an existing role
    mock_session_instance.query.return_value.filter.return_value.first.return_value = Role(
        role_id=1, role_name="Admin", is_admin=True, created_at=datetime.now()
    )
    
    # Mocking session operations
    mock_session_instance.commit.return_value = None
    mock_session_instance.refresh.return_value = None
    
    result = role_repo.update_role_roleRepo(1, "SuperAdmin", True)
    
    role = Role(role_id=1, role_name="SuperAdmin", is_admin=True, created_at=datetime.now(), updated_at=datetime.now())
    expected_response = {"Updated successfully!": RoleResponse.from_orm(role)}
    
    # Check if RoleResponse is correctly mapped
    assert result == expected_response

# Test for delete_role_by_role_id function
def test_delete_role_by_role_id(mock_session):
    role_repo = RoleRepository(mock_session)
    mock_session_instance = mock_session.return_value.__enter__.return_value
    
    # Mocking the query to return an existing role
    mock_session_instance.query.return_value.filter.return_value.first.return_value = Role(
        role_id=1, role_name="Admin", is_admin=True, created_at=datetime.now()
    )
    
    # Mocking session operations
    mock_session_instance.commit.return_value = None
    
    result = role_repo.delete_role_by_role_id(1)
    
    assert result == "Deleted Successfully!"

def test_get_role_fromRepo_by_id(mock_session):
    role_repo = RoleRepository(mock_session)
    mock_session_instance = mock_session.return_value.__enter__.return_value
    
    # Mocking the query to return an existing role
    mock_session_instance.query.return_value.filter.return_value.first.return_value = Role(
        role_id=1, role_name="Admin", is_admin=True, created_at=datetime.now()
    )
    
    result = role_repo.get_role_fromRepo_by_id(1)
    
    # Check if RoleResponse is correctly mapped
    assert result.role_name == "Admin"
    assert result.is_admin is True
