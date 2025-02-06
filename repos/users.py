from contextlib import AbstractContextManager
import datetime
from typing import Callable, Iterator, Optional, Generator

from bcrypt import hashpw, gensalt
import re

from sqlalchemy.orm import Session

from schemas.user import User

from entities.users import GetUserResponse,CreateUserResponse,UpdateUserResponse, LoginUserResponse

class UserRepository:

    def __init__(self, session_factory: Generator[Session, None, None]) -> None:
        self.session_factory = session_factory

    def get_all(self): 
        with self.session_factory() as session:
            users = session.query(User).all()
            return [GetUserResponse.from_orm(user) for user in users]

    def get_by_id(self, user_id: int): 
        with self.session_factory() as session:
            user = session.query(User).filter(User.user_id == user_id).first()
            if not user:
                raise UserNotFoundError(user_id)
            return GetUserResponse.from_orm(user)
        
    def user_login(self,user_id):
        with self.session_factory() as session:
            user = session.query(User).filter(User.user_id == user_id).first()
            if not user:
                raise UserNotFoundError(user_id)
            return LoginUserResponse.from_orm(user) 

    def add(self, user_id:int ,uname:str,password:str) -> User: 
        with self.session_factory() as session:
            created_at = datetime.datetime.now()
            user = User(user_id=user_id, uname=uname, password=password, created_at=created_at, updated_at=None)
            session.add(user)
            session.commit()
            session.refresh(user)
            print("user added successfully")
            return CreateUserResponse.from_orm(user)

    def delete_by_id(self, user_id: int) -> None:
        with self.session_factory() as session:
            entity: User = session.query(User).filter(User.user_id == user_id).first()
            if not entity:
                raise UserNotFoundError(user_id)
            session.delete(entity)
            session.commit() 
            print("deleted")
 
    def update_user(self, user_id, uname:Optional[str]=None, password:Optional[str]=None):   # update 1
        with self.session_factory() as session:
            user = session.query(User).filter(User.user_id == user_id).first()
            if user is None:
                raise UserNotFoundError(user_id)
            updated_at = datetime.datetime.now()
            if uname is not None:
                user.uname = uname
            if password is not None:
                user.password = password
            user.updated_at = updated_at
            session.commit()
            session.refresh(user)
            print("Updated")
            return UpdateUserResponse.from_orm(user)


class user_NotFoundError(Exception):

    entity_name: str

    def __init__(self, entity_id):
        super().__init__(f"{self.entity_name} not found, id: {entity_id}")


class UserNotFoundError(user_NotFoundError):

    entity_name: str = "User"