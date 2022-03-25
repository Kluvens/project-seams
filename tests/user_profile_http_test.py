import json
import requests
import pytest
from src.config import url
from tests.http_helpers import GenerateTestData
from src.error import InputError
from requests import HTTPError


#====================== Helper functions / Fixtures ===============
########## THIS SECTION WILL BE MOVED TO http_helpers.py ##########
OKAY = 200
ACEESS_ERROR = 403
INPUT_ERROR = 400

def reset_call():
    requests.delete(url + 'clear/v1')


@pytest.fixture()
def dummy_data():
    data_instance = GenerateTestData(url)
    return data_instance


@pytest.fixture
def route():
    return url + "user/profile/v1"

def user_profile_request(route, token, u_id):
    return requests.get(route, params={"token" : token})

# Index DOES NOT refer to a database index.
# It's just the order in which a user's info
# was passed to an auth/register/v1 request
def user_expected_details(user_info, token, user_idx):
    return {  
    'u_id' : user1_list[0]["token"]
    'email' : user1_info["email"], 
    'name_first' : user1_info["name_first"],
    'name_last' : user1_info["name_last"],
    'handle_str' : user1_info["name_first"] + user1_info["name_last"]
    }
#================Test Exceptions: Invalid Token===================

# Invalid token - non jwt compliant string.
@pytest.mark.parameterize("random_str", 
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

    assert response.status_code == ACEESS_ERROR


#Invalid u_id
@pytest.mark.parameterize("invalid_uid", ["123", "1", "2"])
def test_invalid_u_id(dummy_data):
    reset_call()
    users_list = dummy_data.register_users(num_of_users=2)
    user1 = users_list[1]
    dummy.data.logout_request(user1["token"])

    user0 = users_list[0]
    response = user_profile_request(user0["token"], user1["auth_user_id"])

    assert response.status_code == ACCESS_ERROR


# Invalid token - jwt compliant
def test_random_invalid_token(dummy_data):
    reset_call()
    users_list = dummy_data.register_users(num_of_users=4)
    # Last to get logged out
    user2_uid = users_list[2]["auth_user_id"]
    for user in user_list:
        dummy.data.logout_request(user["token"])
        response = user_profile_request(user["token"], user2_uid)
        assert response.status_code == ACEESS_ERROR


#=================Testing HTTP layer==============================

@pytest.mark.parameterize("user_idx", ["0", "1"])
def test_user_prof_response(dummy_data):
    reset_call()
    users_list = dummy_data.register_users(num_of_users=2)
    
    user_token = users_list[user_idx]["token"]
    user_uid = users_list[user_idx]["auth_user_id"]
    
    response = users_profile_request(user_token, user_uid)
    assert response.status_code == OKAY
    
    user_details_dict = json.loads(response.text)
    
    # Grab dummy_user1 info used when registering them (no access to any database)
    expected_user_det = user_expected_details(
        dummy_data.dummy_owner(), users_list[user_idx]["token"])

    assert user_details_dict == expected_user_det
