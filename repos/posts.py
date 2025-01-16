from contextlib import AbstractContextManager
import datetime
from http.client import HTTPException
from operator import and_
from typing import Callable, Iterator

from sqlalchemy.orm import Session

from entities.posts import Post
from entities.roles import Role
from entities.user_roles import UserRole
from schemas.posts import PostResponse

class PostRepository:

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def get_all_posts_repo(self) -> Iterator[Post]:
        with self.session_factory() as session:
            posts= session.query(Post).all()
            return [PostResponse.model_validate(post) for post in posts]

    def get_by_id(self,user_id):
        with self.session_factory() as session:
            posts = session.query(Post).filter(Post.user_id == user_id).all()
            if not posts:
                raise PostNotFoundError(user_id)
            return PostResponse.model_validate(user_id)
        
    def add_post_repo(self,post_id,post_text,user_id):
        with self.session_factory() as session:
            created_at = datetime.datetime.now()
            post = Post(post_id=post_id, post_text=post_text, user_id=user_id,created_at=created_at,updated_at=None)
            session.add(post)
            session.commit()
            session.refresh(post)
            return {"Added successfully!": PostResponse.model_validate(post)}
            
        
    def updatepost(self, post_id:int, postText:str, userID:int)-> None:
        with self.session_factory() as session:
            post = session.query(Post).filter(Post.post_id == post_id).first()
            if post is None:
                raise ValueError(f"User with id {post_id} not found")
            updated_at = datetime.datetime.now()
            if postText is not None:
                post.postText = postText
            if userID is not None:
                post.userID = userID
            post.updated_at = updated_at
            session.commit()
            session.refresh(post)
            return {"Updated Successfully!", PostResponse.model_validate(post)}
        
    # def delete_post_repo(self,post_id) -> None:
    #     with self.session_factory() as session:
    #         entity : Post = session.query(Post).filter(Post.post_id == post_id).first()
    #         if not entity:
    #             raise PostNotFoundError(post_id)
    #         session.delete(entity)
    #         session.commit()
    #         return f"Deleted Successfully!"

    def delete_post_by_creator_or_admin(self,user_id,post_id):
        with self.session_factory() as session:
            is_admin = (
                session.query(Role.is_admin).join(UserRole,UserRole.role_id == Role.role_id)
                .filter(and_(UserRole.user_id==user_id,Role.is_admin==True)).first()
            )
            is_creator = Post.user_id == user_id
            if not(is_admin or is_creator):
                raise HTTPException(
                    status_code=403,
                    detail="User is not authorized to delete this post"
                )
            entity : Post = session.query(Post).filter(Post.post_id == post_id).first()
            session.delete(entity)
            session.commit()
            return f"Deleted Successfully!"

class post_NotFoundError(Exception):

    entity_name: str

    def __init__(self, entity_id):
        super().__init__(f"{self.entity_name} with id: {entity_id} not found.")
        
class PostNotFoundError(post_NotFoundError):

    entity_name: str = "Post"