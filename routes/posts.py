from typing import Optional
from fastapi import APIRouter, Depends, Response, status
from dependency_injector.wiring import inject, Provide

from container import Container

from services.posts import PostService

router = APIRouter()

# for posts

## view all
@router.get("/posts")
@inject
def get_post_list(
        post_service: PostService = Depends(Provide[Container.post_service]),
):
    return post_service.get_all_posts()

## view all by one user
@router.get("/posts/{user_id}")
@inject
def get_post(user_id: int,
             post_service: PostService = Depends(Provide[Container.post_service])):
    return post_service.get_post(user_id)
    
## add 1
@router.post("/posts/{user_id}")
@inject
def add_post(post_id: int,post_text: str,user_id: int,
             post_service: PostService = Depends(Provide[Container.post_service])):
    return post_service.add_post(post_id,post_text,user_id)

## update 1
@router.put("/posts")
@inject
def update_post(post_id: int,
                post_text: Optional[str],
                user_id: Optional[int],
             post_service: PostService = Depends(Provide[Container.post_service])):
    return post_service.update_post(post_id, post_text, user_id)

## delete 1 by post_id
@router.delete("/posts")
@inject
def delete_post(
    post_id:int,
    post_service: PostService = Depends(Provide[Container.post_service])):
    return post_service.delete_post_service(post_id)

## post can be deleted by admin or creator
@router.delete("/posts/{user_id}")
@inject
def delete_post_by_id(
    user_id: int,
    post_id:int,
    post_service: PostService = Depends(Provide[Container.post_service])
):
    return post_service.delete_post_by_creatorOrAdmin(user_id,post_id)