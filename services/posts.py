from typing import Iterator
from repos.posts import PostRepository
from schemas.posts import Post


class PostService:

    def __init__(self, post_repository: PostRepository) -> None:
        self._repository: PostRepository = post_repository

    def get_post(self, user_id:int):
        return self._repository.get_by_id(user_id)
    
    def get_all_posts(self) -> Iterator[Post]:
        return self._repository.get_all_posts_repo()
    
    def add_post(self,post_id:str,post_text: str,user_id: int) -> Post:
        return self._repository.add_post_repo(post_id,post_text,user_id)
    
    def update_post(self,post_id, post_text, user_id):
        return self._repository.updatepost(post_id,post_text,user_id)
    
    def delete_post_service(self,post_id):
        return self._repository.delete_post_repo(post_id)
    
    def delete_post_by_creatorOrAdmin(self,user_id,post_id):
        return self._repository.delete_post_by_creator_or_admin(user_id,post_id)