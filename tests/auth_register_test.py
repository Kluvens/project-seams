'''
Description:
This module contains tests for the auth_register_v1 function
based on the black box testing model

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
    clear_v1()
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


# ================================================================
#                        Test Exceptions
# Each set addresses one type of InputError as per the project requirments


# ======================== SET 1 =================================
# Test if an InputError exceptipn is rasied for invalid email input

def test_is_email_valid1():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1("invaild email", "a1b2c3d4e5", "Kais", "Alzubaidi")

# Note to self: Look for better regex "@99.com" is not spotted
def test_is_email_valid2():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1(
            "emaildoesnotexit99.com",
            "a1b2c3d4e5",
            "Kais",
            "Alzubaidi"
        )

# ======================== SET 2 =================================
# Test if exception is raised when an attempting to add an existing email

def test_is_email_registered1():
    clear_v1()
    auth_register_v1("k.z2991@gmail.com", "aqwregjh123", "Sonia", "something")
    with pytest.raises(InputError):
        auth_register_v1("k.z2991@gmail.com", "a1b2c3d4e5", "Jake", "O'conor")

def test_is_email_registered2():
    clear_v1()
    auth_register_v1("ka.z2991@gmail.com", "aqwreg123", "Sonia", "something")
    auth_register_v1("ka1.z2991@gmail.com", "aqwreg123", "Sonia", "something")
    auth_register_v1("kai1.z2991@gmail.com", "aqwre123", "Sonia", "something")
    with pytest.raises(InputError):
        auth_register_v1("ka1.z2991@gmail.com", "a1b2c3d4", "Kai", "Renz")


# Multiple users exist, testing the function's ability 
# to detect existing email when it's "randomly" placed in
# the database and raises an InputError
def test_is_email_registered3():
    clear_v1()
    auth_register_v1("ka.z2991@gmail.com", "aqwreg123", "Sonia", "something")
    auth_register_v1("ka1.z2991@gmail.com", "aqwreg123", "Sonia", "something")
    auth_register_v1("kai.z2991@gmail.com", "aqwreg123", "Sonia", "something")
    auth_register_v1("ka2.z2991@gmail.com", "aqwreh123", "Sonia", "something")
    auth_register_v1("kai1.z2991@gmail.com", "aqwre123", "Sonia", "something")

    with pytest.raises(InputError):
        auth_register_v1("ka2.z2991@gmail.com", "a1b2c3d4", "Kai", "Renz")


# ======================== SET 3 =================================

# Testing if exception is raised when password is less than 6 characters

def test_is_password_valid1():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1("k.z2991@gmail.com", "a12", "Jake", "O'Conor")


def test_is_password_valid2():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1("k.z2991@gmail.com", "aaa11", "Jake", "O'Conor")


def test_is_password_valid3():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1("k.z2991@gmail.com", "", "Jake", "O'Conor")



# ======================== SET 4 =================================
# Testing if an exception is raised for invalid first name and last name inputs

# First name exceeds the 50 character upper bound
def test_is_first_name_valid1():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1(
            "k.z2991@gmail.com",
            "a1233ggsrrq2rhhbdrf",
            "Jafgasdfg222344fdgadhfdhfhkefgdfhdferwtrwqreqfreggsdfgdfh",
            "Smith"
        )

# First name length is less than the permitted lower bound
def test_is_first_name_valid2():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1(
            "k.z2991@gmail.com",
            "a1233ggsrrq2rhhbdrf",
            "",
            "Smith"
        )

# Last name length is less than the permitted lower bound
def test_is_last_name_valid1():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1(
            "k.z2991@gmail.com", "a1233ggsrrq2rhhbdrf", "John", ""
        )

# Last name exceeds the 50 character upper bound
def test_is_last_name_valid2():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1(
            "k.z2991@gmail.com",
            "a1233ggsrrq2rhhbdrf",
            "Ryan",
            "Jafgasdfgfdgadhfdhfhkefgdfhdferwtrwqreqfreggsdfgdfh"
        )
