''' 
Testing module for the auth_register_v1 function
Details about the function input, returns and exceptions can be found
in the project's spec.

# version1.0. -- Kais Al

Note on style: Cetain stylistic features have been ignored for now.

'''

import pytest
from src.error import InputError
from src.auth import auth_register_v1
from src.data_store import data_store
from src.other import clear_v1

# Data structrue used to store users 

'''
data = {
    'users' : []
    'channels: []
    '....' : []
}

data is a dictionary consisting of a few main key: 'users', 'channels', etc

The 'users' key's value is a list that will be used to store each user's user_id

Each user_id will be an integer key whose value is a dictionary containing user's data:

uid: {
    'f_name': 'John'
    'l_name': 'Smith'
    'email': 'john_smith123@something.com'
    'password : '123smith123'
    'handle' : 'johnsmith'
}


uid1 = auth_register_v1("k@gg.com", "123abc123", "Kai", "zz")

====> Data structre after adding new user:
data = {
    users: [
        uid1: {
            'email : "k@gg.com",
            'password: "123abc123"
            'first_name' : "Kai",
            'last_name' : "zz",
            'handle' : "kaizz",
        }
    ]
}
    channels : []
    '...' : []
'''




''' ======================================================== '''
#                   Tests: Program Correctness

#Assumptions:

# All inputs are valid and no exceptions have been rasied
# Different users can have the same password
# Names can have non alpha-numeric characters 
# First and last names must each at least contain one alphanumeric character.
# For now, input must be of the form of printable ASCII characters.



# ======================== SET 1 =================================
# Concatenation of first name and last name is less than or or equal to 20 characters
# Handle is unique (not taken by an existing user)


# First and last names strictly contain lowercase characters
def test_simple_handle1():
    clear_v1()
    uid = auth_register_v1("k.z123@gmail.com", "a1b2c3d4e5", "kais", "alzubaidi")
    data = data_store.get()
    assert(data['users'][uid]['handle'] == "kaisalzubaidi")


# First and last names contain uppercase characters
def test_simple_handle2():
    clear_v1()
    uid = auth_register_v1("k.z123@gmail.com", "a1b2c3d4e5", "KaIS", "AlzuBaidI")
    data = data_store.get()
    assert(data['users'][uid]['handle'] == "kaisalzubaidi")


# First and last names contain a mix of alphanumeric characters
def test_simple_handle3():
    clear_v1()
    uid = auth_register_v1("k.z123@gmail.com", "a1b2c3d4e5", "KaIS12", "AlzuBaidI92190")
    data = data_store.get()
    assert(data['users'][uid]['handle'] == "kais12alzubaidi92190")

# Shortest valid first and last name 
def test_simple_handle4():
    clear_v1()
    uid = auth_register_v1("k.z123@gmail.com", "a1b2c3d4e5", "K", "z")
    data = data_store.get()
    assert(data['users'][uid]['handle'] == "kz")


# ======================== SET 2 =================================
# Test behaviour for long names
# Concatenated string of first and last name exceeds 20 characters 


def test_long_username_handle1():
    clear_v1()
    uid = auth_register_v1("i_hate_tests123@gmail.com", "wowhisnameislong123", "Hubert", "Wolfeschlegelsteinhausenbergredroff")
    data = data_store.get()
    assert(data['users'][uid]['handle'] == "hubertwolfeschlegels")

def test_long_username_handle2():
    uid = auth_register_v1("kakarot999@gmail.com", "powerlevelover9000", "SonGuko", "SuperSayianGodSuperSayianKaioKenX20")
    data = data_store.get()
    assert(data['users'][uid]['handle'] == "songukosupersayiansu")
    


# ======================== SET 3 =================================
# Test behaviour if handle is taken with simple names

# Test behaviour if handle is taken and require an incrementing suffix
def test_taken_handle_simple1():
    clear_v1()
    uid1 = auth_register_v1("k.z123@gmail.com", "a1b2c3d4e5", "kais", "alzubaidi")
    uid2 = auth_register_v1("k.z1234@gmail.com", "a1b2c3d4e5", "kais", "Al_zubaidi")

    data = data_store.get()
    assert(data['users'][uid1]['handle'] == "kaisalzubaidi")
    assert(data['users'][uid2]['handle'] == "kaisalzubaidi0")

