from typing import Optional
from fastapi import APIRouter, Depends, Response, status
from dependency_injector.wiring import inject, Provide

from container import Container
from repos.users import user_NotFoundError
from services.users import UserService

router = APIRouter()


@router.get("/users")
@inject
def get_list(
        user_service: UserService = Depends(Provide[Container.user_service]),
):
    return user_service.get_users()


@router.get("/users/{user_id}")
@inject
def get_by_id(
        user_id: int,
        user_service: UserService = Depends(Provide[Container.user_service]),
):
    return user_service.get_user_by_id(user_id)



@router.post("/users/{user_id}")
@inject
def add(user_id: int, username: str, password: str,
        user_service: UserService = Depends(Provide[Container.user_service])
        ):
    return user_service.create_user(user_id, username, password)



@router.put("/users")
@inject
def update_user(
    user_id: int,
    old_password: str,
    uname: Optional[str]=None,
    new_password: Optional[str]=None,
    user_service: UserService = Depends(Provide[Container.user_service])
):
    return user_service.update_userRepo(user_id,uname,old_password, new_password)

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
def remove(
        user_id: int,
        user_service: UserService = Depends(Provide[Container.user_service]),
):
    try:
        user_service.delete_user_by_id(user_id)
    except user_NotFoundError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)