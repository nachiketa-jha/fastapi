import pytest
from services.password_rules import MinLengthRule, MaxLengthRule, UpperCaseRule, LowerCaseRule, NumberRule, SpecialCharacterRule, PasswordRuleEngine


# Test MinLengthRule
def test_min_length_rule_valid():
    rule = MinLengthRule(8)
    assert rule.is_valid("validpass")

def test_min_length_rule_invalid():
    rule = MinLengthRule(8)
    assert not rule.is_valid("short")


# Test MaxLengthRule
def test_max_length_rule_valid():
    rule = MaxLengthRule(20)
    assert rule.is_valid("validpass")

def test_max_length_rule_invalid():
    rule = MaxLengthRule(10)
    assert not rule.is_valid("thispasswordiswaytoolong")


# Test UpperCaseRule
def test_upper_case_rule_valid():
    rule = UpperCaseRule()
    assert rule.is_valid("ValidPass")

def test_upper_case_rule_invalid():
    rule = UpperCaseRule()
    assert not rule.is_valid("validpass")


# Test LowerCaseRule
def test_lower_case_rule_valid():
    rule = LowerCaseRule()
    assert rule.is_valid("ValidPass")

def test_lower_case_rule_invalid():
    rule = LowerCaseRule()
    assert not rule.is_valid("VALIDPASS")


# Test NumberRule
def test_number_rule_valid():
    rule = NumberRule()
    assert rule.is_valid("Password1")

def test_number_rule_invalid():
    rule = NumberRule()
    assert not rule.is_valid("Password")


# Test SpecialCharacterRule
def test_special_character_rule_valid():
    rule = SpecialCharacterRule()
    assert rule.is_valid("Password@123")

def test_special_character_rule_invalid():
    rule = SpecialCharacterRule()
    assert not rule.is_valid("Password123")


# Test PasswordRuleEngine
def test_password_rule_engine_valid():
    rules = [
        MinLengthRule(8),
        MaxLengthRule(20),
        UpperCaseRule(),
        LowerCaseRule(),
        NumberRule(),
        SpecialCharacterRule()
    ]
    engine = PasswordRuleEngine(rules)
    assert engine.is_valid("ValidPass123@") == True

def test_password_rule_engine_invalid():
    rules = [
        MinLengthRule(8),
        MaxLengthRule(12),
        UpperCaseRule(),
        LowerCaseRule(),
        NumberRule(),
        SpecialCharacterRule()
    ]
    engine = PasswordRuleEngine(rules)
    result = engine.is_valid("invalid")
    assert result == {"error": "Password failed these rules: MinLengthRule, UpperCaseRule, NumberRule, SpecialCharacterRule"}