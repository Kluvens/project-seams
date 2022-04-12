'''
This module contains blackbox tests of the routes
auth/passwordreset/request/v1 and auth/passwordreset/reset/v1

'''

import pytest
import requests
from src.config import url
from src.error import InputError
from src.error import AccessError
from tests.http_helpers import reset_call
from tests.http_helpers import is_success
from tests.http_helpers import get_reset_code


def password_send_resetcode_request(email):
    return requests.post(url + "auth/passwordreset/request/v1",
        json={"email" : email})


def password_reset_request(reset_code, new_password):
    return requests.post(url + "auth/passwordreset/reset/v1",
        json={"reset_code" : reset_code, "new_password" : new_password})


################## TESTING GENERAL BEHAVIOUR #####################

# This is the only test that can be done without violating the 
# blackbox testing method

@pytest.mark.parametrize("email",
    [
    # valid email
    "dummy1@seams.com",
    "Invalid Email",
    "valid_but_doesnot_exist@seams.com"
    ]
)
def test_password_request_return(dummy_data, email):
    reset_call()
    dummy_data.register_users(num_of_users=4)
    response =  password_send_resetcode_request(email)
    assert is_success(response.status_code)
    return_dict = response.json()
    assert isinstance(return_dict, dict) and return_dict == {}


# Test succesful logout after making reset request
def test_logout_sessions_after_reset(dummy_data):
    reset_call()
    users_list = dummy_data.register_users(num_of_users=4)
    dummy1_token = users_list[1]["token"]

    dummy1_email = dummy_data.data_dummy1()["email"]
    response =  password_send_resetcode_request(dummy1_email)
    assert is_success(response.status_code)

    ## Since user is logged out, trying to log them out should
    # throw the an AccessError
    response = dummy_data.logout_request(dummy1_token)
    assert response.status_code == AccessError.code
##################### auth/passwordreset/reset ###################

####################### TESTING EXCEPTIONS #######################

@pytest.mark.parametrize("invalid_reset_code",
    [
    # valid but already used
    "49d5c2c3eede46f38dee00d4b93395ed",
    "InvalidResetCode"
    ]
)
def test_invalid_reset_code(dummy_data, invalid_reset_code):
    reset_call()
    dummy_data.register_users(num_of_users=3)
    response_reset_request = password_send_resetcode_request(
        dummy_data.data_dummy1()["email"])
    assert is_success(response_reset_request.status_code)

    new_password = "123123123"
    response = password_reset_request(invalid_reset_code, new_password)
    assert response.status_code == InputError.code


# ###### Still need to improve this by passing the actual reset_code ####
@pytest.mark.parametrize("invalid_new_password", ["", "12345"])
def test_invalid_new_password(dummy_data, invalid_new_password):
    reset_call()
    dummy_data.register_users(num_of_users=5)
    user_login_info = dummy_data.data_dummy1()
    response_reset_request = password_send_resetcode_request(
        user_login_info["email"])

    assert is_success(response_reset_request.status_code)
    
    reset_code = ""
    response = password_reset_request(reset_code, invalid_new_password)
    assert response.status_code == InputError.code



# need a acual email, change http helpers
def test_success_reset_password(dummy_data):
    reset_call()
    users_list = dummy_data.register_users(num_of_users=5)

    user4_token = users_list[4]["token"]
    user4_login_info = dummy_data.data_dummy_real()
    email = user4_login_info["email"]

    response_reset_request = password_send_resetcode_request(email)
    assert response_reset_request.status_code == 200
    
    # Checking user who sent the request is logged out
    response = dummy_data.logout_request(user4_token)
    assert response.status_code == AccessError.code

    new_password = "NewPassword"
    response = password_reset_request(
        get_reset_code(), new_password)

    ## Try to login using old password
    old_password = user4_login_info["password"]
    login_response = dummy_data.login_user(email, old_password)
    assert login_response.status_code == InputError.code

    ## Try to login using the new password
    login_response = dummy_data.login_user(email, new_password)
    assert is_success(login_response.status_code)

