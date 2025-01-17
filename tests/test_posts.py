from contextlib import contextmanager
from unittest import mock
from sqlalchemy import create_engine
import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from ..schemas.posts import PostResponse
from ..repos.posts import PostRepository, PostNotFoundError
from ..entities.posts import Post
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
def post_repo():
    Post.metadata.drop_all(bind=engine)
    Post.metadata.create_all(bind=engine)
    return PostRepository(session_factory=get_test_session)

@pytest.fixture
def sample_post(post_repo):
    if not post_repo.get_all_posts_repo():
        post_repo.add_post_repo(post_id=1, post_text="testpost", user_id=4)
    return post_repo.get_by_id(1)

@pytest.fixture
def client():
    yield TestClient(app)


def test_get_all_posts(post_repo, sample_post):
    # Ensure that there is at least one post
    posts = post_repo.get_all_posts_repo()
    assert len(posts) == 1
    assert posts[0].post_text == "testpost"

def test_get_by_id(post_repo, sample_post):
    # Test for an existing post
    post = post_repo.get_by_id(1)
    assert post.post_text == "testpost"

    # Test for a non-existing post, which should raise a PostNotFoundError
    with pytest.raises(PostNotFoundError):
        post_repo.get_by_id(999)

def test_add_post(post_repo):
    # Add a new post
    response = post_repo.add_post_repo(post_id=2, post_text="newpost", user_id=3)
    assert response["Added Successfully"].post_text == "newpost"

    # Check if the new post is added correctly
    new_post = post_repo.get_by_id(2)
    assert new_post.post_text == "newpost"

def test_update_post(post_repo, sample_post):
    # Update an existing post
    response = post_repo.updatepost(1, postText="updatedpost", userID=4)
    assert response["Updated Successfully!"].post_text == "updatedpost"

    # Check if the post was updated correctly
    updated_post = post_repo.get_by_id(1)
    assert updated_post.post_text == "updatedpost"

    # Test trying to update a non-existing post
    with pytest.raises(ValueError):
        post_repo.updatepost(999, postText="nonexistent", userID=3)

def test_delete_post_by_creator_or_admin(post_repo, sample_post):
    # Delete the post by creator (user_id = 4)
    response = post_repo.delete_post_by_creator_or_admin(user_id=4, post_id=1)
    assert response == "Deleted Successfully!"
    
    # Verify the post is deleted
    with pytest.raises(PostNotFoundError):
        post_repo.get_by_id(1)

    # Add the post again for further tests
    post_repo.add_post_repo(post_id=1, post_text="testpost", user_id=4)

    # Test for an admin user (simulate admin role)
    with mock.patch("sqlalchemy.orm.Session") as mock_session:
        mock_session.query.return_value.filter.return_value.first.return_value = True  # Simulating an admin
        response = post_repo.delete_post_by_creator_or_admin(user_id=1, post_id=1)  # Admin user_id = 1
        assert response == "Deleted Successfully!"

    # Test if a user without the right role tries to delete the post
    with pytest.raises(HTTPException):
        post_repo.delete_post_by_creator_or_admin(user_id=2, post_id=1)  # User with no permission