# Test handle generation for multiple users where the concatenation of their first and last
# name matches existing users 
def test_taken_handle_simple2():
    clear_v1()
    uid1 = auth_register_v1("k.z123@gmail.com", "a1b2c3d4e5", "kais", "alzubaidi")
    uid2 = auth_register_v1("k.z1234@gmail.com", "a1b2c3d4e5", "kais", "Al_zubaidi")
    uid3 = auth_register_v1("k.z12345@gmail.com", "a1b2c3d4e5", "Ryan", "uddin")
    uid4 = auth_register_v1("k.z123456@gmail.com", "a1b2c3d4e5", "KAIS", "ALZUBAIDI")
    uid5 = auth_register_v1("k.z1234567@gmail.com", "a1b2c3d4e5", "kais", "ALZubaidi")

    data = data_store.get()
    assert(data['users'][uid1]['handle'] == "kaisalzubaidi")
    assert(data['users'][uid2]['handle'] == "kaisalzubaidi0")
    assert(data['users'][uid4]['handle'] == "kaisalzubaidi1")
    assert(data['users'][uid5]['handle'] == "kaisalzubaidi2")


# Test behaviour if handle is taken with long names, when handle generation
# requires adding an incrementing interger suffix at the end (which may exceed 20 characters)
def test_taken_handle_long1():
    clear_v1()
    uid1 = auth_register_v1("i_hate_tests123@gmail.com", "a1b2c3d4e5", "Hubert", "Wolfeschlegelsteinhausenbergredroff123345dsfa")
    uid2 = auth_register_v1("i_hate_tests1234@gmail.com", "a1b2c3d4e5", "Hubert__", "Wolfeschlegelste12")
    uid3 = auth_register_v1("i_hate_tests12345@gmail.com", "a1b2c3d4e5", "__HuBert___", "Wolfeschlegelsteinhause34235nbergr")
    data = data_store.get()
    assert(data['users'][uid1]['handle'] == "hubertwolfeschlegels")
    assert(data['users'][uid2]['handle'] == "hubertwolfeschlegels0")
    assert(data['users'][uid3]['handle'] == "hubertwolfeschlegels1")

    clear_v1()
def test_taken_handle_long2():
    uid1 = auth_register_v1("i_hate_tests123@gmail.com", "Hubert", "Wolfeschlegelsteinhausenbergredroff123345dsfa")
    uid2 = auth_register_v1("i_hate_tests1234@gmail.com", "Hubert", "Wolfeschlegelsteinhausenbergredroffgsdg")
    data = data_store.get()
    assert(data['users'][uid1]['handle'] == "hubertwolfeschlegels")
    assert(data['users'][uid2]['handle'] == "hubertwolfeschlegels0")


# ======================== SET 4 =================================

# Test if register can add 1 user to database by accessing their data using auth_id
def test_user_auth_register1():
    clear_v1()
    uid = auth_register_v1("k.z123@gmail.com", "a1b2c3d4e5", "kais", "alzubaidi")
    data = data_store.get()
    assert(data['users'][uid]['email'] == "k.z123@gmail.com")
    assert(data['users'][uid]['password'] == "a1b2c3d4e5")
    assert(data['users'][uid]['first_name'] == "kais")
    assert(data['users'][uid]['last_name'] == "alzubaidi")
    assert(data['users'][uid]['handle'] == "kaisalzubaidi")


