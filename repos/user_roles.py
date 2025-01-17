from contextlib import AbstractContextManager
import datetime
from typing import Callable, Iterator

from sqlalchemy.orm import Session

from entities.user_roles import UserRole
from schemas.user_roles import UserRoleResponse

class UserRoleRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def get_all(self) -> Iterator[UserRole]:
        with self.session_factory() as session:
            user_roles= session.query(UserRole).all()
            return [UserRoleResponse.model_validate(user_role) for user_role in user_roles]

    def add_user_role(self, user_role_id:int, user_id:int, role_id:int) -> UserRole:
        with self.session_factory() as session:
            created_at = datetime.datetime.now()
            user_role = UserRole(user_role_id=user_role_id, user_id=user_id, role_id=role_id, created_at=created_at)
            session.add(user_role)
            session.commit()
            session.refresh(user_role)
            return {"Added successfully": UserRoleResponse.model_validate(user_role)}
        
    def delete_user_role(self, user_id: int) -> None:
        with self.session_factory() as session:
            entity: UserRole = session.query(UserRole).filter(UserRole.user_id == user_id).first()
            if not entity:
                raise UserNotFoundError(user_id)
            session.delete(entity)
            session.commit()
            return f"Deleted Successfully!"

    def update_user_role(self,user_role_id,user_id,role_id):
        with self.session_factory() as session:
            user_role = session.query(UserRole).filter(UserRole.user_role_id == user_role_id).first()
            if user_role is None:
                raise ValueError(f"User role with id {user_role_id} not found")
            updated_at = datetime.datetime.now()
            if user_role_id is not None:
                user_role.user_role_id = user_role_id
            if user_id is not None:
                user_role.user_id = user_id
            if role_id is not None:
                user_role.role_id = role_id
            user_role.updated_at = updated_at
            session.commit()
            session.refresh(user_role)
            return {"Updated Successfully": UserRoleResponse.model_validate(user_role)}
        
    def getUserRole(self,user_role_id):
        with self.session_factory() as session:
            user_role = session.query(UserRole).filter(UserRole.user_role_id == user_role_id).first()
            if not user_role:
                raise userRole_NotFoundError(user_role_id)
            return UserRoleResponse.model_validate(user_role)


class userRole_NotFoundError(Exception):

    entity_name: str

    def __init__(self, entity_id):
        super().__init__(f"{self.entity_name} not found, id: {entity_id}")


class UserRoleNotFoundError(userRole_NotFoundError):

    entity_name: str = "UserRole"