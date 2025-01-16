from typing import Optional
from fastapi import APIRouter, Depends
from services.user_roles import UserRoleService
from dependency_injector.wiring import inject, Provide

from container import Container

router = APIRouter()


@router.get("/userRole")
@inject
def get_all_user_roles(
    userRole_service: UserRoleService = Depends(Provide[Container.user_role_service])
):
    return userRole_service.get_all()


@router.post("/userrole")
@inject
def create_userRole(
    user_role_id: int,
    user_id: int,
    role_id: int,
    userRole_service: UserRoleService = Depends(Provide[Container.user_role_service])
):
    return userRole_service.create_user_role(user_role_id, user_id, role_id)

@router.put("/userrole")
@inject
def update_userRole(user_role_id: int,
                user_id: Optional[int],
                role_id: Optional[int],
             userRole_service: UserRoleService = Depends(Provide[Container.user_role_service])):
    return userRole_service.update_user_role(user_role_id,user_id,role_id)


@router.delete("/userrole")
@inject
def delete_userRole(
    user_id: int,
    userRole_service: UserRoleService = Depends(Provide[Container.user_role_service])
):
    return userRole_service.delete_user_role(user_id)


@router.get("/userrole/{user_role_id}")
@inject
def get_userRole_by_id(
    user_role_id: int,
    userRole_service: UserRoleService = Depends(Provide[Container.user_role_service])
    ):
    return userRole_service.get_userRole(user_role_id)