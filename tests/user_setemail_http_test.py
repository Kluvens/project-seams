'''
This is testing module for the user/profile/setemail/v1 route.

This module makes use of modularised fixtures which
can be found in src.conftest.py

Additionally, a helper class has been used
to generate dummy user test data to pass in
the server. 
NOTE: There is a modularised fixture called
dummy_data, which is used in this module. You
can find it under project_backend/conftest.py  

Author: Kais Alzubaidi, z5246721

'''

import json
import requests
import pytest
from src.config import url
from tests.http_helpers import GenerateTestData
from tests.http_helpers import reset_call
from src.error import AccessError
from src.error import InputError

#====================== Helper functions / Fixtures ===============


@pytest.fixture
def route():
    # make sure other routes have profile in their name
    return url + "user/profile/setemail/v1"


def user_setemail_request(route, token, email):
    return requests.put(
        route, 
        json={
            "token" : token,
            "email" : email,
        }
    )

def user_profile_request(token, u_id):
    return requests.get(
        url + "user/profile/v1", params={"token" : token, "u_id" : u_id})

#========================= Test Exception Handelling ==================

# Invalid token - non jwt compliant string.
@pytest.mark.parametrize("random_token", 
    [
        "",
        " ",
        "K5nposQGhC",
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
    users_list = dummy_data.register_users(num_of_users=4)
    new_email = "Kais999@seams.com"
    setemail_response = user_setemail_request(route, random_token, new_email)

    assert setemail_response.status_code == AccessError.code

# Invalid token - jwt compliant
def test_invalid_token(route, dummy_data):
    reset_call()
    users_list = dummy_data.register_users(num_of_users=4)
    user1_token = users_list[1]["token"]

    dummy_data.logout_request(user1_token)

    response = user_setemail_request(route, user1_token, "new_email123@seams.com")
    assert response.status_code == AccessError.code


#Invalid Email
@pytest.mark.parametrize("invalid_email", 
    [
        "invaild email",
        "emaildoesnotexit99.com",
        "a**z@.c.om",
        "qw@gmailcom"
    ]
)
def test_invalid_email(route, dummy_data, invalid_email):
    reset_call()
    users_list = dummy_data.register_users(num_of_users=3)
    user1_token = users_list[1]["token"]

    setemail_response = user_setemail_request(route, user1_token, invalid_email)

    assert setemail_response.status_code == InputError.code


@pytest.mark.parametrize("existing_email", 
    [
        "dummy1@seams.com",
        "dummy2@seams.com",
        "owner@seams.com",
    ]
)
def test_email_registered(route, dummy_data, existing_email):
    reset_call()
    users_list = dummy_data.register_users(num_of_users=4)
    user0_token = users_list[0]["token"]

    setemail_response = user_setemail_request(route, user0_token, existing_email)
  
    assert setemail_response.status_code == InputError.code

# Check if email becomes available after user is deleted NOTEEEE TO SELF

#================= Test Route Interface/Interactions =============
@pytest.mark.parametrize("user_idx", [0, 1, 2, 3])
def test_set_new_email(route, dummy_data, user_idx):
    reset_call()
    users_list = dummy_data.register_users(num_of_users=4)
    # trying changing emails of different users (user_idx is changing)
    user_token = users_list[user_idx]["token"]
    user_u_id = users_list[user_idx]["auth_user_id"]
    
    new_email = "new_email999@seams.com"
    setemail_response = user_setemail_request(route, user_token, new_email)
    
    assert setemail_response.status_code ==  200

    # Note that since reset is call with each user_idx parameter
    # new email is guarnteed to not be duplicated 
    profile = user_profile_request(user_token, user_u_id).json()
    assert profile["email"] == new_email
