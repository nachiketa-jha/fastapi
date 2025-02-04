from typing import Optional
from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide

from services.roles import RoleService

from container import Container


router = APIRouter()

# for roles

## view all
@router.get("/role")
@inject
def get_all_roles(
    Role_service: RoleService = Depends(Provide[Container.role_service])
):
    return Role_service.get_all_roleService()

## view 1
@router.get("/role/{role_id}")
@inject
def get_role_by_id(
    role_id:int,
    Role_service: RoleService = Depends(Provide[Container.role_service])
):
    return Role_service.get_role(role_id)

## add 1
@router.post("/role")
@inject
def create_Role(
    role_id: int,
    role_name: str,
    is_admin: bool,
    Role_service: RoleService = Depends(Provide[Container.role_service])
):
    return Role_service.add_role_service(role_id,role_name,is_admin)


## update 1
@router.put("/role")
@inject
def update_Role(
    role_id: int,
    role_name: Optional[str],
    is_admin: Optional[bool],
    Role_service: RoleService = Depends(Provide[Container.role_service])
):
    return Role_service.update_role_roleService(role_id,role_name,is_admin)

## delete 1
@router.delete("/Role")
@inject
def delete_Role(
    role_id: int,
    Role_service: RoleService = Depends(Provide[Container.role_service])
):
    return Role_service.delete_role_by_id(role_id)