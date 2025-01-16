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

    def get_by_id(self, user_id: int) -> UserResponse:  
        with self.session_factory() as session:
            user = session.query(User).filter(User.user_id == user_id).first()
            if not user:
                raise UserNotFoundError(user_id)
            return UserResponse.model_validate(user)

    def add(self, user_id:int ,username:str,password:str) -> User: 
        with self.session_factory() as session:
            created_at = datetime.datetime.now().replace(microsecond=0) 
            if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", password):
                return f"Error! Password must have at least one uppercase letter, one lowercase letter, one digit, one special character, and be at least 8 characters long."
            hashed_password=hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')
            created_at = datetime.datetime.now()
            user = User(user_id=user_id, username=username, password=hashed_password, created_at=created_at, updated_at=None)
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
 
    def update_user(self, user_id, old_password, username:Optional[str]=None, new_password:Optional[str]=None):   # update 1
        with self.session_factory() as session:
            user = session.query(User).filter(User.user_id == user_id).first()
            if user is None:
                raise ValueError(f"User witsh id {user_id} not found")
            updated_at = datetime.datetime.now()
            if username is not None:
                user.username = username
            if new_password is not None:
                if old_password is None or not checkpw(old_password.encode('utf-8'), user.password.encode('utf-8')):
                    raise HTTPException (status_code=401, detail=f"Unauthorized User! Password entered is incorrect")
            
                if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", new_password):
                    return f"Error! Password must have at least one uppercase letter, one lowercase letter, one digit, one special character, and be at least 8 characters long."
                user.password=hashpw(new_password.encode('utf-8'), gensalt()).decode('utf-8')
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