import datetime
from typing import Iterator, Optional
from repos.users import UserRepository
from entities.users import User
from bcrypt import hashpw, gensalt, checkpw
from fastapi import HTTPException
from schemas.user import UserResponse
import database as db

class StrategyPassword:
    def __init__(self):
        pass
    def encrypt(self, password:str):
        return hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')
    def validate(self, old_password: str, current_password: str):
        print("Verifying old password...")
        print(old_password, current_password)
        print(old_password.encode('utf-8'), current_password.encode('utf-8'))
        if old_password is None and not checkpw(old_password.encode('utf-8'), current_password.encode('utf-8')):
            raise HTTPException(status_code=401, detail="Unauthorized: Password entered is incorrect")
        print("Old password verified")
        return "Authorized"


class Rule:
    def is_valid(self, password):
        pass

class MinLengthRule(Rule):
    def __init__(self, min_length: int):
        self.min_length = min_length
    def is_valid(self, password: str):
        return len(password) >= self.min_length
    
class MaxLengthRule(Rule):
    def __init__(self, max_length: int):
        self.max_length = max_length
    def is_valid(self, password: str):
        return len(password) <= self.max_length

class SpecialCharacter(Rule):
    def __init__(self, special_char:str = "[@$!%*?&]"):
        self.special_char = special_char
    def is_valid(self, password: str):
        return any(char in self.special_char for char in password)

class CapitalRule(Rule):
    def __init__(self, capital_char: str):
        self.capital_char = capital_char
    def is_valid(self, password:str):
        return any(char.isupper() for char in password)
    
class SmallRule(Rule):
    def __init__(self, small_char: str):
        self.small_char = small_char
    def is_valid(self, password:str):
        return any(char.islower() for char in password)
    
class PasswordRuleEngine(Rule):
    def __init__(self, rules):
        self.rules= rules
    
    def is_valid(self, password):
        return all([rule.is_valid(password) for rule in self.rules])

class UserService:
    def __init__(self, user_repository: UserRepository) -> None:
        self._repository: UserRepository = user_repository
        self.password_strategy = StrategyPassword()
        # Define the rules to validate passwords
        self.rules = [
            MinLengthRule(8),
            MaxLengthRule(20),
            SpecialCharacter(),
            CapitalRule(""),
            SmallRule("")
        ]
        self.password_rule_engine = PasswordRuleEngine(self.rules)

    def get_users(self):
        return self._repository.get_all()

    def get_user_by_id(self, user_id: int) -> UserResponse:
        user = self._repository.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return self._repository.get_by_id(user_id)

    def create_user(self, user_id: int, username: str, password: str) -> UserResponse:
        if not self.password_rule_engine.is_valid(password):
            raise HTTPException(status_code=400, detail="Password does not meet the required criteria.")
    
        hashed_password = self.password_strategy.encrypt(password)
        created_at = datetime.datetime.now().replace(microsecond=0)
        
        return self._repository.add(user_id, username, hashed_password, created_at)

    def delete_user_by_id(self, user_id: int) -> None:
        return self._repository.delete_by_id(user_id)
    
    def update_user(self, user_id: int, old_password: str, username: Optional[str], new_password: Optional[str]):
        user = self.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        if new_password:
            if not self.password_strategy.validate(old_password, user.password):
                raise HTTPException(status_code=401, detail="Old password is incorrect")
            if not self.password_rule_engine.is_valid(new_password):
                raise HTTPException(status_code=400, detail="New password does not meet the required criteria")
            hashed_password = self.password_strategy.encrypt(new_password)
            new_password = hashed_password
        
        if username:
            user.username = username
        user.updated_at = datetime.datetime.now()
        return self._repository.update_user(user_id, username)