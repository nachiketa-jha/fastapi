from typing import Iterator, Optional

import bcrypt
from repos.users import UserRepository
from schemas.user import User
from fastapi import HTTPException
from bcrypt import hashpw, gensalt, checkpw

from services.password_rules import PasswordRuleEngine, PasswordEncrypt, PasswordRules, MaxLengthRule, MinLengthRule, UpperCaseRule, LowerCaseRule, NumberRule, SpecialCharacterRule

class UserService:

    def __init__(self, user_repository: UserRepository) -> None:
        self._repository: UserRepository = user_repository
        rules = [
            MinLengthRule(8),
            MaxLengthRule(26),
            UpperCaseRule(),
            LowerCaseRule(),
            NumberRule(),
            SpecialCharacterRule()
        ]
        self.password_rule_engine = PasswordRuleEngine(rules)

        self.password_encrypt = PasswordEncrypt()

    def get_users(self): 
        return self._repository.get_all()

    def get_user_by_id(self, user_id: int) -> User:  
        return self._repository.get_by_id(user_id)

    def create_user(self, user_id: int, uname: str, password: str): 
        password_validation = self.password_rule_engine.is_valid(password)
        if isinstance(password_validation, dict): 
            return password_validation
        hashed_password = self.password_encrypt.encrypt(password)
        return self._repository.add(user_id, uname, hashed_password)
    
    def update_user_service(self, user_id: str, uname: Optional[str], new_password: Optional[str]): 
        if new_password:
            password_validation = self.password_rule_engine.is_valid(new_password)
            if isinstance(password_validation, dict): 
                return password_validation
            new_password = self.password_encrypt.encrypt(new_password)
        return self._repository.update_user(user_id, uname, new_password)
    
    def delete_user_by_id(self,user_id):
        return self._repository.delete_by_id(user_id)

    def login_user(self, user_id: int, password: str) -> dict:
        user = self._repository.user_login(user_id)
        
        if not user:
            return {"Error": "User not found"}

        if not self.password_encrypt.verify(password,user.password):
            raise HTTPException(status_code=401)

        return {"Success": "Login successful", "user": user}