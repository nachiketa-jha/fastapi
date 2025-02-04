
from contextlib import contextmanager
from unittest import mock
from sqlalchemy import create_engine
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from repos.posts import PostNotFoundError, PostRepository
from schemas.posts import Post
from application import app
from services.posts import PostService

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
def post_repo():
    Post.metadata.drop_all(bind=engine)
    Post.metadata.create_all(bind=engine)
    return PostRepository(session_factory=get_test_session)

@pytest.fixture
def sample_post(post_repo):
    if not post_repo.get_all_posts_repo():  # Add user only if table is empty
        post_repo.add_post_repo(post_id=0, post_text="testPostText", user_id=0)
    return post_repo.get_by_id(0)

@pytest.fixture
def client():
    yield TestClient(app)


def test_get_all(post_repo, sample_post):
    post = post_repo.get_all_posts_repo()
    assert len(post) == 1
    assert post[0].post_text == "testPostText"

def test_get_by_id(post_repo, sample_post):
    post = post_repo.get_by_id(0)
    assert len(post) != 0

    with pytest.raises(PostNotFoundError):
        post_repo.get_by_id(999)

def test_add_post(post_repo):
    response = post_repo.add_post_repo(post_id=2, post_text="testPostText2", user_id=2)
    assert response.post_text == "testPostText2"
    assert response.post_id == 2
    assert response.user_id == 2

def test_delete_by_id(post_repo, sample_post):
    with mock.patch.object(post_repo, 'delete_post_repo') as mock_delete_post:
        post_repo.delete_post_repo(0)
        mock_delete_post.assert_called_once()
    with pytest.raises(PostNotFoundError):
        post_repo.delete_post_repo(999)


def test_update_post(post_repo, sample_post):
    response = post_repo.updatepost(post_id=0, post_text="updatedtestPostText", user_id=0)
    assert response.post_text == "updatedtestPostText"
    with pytest.raises(PostNotFoundError):
        post_repo.updatepost(999,"notExisting",999)

# def test_delete_by_creator_or_admin(post_repo,sample_post):
#     with mock.patch.object(post_repo, 'delete_post_by_creator_or_admin') as mock_delete_post:
#         post_repo.delete_post_by_creator_or_admin(1,1)
#         mock_delete_post.assert_called_once()

def test_get_post():
    mock_repo = mock.Mock(spec=PostRepository)
    mock_repo.get_by_id.return_value = {"post_id":1,"post_text":"postTextOne","user_id":1}
    post_service = PostService(mock_repo)

    posts = post_service.get_post(1)
    assert posts["post_id"] == 1
    assert posts["user_id"] == 1
    assert posts["post_text"] == "postTextOne"

def test_get_all_posts():
    mock_repo = mock.Mock(spec=PostRepository)
    mock_repo.get_all_posts_repo.return_value = [{"post_id":1,"post_text":"postTextOne","user_id":1}]
    post_service = PostService(mock_repo)

    posts = post_service.get_all_posts()
    assert len(posts) == 1
    assert posts[0]["post_id"] == 1
    assert posts[0]["user_id"] == 1

def test_update_post_service():
    mock_repo = mock.Mock(spec=PostRepository)
    mock_repo.updatepost.return_value = {"post_id": 1, "post_text": "updatedPost", "user_id": 1,"created_at":"now","updated_at":"now"}
    
    post_service = PostService(mock_repo)
    
    result = post_service.update_post(1, "updatedPost", 1)
    
    assert result["user_id"] == 1
    assert result["post_text"] == "updatedPost"
    assert result["post_id"] == 1
    mock_repo.updatepost.assert_called_once()

def test_delete_post_by_id():
    mock_repo = mock.Mock(spec=PostRepository)
    
    post_service = PostService(mock_repo)
    
    post_service.delete_post_service(1)
    
    mock_repo.delete_post_repo.assert_called_once_with(1)
