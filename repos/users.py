from contextlib import AbstractContextManager
import datetime
from fastapi import HTTPException
from typing import Callable, Iterator, Optional
from bcrypt import hashpw, gensalt, checkpw
from schemas.user import UserResponse
from sqlalchemy.orm import Session
import re
from entities.users import User

class UserRepository:

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def get_all(self):  
        with self.session_factory() as session:
            users = session.query(User).all()
            return [UserResponse.model_validate(user) for user in users]

    def get_by_id(self, user_id: int) -> User:  
        with self.session_factory() as session:
            user = session.query(User).filter(User.user_id == user_id).first()
            if not user:
                raise UserNotFoundError(user_id)
            return UserResponse.model_validate(user)

    def add(self, user_id:int ,username:str,password:str) -> User: 
        with self.session_factory() as session:
            user = User(user_id=user_id, username=username, password=password, updated_at=None)
            session.add(user)
            session.commit()
            session.refresh(user)
            return {"Added Successfully!": UserResponse.model_validate(user)}

    def delete_by_id(self, user_id: int) -> None: 
        with self.session_factory() as session:
            entity: User = session.query(User).filter(User.user_id == user_id).first()
            if not entity:
                raise UserNotFoundError(user_id)
            session.delete(entity)
            session.commit() 
            return print("Deleted Successfully!")
 
    def update_user(self, user_id, username:Optional[str]=None, hashed_password:Optional[str]=None): 
        with self.session_factory() as session:
            user = session.query(User).filter(User.user_id == user_id).first()
            if user is None:
                raise ValueError(f"User witsh id {user_id} not found")
            updated_at = datetime.datetime.now()
            if username is not None:
                user.username = username
            if hashed_password is not None:
                user.password=hashed_password
                
            user.updated_at = updated_at
            session.commit()
            session.refresh(user)
            return {"Updated Successfully!": UserResponse.model_validate(user)}


class user_NotFoundError(Exception):

    entity_name: str

    def __init__(self, entity_id):
        super().__init__(f"{self.entity_name} not found, id: {entity_id}")


class UserNotFoundError(user_NotFoundError):

    entity_name: str = "User"