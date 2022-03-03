'''
This module contains tests for the auth_register_v1 function
based on the black box testing model

Kais Alzubaidi z5246721


'''

import pytest
from src.error import InputError
from src.auth import auth_login_v1, auth_register_v1
from src.auth import auth_register_v1
from src.other import clear_v1

# ======================== SET 1 ================================
def test_return_type():
    clear_v1()
    return_val = auth_register_v1(
            "k.z123@gmail.com",
            "a1b2c3d4e5",
            "KaIS",
            "AlzuBaidI")
    assert type(return_val) == dict
    assert type(return_val['auth_user_id']) == int


# Checking that the return val is not an empty dict
def test_return_id_one_user():
    clear_v1()
    register_return_val = auth_register_v1(
            "kais.z123@gmail.com",
            "a1b2c3d4e5",
            "KaIS",
            "AlzuBaidI")
        
    login_return_uid = auth_login_v1("kais.z123@gmail.com", "a1b2c3d4e5")

    assert register_return_val == login_return_uid


# Checking that auth_register returns the correct uid
# for one user
def test_return_is_not_empty():
    clear_v1()
    register_return_val_usr1 = auth_register_v1(
            "kais.z123@gmail.com",
            "a1b2c3d4e5",
            "KaIS",
            "AlzuBaidI")
        
    assert register_return_val_usr1 != {}

# Checking that auth_register returns the correct uid
# for multiple users
def test_return_id_multiple_users():
    register_return_val_usr1 = auth_register_v1(
            "k.z1@gmail.com",
            "a1b2c3d4e5",
            "Kais",
            "alzubaidi")

    register_return_val_usr2 = auth_register_v1(
            "k.z2@gmail.com",
            "a1b2c3d4e5",
            "Liam",
            "Conor")

    register_return_val_usr3 = auth_register_v1(
            "k.z3@gmail.com",
            "a1b2c3d4e5",
            "James",
            "Austin")

    register_return_val_usr4 = auth_register_v1(
            "k.z4567@gmail.com",
            "a1b2c3d4e5",
            "Kai",
            "ALZubaidi")

    login_return_val_usr1 = auth_login_v1("k.z1@gmail.com", "a1b2c3d4e5")
    login_return_val_usr2 = auth_login_v1("k.z2@gmail.com", "a1b2c3d4e5")
    login_return_val_usr3 = auth_login_v1("k.z3@gmail.com", "a1b2c3d4e5")
    login_return_val_usr4 = auth_login_v1("k.z4567@gmail.com", "a1b2c3d4e5")

    assert register_return_val_usr1 == login_return_val_usr1
    assert register_return_val_usr2 == login_return_val_usr2
    assert register_return_val_usr3 == login_return_val_usr3
    assert register_return_val_usr4 == login_return_val_usr4

# ======================== SET 2 =================================
# Testing if is exception is raised for invalid first name and last name inputs

# First name exceeds the 50 character upper bound
def test_is_first_name_valid1():
    with pytest.raises(InputError):
        auth_register_v1(
            "k.z2991@gmail.com",
            "a1233ggsrrq2rhhbdrf",
            "Jafgasdfg222344fdgadhfdhfhkefgdfhdferwtrwqreqfreggsdfgdfh",
            "Smith"
        )

# First name length is less than the permitted lower bound
def test_is_first_name_valid2():
    with pytest.raises(InputError):
        auth_register_v1(
            "k.z2991@gmail.com",
            "a1233ggsrrq2rhhbdrf",
            "",
            "Smith"
        )

# Last name length is less than the permitted lower bound
def test_is_last_name_valid1():
    with pytest.raises(InputError):
        auth_register_v1(
            "k.z2991@gmail.com", "a1233ggsrrq2rhhbdrf", "John", ""
        )

# Last name exceeds the 50 character upper bound
def test_is_last_name_valid2():
    with pytest.raises(InputError):
        auth_register_v1(
            "k.z2991@gmail.com",
            "a1233ggsrrq2rhhbdrf",
            "Ryan",
            "Jafgasdfgfdgadhfdhfhkefgdfhdferwtrwqreqfreggsdfgdfh"
        )
