import json
import requests
import pytest
from src.config import url
from src.error import AccessError
from tests.http_helpers import GenerateTestData
from tests.http_helpers import reset_call


#====================== Helper functions / Fixtures ===============

OKAY = 200

@pytest.fixture
def route():
    return url + "users/all/v1"


def users_all_request(route, token):
    return requests.get(
        route, params={"token" : token})


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
@pytest.mark.parametrize("random_token", 
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
def test_random_invalid_token(route, dummy_data, random_token):
    reset_call()
    dummy_data.register_users(num_of_users=3)
    response = users_all_request(route, token=random_token)

    assert response.status_code == AccessError.code



# Invalid token - jwt compliant
# registering users, logging them out and
# testing users/all/v1 excpetion handelling capability
# with a variable number of registered users
def test_invalid_token(route, dummy_data):
    reset_call()
    users_list = dummy_data.register_users(num_of_users=4)
    for user in users_list:
        dummy_data.logout_request(user["token"])
        response = users_all_request(route, user["token"])
        assert response.status_code == AccessError.code


def test_users_all_request(route, dummy_data):
    reset_call()
    users_list = dummy_data.register_users(num_of_users=2)
    
    # The users making the profile request varies according to user_idx
    user0_token = users_list[0]["token"]

    user0_u_id = users_list[0]["auth_user_id"]
    user1_u_id = users_list[1]["auth_user_id"]

    response = users_all_request(route, user0_token)
    assert response.status_code == OKAY

    users_details_dict = json.loads(response.text)["users"]
    
 
    for user_dict in users_details_dict:
        user_dict.pop("profile_img_url")

    # This is still blackbox, as we're only testing http server interface
    expected_user0_det = user_expected_details(
        dummy_data.data_owner(), 
        user0_u_id
    )

    expected_user1_det = user_expected_details(
    dummy_data.data_dummy1(), user1_u_id)

    expected_output = [expected_user0_det, expected_user1_det]
    
    assert users_details_dict == expected_output