# Test if register can add multiple users to data base by accessing their data using auth_id
def test_multiple_users_auth_register2():
    clear_v1()
    uid1 = auth_register_v1("k.z123@gmail.com", "a1b2c3d4e5", "kais", "alzubaidi")
    uid2 = auth_register_v1("k.z1234@gmail.com", "a1b2c3d4e5", "KaIS12", "AlzuBaidI92190")
    uid3 = auth_register_v1("kakarot999@gmail.com", "a1b2c3d4e5", "SonGuko", "SuperSayianGodSuperSayianKaioKenX20")
    uid4 = auth_register_v1("onepunchman1111@gmail.com", "a1b2c3d4e5d6e7AAAA", "Ryan_22", "Saitama")

    data = data_store.get()

    assert(data['users'][uid2]['email'] == "k.z1234@gmail.com")
    assert(data['users'][uid2]['password'] == "a1b2c3d4e5")
    assert(data['users'][uid2]['first_name'] == "KaIS12")
    assert(data['users'][uid2]['last_name'] == "AlzuBaidI92190")
    assert(data['users'][uid2]['handle'] == "kais12alzubaidi92190")

    assert(data['users'][uid2]['email'] == "onepunchman1111@gmail.com")
    assert(data['users'][uid2]['password'] == "a1b2c3d4e5d6e7AAAA")
    assert(data['users'][uid2]['first_name'] == "Ryan_22")
    assert(data['users'][uid2]['last_name'] == "Saitama")
    assert(data['users'][uid2]['handle'] == "ryan22saitama")



# ======================== SET 5 =================================
##### These tests will be added or discarded after discussing project assumptions during meeting #####

# Test if handle is generated correctly with first and last names contain
# non alpha number characters 
def test_handle_non_alphanumeric_name1():
    pass

def test_handle_non_alphanumeric_name1():
    pass

def test_handle_non_ascii_alphanumer_name():
    pass


'''                  ======================================================== 
                                        Test Exceptions
# Each test 'class/set' addresses one exception point as per the project requirments 
'''


# ======================== SET 1 =================================
# Test if an InputError exceptipn is rasied for invalid email input

def test_is_email_valid1():    
    with pytest.raises(InputError):
        auth_register_v1("invaild email", "a1b2c3d4e5", "Kais", "Alzubaidi")

def test_is_email_valid1():    
    with pytest.raises(InputError):
        auth_register_v1("emaildoesnotexit@99.com", "a1b2c3d4e5", "Kais", "Alzubaidi")

def test_is_email_valid3():    
    with pytest.raises(InputError):
        auth_register_v1("emaildoesnotexit@99.com", "a1b2c3d4e5", "Kais", "Alzubaidi")


# ======================== SET 2 =================================
# Test if exception is raised when an attempting to add an existing email
def test_is_email_registered():    
    auth_register_v1("k.z2991@gmail.com", "aqwregjh123", "Sonia", "something")
    with pytest.raises(InputError):
        auth_register_v1("k.z2991@gmail.com", "a1b2c3d4e5", "Jake", "O'conor")



# ======================== SET 3 =================================
# Testing if exception is raised when password is less than 6 characters

def test_is_password_valid1():    
    with pytest.raises(InputError):
        auth_register_v1("k.z2991@gmail.com", "a12", "Jake", "O'Conor")


def test_is_password_valid2():    
    with pytest.raises(InputError):
        auth_register_v1("k.z2991@gmail.com", "aaa11", "Jake", "O'Conor")


def test_is_password_valid3():    
    with pytest.raises(InputError):
        auth_register_v1("k.z2991@gmail.com", "", "Jake", "O'Conor")



# ======================== SET 4 =================================
# Testing if is exception is raised for invalid first name and last name inputs

# First name exceeds the 50 character upper bound
def test_is_first_name_valid():    
    with pytest.raises(InputError):
        auth_register_v1(
            "k.z2991@gmail.com", "a1233ggsrrq2rhhbdrf", 
            "Jafgasdfg222344fdgadhfdhfhkefgdfhdferwtrwqreqfreggsdfgdfh", "Smith"
    )

# First name length is less than the permitted lower bound 
def test_is_first_name_valid():    
    with pytest.raises(InputError):
        auth_register_v1(
            "k.z2991@gmail.com", "a1233ggsrrq2rhhbdrf", 
            "", "Smith"
    )

# Last name length is less than the permitted lower bound 
def test_is_first_name_valid():    
    with pytest.raises(InputError):
        auth_register_v1(
            "k.z2991@gmail.com", "a1233ggsrrq2rhhbdrf", "John", ""
    )

# Last name exceeds the 50 character upper bound
def test_is_last_name_valid():
    with pytest.raises(InputError):
        auth_register_v1(
            "k.z2991@gmail.com", "a1233ggsrrq2rhhbdrf", 
            "Ryan", "Jafgasdfgfdgadhfdhfhkefgdfhdferwtrwqreqfreggsdfgdfh"
        )
