from contextlib import AbstractContextManager
import datetime
from typing import Callable, Iterator

from sqlalchemy.orm import Session

from entities.roles import Role
from schemas.roles import RoleResponse

class RoleRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def get_all(self) -> Iterator[Role]:
        with self.session_factory() as session:
            roles= session.query(Role).all()
            return [RoleResponse.model_validate(role) for role in roles]

    def add_role(self, role_id:int, role_name:str, is_admin:bool) -> Role:
        with self.session_factory() as session:
            created_at = datetime.datetime.now()
            role = Role(role_id=role_id, role_name=role_name, is_admin=is_admin, created_at=created_at)
            session.add(role)
            session.commit()
            session.refresh(role)
            return {"Added Successfully!": RoleResponse.model_validate(role)}
        
    def update_role_roleRepo(self,role_id,role_name,is_admin):
        with self.session_factory() as session:
            role = session.query(Role).filter(Role.role_id == role_id).first()
            if role is None:
                raise ValueError(f"User with role id {role_id} not found")
            updated_at = datetime.datetime.now()
            if role_name is not None:
                role.role_name = role_name
            if is_admin is not None:
                role.is_admin = is_admin
            role.updated_at = updated_at
            session.commit()
            session.refresh(role)
            return {"Updated successfully!": RoleResponse.model_validate(role)}
    
    def delete_role_by_role_id(self, role_id) -> None:
        with self.session_factory() as session:
            entity: Role = session.query(Role).filter(Role.role_id == role_id).first()
            if not entity:
                raise RoleNotFoundError(role_id)
            session.delete(entity)
            session.commit()
            return f"Deleted Successfully!"

    def get_role_fromRepo_by_id(self,role_id):
        with self.session_factory() as session:
            role = session.query(Role).filter(Role.role_id == role_id).first()
            if not role:
                raise RoleNotFoundError(role_id)
            return RoleResponse.model_validate(role)

class role_NotFoundError(Exception):

    entity_name: str

    def __init__(self, entity_id):
        super().__init__(f"{self.entity_name} not found, id: {entity_id}")


class RoleNotFoundError(role_NotFoundError):

    entity_name: str = "Role"