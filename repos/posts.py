from contextlib import AbstractContextManager
import datetime
from http.client import HTTPException
from operator import and_
from typing import Callable, Iterator, Generator

from sqlalchemy.orm import Session

from schemas.posts import Post
from schemas.roles import Role
from schemas.user_roles import UserRole

from entities.posts import CreatePostResponse,UpdatePostResponse,GetPostByIDResponse,GetPostResponse

class PostRepository:

    def __init__(self, session_factory: Generator[Session, None, None]) -> None:
        self.session_factory = session_factory

    def get_all_posts_repo(self) -> Iterator[Post]:
        with self.session_factory() as session:
            posts = session.query(Post).all()
            return [GetPostResponse.from_orm(posts) for posts in posts]

    def get_by_id(self,user_id):  # getting all posts associated to a given user_id
        with self.session_factory() as session:
            posts = session.query(Post).filter(Post.user_id == user_id).all()
            if not posts:
                raise PostNotFoundError(user_id)
            return [GetPostByIDResponse.from_orm(posts) for posts in posts]
        
    def add_post_repo(self,post_id,post_text,user_id):
        with self.session_factory() as session:
            created_at = datetime.datetime.now()
            post = Post(post_id=post_id, post_text=post_text, user_id=user_id,created_at=created_at)
            session.add(post)
            session.commit()
            session.refresh(post)
            print("post added successfully")
            return CreatePostResponse.from_orm(post)
        
    def updatepost(self, post_id:int, post_text:str, user_id:int)-> None:
        with self.session_factory() as session:
            post = session.query(Post).filter(Post.post_id == post_id).first()
            if post is None:
                raise PostNotFoundError(post_id)
            updated_at = datetime.datetime.now()
            if post_text is not None:
                post.post_text = post_text
            if user_id is not None:
                post.user_id = user_id
            post.updated_at = updated_at
            session.commit()
            session.refresh(post)
            print("Updated")
            return UpdatePostResponse.from_orm(post)
        
    def delete_post_repo(self,post_id) -> None:
        with self.session_factory() as session:
            entity : Post = session.query(Post).filter(Post.post_id == post_id).first()
            if not entity:
                raise PostNotFoundError(post_id)
            session.delete(entity)
            session.commit()
            return print("deleted")

    def delete_post_by_creator_or_admin(self,user_id,post_id):
        with self.session_factory() as session:
            is_admin = (
                session.query(Role.is_admin).join(UserRole,UserRole.role_id == Role.role_id)
                .filter(and_(UserRole.user_id==user_id,Role.is_admin==True)).first()
            )
            is_creator = post_id == user_id
            if not(is_admin or is_creator):
                raise HTTPException(
                    status_code=403,
                    detail="User is not authorized to delete this post"
                )
            entity : Post = session.query(Post).filter(Post.post_id == post_id).first()
            session.delete(entity)
            session.commit()
            print("Deleted")

class post_NotFoundError(Exception):

    entity_name: str

    def __init__(self, entity_id):
        super().__init__(f"{self.entity_name} with id: {entity_id} not found.")
        
class PostNotFoundError(post_NotFoundError):

    entity_name: str = "Post"