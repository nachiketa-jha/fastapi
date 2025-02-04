from contextlib import AbstractContextManager
import datetime
from typing import Callable, Iterator, Generator

from sqlalchemy.orm import Session

from schemas.roles import Role

from entities.roles import CreateRoleResponse,UpdateRoleResponse,GetRoleResponse

class RoleRepository:
    def __init__(self, session_factory: Generator[Session, None, None]) -> None:
        self.session_factory = session_factory

    def get_all(self):
        with self.session_factory() as session:
            roles = session.query(Role).all()
            return [GetRoleResponse.from_orm(roles) for roles in roles]
        
    def add_role(self, role_id:int, role_name:str, is_admin:bool) -> Role:
        with self.session_factory() as session:
            created_at = datetime.datetime.now()
            role = Role(role_id=role_id, role_name=role_name, is_admin=is_admin, created_at=created_at)
            session.add(role)
            session.commit()
            session.refresh(role)
            print("role added successfully")
            return CreateRoleResponse.from_orm(role)
        
    def update_role_roleRepo(self,role_id,role_name,is_admin):
        with self.session_factory() as session:
            role = session.query(Role).filter(Role.role_id == role_id).first()
            if role is None:
                raise RoleNotFoundError(role_id)
            updated_at = datetime.datetime.now()
            if role_name is not None:
                role.role_name = role_name
            if is_admin is not None:
                role.is_admin = is_admin
            role.updated_at = updated_at
            session.commit()
            session.refresh(role)
            print("Updated")
            return UpdateRoleResponse.from_orm(role)

    def delete_role_by_role_id(self, role_id) -> None:
        with self.session_factory() as session:
            entity: Role = session.query(Role).filter(Role.role_id == role_id).first()
            if not entity:
                raise RoleNotFoundError(role_id)
            session.delete(entity)
            session.commit()

    def get_role_fromRepo_by_id(self,role_id):
        with self.session_factory() as session:
            role = session.query(Role).filter(Role.role_id == role_id).first()
            if role is None:
                raise RoleNotFoundError(role_id)
            return GetRoleResponse.from_orm(role)

class role_NotFoundError(Exception):

    entity_name: str

    def __init__(self, entity_id):
        super().__init__(f"{self.entity_name} not found, id: {entity_id}")


class RoleNotFoundError(role_NotFoundError):

    entity_name: str = "Role"