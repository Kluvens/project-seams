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
    return url + "users/all/v1"

def users_all_request(route, token):
    return requests.get(route, params={"token" : token})

# Index DOES NOT refer to a database index.
# It's just the order in which a user's info
# was passed to an auth/register/v1 request
def user_expected_details(user_info, token):
    return {  
    'u_id' : user1_list[0]["token"]
    'email' : user1_info["email"], 
    'name_first' : user1_info["name_first"],
    'name_last' : user1_info["name_last"],
    'handle_str' : user1_info["name_first"] + user1_info["name_last"]
    }
#================Test Exceptions: Invalid Token===================

# Invalid token - non jwt compliant string.
@pytest.mark.fixtures("random_str", 
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
def test_random_invalid_token(route, dummy_data, random_str):
    dummy_data.register_users(num_of_users=3)
    response = requests.get(route, json={"token" : random_str})

    assert response.status_code == ACEESS_ERROR



# Invalid token - jwt compliant
# registering users, logging them out and
# testing users/all/v1 excpetion handelling capability
# with a variable number of registered users
def test_random_invalid_token(route, dummy_data):
    reset_call()
    users_list = dummy_data.register_users(num_of_users=4)
    for user in user_list:
        dummy.data.logout_request(user["token"])
        response = requests.get(route, json={user["token"]})
        assert response.status_code == ACEESS_ERROR


#=================Testing HTTP layer==============================
def test_request_response():
    users_list = dummy_data.register_users(num_of_users=3)
    user0_token = users_list[0]["token"]
    response = users_all_request(user0_token)
    assert response.status_code == OKAY
    users_details_dict = json.loads(response.text)
    
    # Grab dummy_user1 info used when registering them (no access to any database)
    expected_output = []
    expected_user0 = user_expected_details(
        dummy_data.dummy_owner(), users_list[0]["token"])
    expected_output.append(expected_user0)
    expected_user1 = user_expected_details(
        dummy_data.dummy_user1(), users_list[1]["token"])
    expected_output.append(expected_user1)

    expected_user2 = user_expected_details(
        dummy_data.dummy_user2(), users_list[2]["token"])
    expected_output.append(expected_user2)
}

    assert users_details_dict == expected_output
