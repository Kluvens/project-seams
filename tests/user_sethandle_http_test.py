'''
This is testing module for the user/profile/sethandle/v1 route.

NOTE: This module makes use of modularised fixtures which
can be found in src.conftest.py

Additionally, a helper class has been used
to generate dummy user test data to pass in
the server. 


Author: Kais Alzubaidi, z5246721

'''
#====================== Import Statements ========================

import json
import requests
import pytest
from src.config import url
from tests.http_helpers import GenerateTestData
from tests.http_helpers import reset_call
from src.error import AccessError
from src.error import InputError

#====================== Helper functions / Fixtures ==============

@pytest.fixture
def route():
    # make sure other routes have profile in their name
    return url + "user/profile/sethandle/v1"


def user_sethandle_request(route, token, handle_str):
    return requests.put(
        route, 
        json={
            "token" : token,
            "handle_str" : handle_str,
        }
    )


def user_profile_request(token, u_id):
    return requests.get(
        url + "user/profile/v1", params={"token" : token, "u_id" : u_id})

#========================= Test Exception Handelling =============

# Invalid token - non jwt compliant string.
@pytest.mark.parametrize("random_token", 
    [
        "",
        " ",
        "****)()+@$(*$_!&&%(&&%*&*&@(*&(*^@",
        "UwpvGMswsDInLipwKolBdvWjSFsvsOwfZRaoafoIRpCvz",
        "Random STRING",
        # Removed the dot, so no headers or signitures
        # will be recognised
        """eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9eyJzd
        WIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9l
        IiwiaWF0IjoxNTE2MjM5MDIyfQ.OsYeNeIRzSGp0Ss2
        32RIL9xjKwsmo-c6slPSi0plpWE"""
    ]
)
def test_random_invalid_token(route, dummy_data, random_token):
    reset_call()
    dummy_data.register_users(num_of_users=4)
    handle_str = "IamAnewHandle"
    sethandle_response = user_sethandle_request(
        route, random_token, handle_str)

    assert sethandle_response.status_code == AccessError.code


# Invalid token - jwt compliant
def test_invalid_token(route, dummy_data):
    reset_call()
    users_list = dummy_data.register_users(num_of_users=3)
    user1_token = users_list[1]["token"]

    dummy_data.logout_request(user1_token)

    response = user_sethandle_request(route, user1_token, "BlackPanther90")
    assert response.status_code == AccessError.code

# Test invalid handles
@pytest.mark.parametrize("Invalid_handle_str", 
    [
        ""
        "RA",
        "KaI_Al",
        "`fJRZ]%BA`*MK0a",
        "tQeoZo2ACe8hcfnjRPwnX",
        "k9V2MjYQZvLvoJdoaBpdgmqscfJW"   
    ]
)
def test_invalid_handle(route, dummy_data, Invalid_handle_str):
    reset_call()
    users_list = dummy_data.register_users(num_of_users=3)
    user2_token = users_list[2]["token"]

    sethandle_response = user_sethandle_request(
        route, user2_token, Invalid_handle_str)
    
    assert sethandle_response.status_code ==  InputError.code


#===================Test route interactions/interface =================

# Testing differnet handles with different users
@pytest.mark.parametrize("user_idx, handle_str",
    [
        # 3 character handle
        (0, "LEE"),
        (1, "FiReFoX2000"),
        # 19 character handle
        (2, "0UiGleRoVsYOAfaBqfn"),
        # 20 Character handle
        (3, "OG18O9hyVChEgtJIr8c7")
    ]
)
def test_set_handle(route, dummy_data, user_idx, handle_str):
    reset_call()
    users_list = dummy_data.register_users(num_of_users=4)
    # trying setting new handle_str for different users (user_idx is changing)
    user_token = users_list[user_idx]["token"]
    user_u_id = users_list[user_idx]["auth_user_id"]

    sethandle_response = user_sethandle_request(route, user_token, handle_str)
    
    assert sethandle_response.status_code ==  200

    # Note that since reset is call with each user_idx parameter
    # new handle_str is guarnteed to not be duplicated 
    profile = user_profile_request(user_token, user_u_id).json()
    assert profile["handle_str"] == handle_str
