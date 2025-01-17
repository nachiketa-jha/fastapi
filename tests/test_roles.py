import pytest
from unittest.mock import MagicMock
from datetime import datetime, timedelta
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


# Helper function to compare datetimes with tolerance for 'updated_at'
def compare_datetime_with_tolerance(actual, expected, tolerance_seconds=1):
    if not expected:
        return actual is None
    return abs((actual - expected).total_seconds()) <= tolerance_seconds


# Helper function to manually convert Role to RoleResponse
def convert_role_to_role_response(role: Role) -> RoleResponse:
    return RoleResponse(
        role_id=role.role_id,
        role_name=role.role_name,
        is_admin=role.is_admin,
        created_at=role.created_at,
        updated_at=role.updated_at
    )


# Test for get_all function
def test_get_all(mock_session):
    role_repo = RoleRepository(mock_session)
    mock_session_instance = mock_session.return_value.__enter__.return_value
    
    # Mocking role query result
    role_instance = Role(role_id=1, role_name="Admin", is_admin=True, created_at=datetime.now())
    mock_session_instance.query.return_value.all.return_value = [role_instance]
    
    result = role_repo.get_all()
    
    # Creating expected RoleResponse manually
    expected_response = [convert_role_to_role_response(role_instance)]
    
    # Assert that the result matches the expected response
    assert result == expected_response


# Test for add_role function
def test_add_role(mock_session):
    role_repo = RoleRepository(mock_session)
    mock_session_instance = mock_session.return_value.__enter__.return_value
    
    # Mocking session operations
    role = Role(role_id=2, role_name="User", is_admin=False, created_at=datetime.now())
    mock_session_instance.add.return_value = None
    mock_session_instance.commit.return_value = None
    mock_session_instance.refresh.return_value = None
    
    result = role_repo.add_role(2, "User", False)
    
    # Creating expected response manually
    expected_response = {"Added Successfully!": convert_role_to_role_response(role)}
    
    assert result == expected_response


# Test for update_role function
def test_update_role(mock_session):
    role_repo = RoleRepository(mock_session)
    mock_session_instance = mock_session.return_value.__enter__.return_value
    
    # Mocking the query to return an existing role
    role_instance = Role(role_id=1, role_name="Admin", is_admin=True, created_at=datetime.now())
    mock_session_instance.query.return_value.filter.return_value.first.return_value = role_instance
    
    # Mocking session operations
    mock_session_instance.commit.return_value = None
    mock_session_instance.refresh.return_value = None
    
    # Updated role instance (including dynamic `updated_at`)
    updated_role_instance = Role(role_id=1, role_name="SuperAdmin", is_admin=True, created_at=datetime.now(), updated_at=datetime.now())
    
    result = role_repo.update_role_roleRepo(1, "SuperAdmin", True)
    
    # Creating expected response manually
    expected_response = {"Updated successfully!": convert_role_to_role_response(updated_role_instance)}
    
    # Compare everything except `updated_at` with tolerance
    assert result["Updated successfully!"].role_name == "SuperAdmin"
    assert result["Updated successfully!"].is_admin is True
    assert compare_datetime_with_tolerance(result["Updated successfully!"].updated_at, updated_role_instance.updated_at)


# Test for delete_role_by_role_id function
def test_delete_role_by_role_id(mock_session):
    role_repo = RoleRepository(mock_session)
    mock_session_instance = mock_session.return_value.__enter__.return_value
    
    # Mocking the query to return an existing role
    role_instance = Role(role_id=1, role_name="Admin", is_admin=True, created_at=datetime.now())
    mock_session_instance.query.return_value.filter.return_value.first.return_value = role_instance
    
    # Mocking session operations
    mock_session_instance.commit.return_value = None
    
    result = role_repo.delete_role_by_role_id(1)
    
    assert result == "Deleted Successfully!"


# Test for get_role_fromRepo_by_id function
def test_get_role_fromRepo_by_id(mock_session):
    role_repo = RoleRepository(mock_session)
    mock_session_instance = mock_session.return_value.__enter__.return_value
    
    # Mocking the query to return an existing role
    role_instance = Role(role_id=1, role_name="Admin", is_admin=True, created_at=datetime.now())
    mock_session_instance.query.return_value.filter.return_value.first.return_value = role_instance
    
    result = role_repo.get_role_fromRepo_by_id(1)
    
    # Creating expected RoleResponse manually
    expected_response = convert_role_to_role_response(role_instance)
    
    # Assert that the result matches the expected response
    assert result == expected_response
