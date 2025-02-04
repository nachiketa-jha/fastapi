from bcrypt import hashpw, gensalt, checkpw
import bcrypt

class PasswordEncrypt:

    def encrypt(self,password):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hashed_password

    def verify(self,current_password, db_password):
        return bcrypt.checkpw(current_password.encode('utf-8'), db_password.encode('utf-8'))

class PasswordRules:
    def is_valid(self,password):
        pass

class MinLengthRule(PasswordRules):
    def __init__(self,min_length: int):
        self.min_length = min_length

    def is_valid(self, password: str):
        return len(password) >= self.min_length

class MaxLengthRule(PasswordRules):
    def __init__(self,max_length: int):
        self.max_length = max_length

    def is_valid(self, password: str):
        return len(password) <= self.max_length

class UpperCaseRule(PasswordRules):
    def is_valid(self, password: str):
        return any(char.isupper() for char in password)

class LowerCaseRule(PasswordRules):
    def is_valid(self, password: str):
        return any(char.islower() for char in password)

class NumberRule(PasswordRules):
    def is_valid(self, password: str):
        return any(char.isdigit() for char in password)

class SpecialCharacterRule(PasswordRules):
    def __init__(self, special_chars="!@#$%^&*()"):
        self.special_chars = special_chars

    def is_valid(self, password: str):
        return any(char in self.special_chars for char in password)

class PasswordRuleEngine:
    def __init__(self,rules):
        self.rules = rules

    def is_valid(self,password):
        errors = []
        for rule in self.rules:
            if not rule.is_valid(password):
                errors.append(str(rule.__class__.__name__))
        if errors:
            return {"error": f"Password failed these rules: {', '.join(errors)}"}
        return True 