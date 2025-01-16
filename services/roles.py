from typing import Iterator, Optional
from repos.roles import RoleRepository
from entities.roles import Role


class RoleService:
    def __init__(self, role_repository: RoleRepository) -> None:
        self._repository: RoleRepository = role_repository
    
    def get_all_roleService(self) -> Iterator[Role]:
        return self._repository.get_all()
    
    def add_role_roleRepo(self, role_id:int, role_name:str, is_admin:bool) -> Role:
        return self._repository.add_role(role_id,role_name, is_admin)
    
    def get_role(self,role_id:int):
        return self._repository.get_role_fromRepo_by_id(role_id)
    
    def update_role_roleService(self,role_id:Optional[int],role_name:Optional[str],is_admin:Optional[bool]):
        return self._repository.update_role_roleRepo(role_id,role_name,is_admin)
    
    def delete_role_by_id(self, role_id: int) -> None:
        return self._repository.delete_role_by_role_id(role_id)