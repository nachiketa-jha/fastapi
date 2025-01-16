import datetime
from typing import Iterator
from repos.user_roles import UserRoleRepository
from entities.user_roles import UserRole


class UserRoleService:
    def __init__(self, user_role_repository: UserRoleRepository) -> None:
        self._repository: UserRoleRepository = user_role_repository
    
    def get_all(self) -> Iterator[UserRole]:
        return self._repository.get_all()
    
    def create_user_role(self, user_role_id:int,user_id:int, role_id:int) -> UserRole:
        return self._repository.add_user_role(user_role_id, user_id, role_id)
    
    def delete_user_role(self, user_id:int) -> None:
        return self._repository.delete_user_role(user_id)
    
    def get_userRole(self, user_role_id:int):
        return self._repository.getUserRole(user_role_id)
    
    def update_user_role(self, user_role_id, user_id, role_id) -> None:
        return self._repository.update_user_role(user_role_id,user_id,role_id)