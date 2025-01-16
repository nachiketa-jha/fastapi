from typing import Iterator, Optional
from repos.users import UserRepository
from entities.users import User


class UserService:

    def __init__(self, user_repository: UserRepository) -> None:
        self._repository: UserRepository = user_repository

    def get_users(self):
        return self._repository.get_all()

    def get_user_by_id(self, user_id: int) -> User: 
        return self._repository.get_by_id(user_id)

    def create_user(self,user_id,username,password):
        return self._repository.add(user_id,username,password)

    def delete_user_by_id(self, user_id: int) -> None:
        return self._repository.delete_by_id(user_id)
    
    def update_userRepo(self, user_id, old_password, username: Optional[str], new_password: Optional[str]):
        return self._repository.update_user(user_id, username,old_password, new_password)