from typing import Optional
from fastapi import APIRouter, Depends, Response, status
from dependency_injector.wiring import inject, Provide

from container import Container
from services.users import UserService

router = APIRouter()

# For users

## user login
@router.get("/user/login/{user_id}")
@inject
def user_login(
    user_id: int,
    password: str,
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    return user_service.login_user(user_id,password)

## view all
@router.get("/users")
@inject
def get_list(
        user_service: UserService = Depends(Provide[Container.user_service]),
):
    return user_service.get_users()

## view 1
@router.get("/users/{user_id}")
@inject
def get_by_id(
        user_id: int,
        user_service: UserService = Depends(Provide[Container.user_service]),
):
    return user_service.get_user_by_id(user_id)


## add 1
@router.post("/users/{user_id}")
@inject
def add(user_id: int, uname: str, password: str,
        user_service: UserService = Depends(Provide[Container.user_service])
        ):
    return user_service.create_user(user_id, uname, password)

## update 1
@router.put("/users")
@inject
def update_user(
    user_id: int,
    uname: Optional[str]=None,
    new_password: Optional[str]=None,
    user_service: UserService = Depends(Provide[Container.user_service])
):
    return user_service.update_user_service(user_id,uname,new_password)

## delete 1
@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
def remove(
        user_id: int,
        user_service: UserService = Depends(Provide[Container.user_service]),
):
    user_service.delete_user_by_id(user_id)