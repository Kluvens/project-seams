import json
import requests
import pytest
from src.config import url
from tests.http_helpers import GenerateTestData
from src.error import InputError
from requests import HTTPError


#====================== Helper functions / Fixtures ===============

def reset_call():
    requests.delete(url + 'clear/v1')


@pytest.fixture
def register_test_users(num_of_users):
    dummy_data = GenerateTestData(url)
    users_return_dict = dummy_data.register_users(num_of_users)
    

@pytest.fixture()
def dummy_data():
    data_instance = GenerateTestData(url)
    return data_instance


@pytest.fixture
def route():
    return url + "auth/register/v2"


#======================= Testing Returned Data ===================


def test_return_type(dummy_data):

    reset_call()
    user = dummy_data.register_users(num_of_users=1)
    users_return_dict = user[0]

    assert isinstance(users_return_dict['auth_user_id'] , int)
    assert isinstance(users_return_dict['token'] , str)



def test_return_id_one_user(dummy_data):

    reset_call()

    registered_user = dummy_data.register_users(num_of_users=1)
    logged_in_user = dummy_data.login(num_of_users=1)

    # I added those two lines to increase readability
    register_route_return_id = registered_user[0]['auth_user_id']
    login_route_return_id = logged_in_user[0]['auth_user_id']

    assert register_route_return_id == login_route_return_id


def test_return_is_not_empty(dummy_data):
    reset_call()
    registered_user_dict = dummy_data.register_users(num_of_users=1)[0]
    assert registered_user_dict != {}


# Checking that auth_register returns the correct uid
# for multiple users
def test_return_id_multiple_users(dummy_data):
    reset_call()
    registered_users_return_list = dummy_data.register_users(num_of_users=4)
    logged_in_users_return_list = dummy_data.login(num_of_users=4)

    for user_num in range(0, 4):
        register_id  = registered_users_return_list[user_num]['auth_user_id']
        login_id = logged_in_users_return_list[user_num]['auth_user_id']

        assert register_id == login_id

# ====================Testing Exceptions==========================

# ======================== SET 1 =================================
# Test if an InputError exceptipn is rasied for invalid email input


@pytest.mark.parametrize("email", 
    [
        "invaild email",
        "emaildoesnotexit99.com",
        "dotnotcomma@a,com"
    ]
)

def test_is_email_valid(route, email):
    reset_call()
    response = requests.post(
        route, 
        json={
            "email": email,
            "password" : "123abc123",
            "name_first" : "Kais",
            "name_last" : "Alz"
        }
    )
    assert response.status_code == 400



# ======================== SET 2 =================================
#Test if exception is raised when attempting to add an existing email

@pytest.mark.parametrize("email", 
    [
        "owner@seams.com",
        "dummy1@seams.com",
        "dummy2@seams.com"
    ]
)
def test_email_registered(route, email):
    reset_call()
    dummy_data = GenerateTestData(url)
    registered_users = dummy_data.register_users(num_of_users=3)

    response = requests.post(
        route,
        json={
            "email": email,
            "password" : "123abc123",
            "name_first" : "Kais",
            "name_last" : "Alz"
        }
    )
    assert response.status_code == 400



#======================== SET 3 ==================================

# Testing if exception is raised when password is less than 6 characters

@pytest.mark.parametrize("password", ["", "a", "AAa", "12345", "* __1"])
def test_is_password_valid(route, password):
    reset_call()

    response = requests.post(
        route,
        json={
            "email": "Kais11011@seams.com",
            "password" : password,
            "name_first" : "Kais",
            "name_last" : "Alz"
        }
    )

    assert response.status_code == 400

#=========================== SET 4 ===============================
# Testing if an exception is raised for invalid first name and last name inputs

@pytest.mark.parametrize(
    "name_first,name_last", 
    #("INVALID first name", "valid last name")
    [("", "John"), 
    ("IcontainmorethanfiftycharactersSoIshouldChangeMyName", "KAiS"),
    #("valid first name", "INVALID last name")
    ("John", ""), 
    ("Kais", "IcontainmorethanfiftycharactersSoIshouldChangeMyName")]
)
def test_name_is_valid(route, name_first, name_last):
    reset_call()
    response = requests.post(
        route,
        json={
            "email": "Kais11011@seams.com",
            "password" : "IamApassword123",
            "name_first" : name_first,
            "name_last" : name_last
        }
    )
    assert response.status_code == 400
