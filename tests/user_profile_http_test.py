'''
This is testing module for the user/profile/v1 route.

This module makes use of modularised fixtures which
can be found in src.conftest.py

Additionally, a helper class has been used
to generate dummy user test data to pass in
the server.

Author: Kais Alzubaidi, z5246721

'''

import json
import requests
import pytest
from src.config import url
from tests.http_helpers import GenerateTestData
from tests.http_helpers import reset_call


#====================== Helper functions / Fixtures ===============

OKAY = 200
ACCESS_ERROR = 403
INPUT_ERROR = 400


@pytest.fixture
def route():
    return url + "user/profile/v1"


def user_profile_request(token, u_id):
    return requests.get(
        url + "user/profile/v1", params={"token" : token, "u_id" : u_id})


def user_expected_details(user_info, u_id):
    return {  
    'u_id' : u_id,
    'email' : user_info["email"], 
    'name_first' : user_info["name_first"],
    'name_last' : user_info["name_last"],
    'handle_str' : (user_info["name_first"] + user_info["name_last"]).lower()
    }


#================Test Exceptions: Invalid Token===================

# Invalid token - non jwt compliant string.
@pytest.mark.parametrize("random_str", 
    [
        "",
        " ",
        "0"
        "$%#!#(*&!~~~!@#%^&*(^#@!!",
        "K5nposQGhC",
        "AERt57xvzMAP75M1SSZ4",
        "vziOn8qtcS0dair4QumzNORUKMj13vTA3i0mWm9i",
        "v6zDYwO1PpLyMIAi8DP2LudrNehIoaQhxsG0TbFUS37Igc6qx9GTsvjlKsTugWA7gvkM"
    ]
)
def test_random_invalid_token(dummy_data, random_str):
    reset_call()
    users_list = dummy_data.register_users(num_of_users=3)
    user0_uid = users_list[0]["auth_user_id"]
    response = user_profile_request(random_str, user0_uid)

    assert response.status_code == ACCESS_ERROR


# Invalid u_id
# Testing invalid u_id type, and two that u_ids that do not exist
# given that we called the clear request and register 4 users only
@pytest.mark.parametrize("invalid_uid", [5, 999, "1234"])
def test_invalid_u_id(dummy_data, invalid_uid):
    reset_call()

    users_list = dummy_data.register_users(num_of_users=4)

    user1_token = users_list[1]["token"]
    response = user_profile_request(user1_token, invalid_uid)

    assert response.status_code == ACCESS_ERROR



# Invalid token - jwt compliant
def test_invalid_token(dummy_data):
    reset_call()
    users_list = dummy_data.register_users(num_of_users=4)
    
    user3_uid = users_list[3]["auth_user_id"]
    for user in users_list:
        dummy_data.logout_request(user["token"])
        # user3 is the last to get logged out
        response = user_profile_request(user["token"], user3_uid)
        assert response.status_code == ACCESS_ERROR



#=================Testing HTTP layer==============================
# user idx refers to the order in which the users were registered
@pytest.mark.parametrize("user_idx", [0, 1, 2])
def test_users_request_profile(dummy_data, user_idx):
    reset_call()
    users_list = dummy_data.register_users(num_of_users=4)
    
    # The users making the profile request varies according to user_idx
    user_token = users_list[user_idx]["token"]

    # We're always requesting dummy_user1 profile.
    user_uid = users_list[1]["auth_user_id"]
    
    response = user_profile_request(user_token, user_uid)
    assert response.status_code == OKAY
    
    user_details_dict = json.loads(response.text)

    # This is still blackbox, as we're only testing http server interface
    expected_user_det = user_expected_details(
        dummy_data.data_dummy1(), 
        user_uid
    )

    assert user_details_dict == expected_user_det
