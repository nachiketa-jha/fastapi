import pytest
from sqlalchemy.orm import Session
from repos.users import UserRepository
from entities.users import User
from database import SessionLocal
from unittest.mock import MagicMock
from datetime import datetime

# Fixture to mock the session factory
@pytest.fixture
def mock_session_factory():
    mock_session = MagicMock(spec=Session)
    return mock_session

@pytest.fixture
def user_repository(mock_session_factory):
    return UserRepository(session_factory=lambda: mock_session_factory)

def test_add_user(user_repository, mock_session_factory):
    user_data = {
        'user_id': 1,
        'username': 'testuser',
        'password': 'hashedpassword'
    }
    
    # Mock adding the user to the session
    user = User(**user_data)
    mock_session_factory.return_value.add.return_value = None  # Simulate commit
    mock_session_factory.return_value.commit.return_value = None
    mock_session_factory.return_value.refresh.return_value = user
    
    result = user_repository.add(user_data['user_id'], user_data['username'], user_data['password'])
    assert "Added Successfully!" in result
    assert result['Added Successfully!'].username == user_data['username']

def test_get_by_id(user_repository, mock_session_factory):
    # Simulate user retrieval
    user = User(user_id=1, username='testuser', password='hashedpassword', created_at=datetime.now(datetime.timezone.utc), updated_at=datetime.now(datetime.timezone.utc))
    mock_session_factory.return_value.query.return_value.filter.return_value.first.return_value = user
    
    result = user_repository.get_by_id(1)
    assert result.username == 'testuser'

def test_update_user(user_repository, mock_session_factory):
    # Simulate user update
    user = User(user_id=1, username='testuser', password='hashedpassword', created_at=datetime.now(datetime.timezone.utc), updated_at=datetime.now(datetime.timezone.utc))
    mock_session_factory.return_value.query.return_value.filter.return_value.first.return_value = user
    user_repository.update_user(1, username='newusername', password='newpassword')
    
    assert user.username == 'newusername'

def test_delete_user(user_repository, mock_session_factory):
    # Simulate user deletion
    user = User(user_id=1, username='testuser', password='hashedpassword', created_at=datetime.now(datetime.timezone.utc), updated_at=datetime.now(datetime.timezone.utc))
    mock_session_factory.return_value.query.return_value.filter.return_value.first.return_value = user
    
    user_repository.delete_by_id(1)
    mock_session_factory.return_value.delete.assert_called_once_with(user)
