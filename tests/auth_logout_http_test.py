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


def reset_call():
    requests.delete(url + 'clear/v1')


@pytest.fixture()
def dummy_data():
    data_instance = GenerateTestData(url)
    return data_instance


@pytest.fixture
def route():
    return url + "auth/logout/v1"

#==================================================================

# Check behaviour when there is a varaible number of registers
# and logged in users


@pytest.mark.parametrize("num_of_users, user_num", [(1, 0), (2, 1), (3, 2)])
def test_logout_new_user(route, dummy_data, num_of_users, user_num):
    reset_call()
    user_dict = dummy_data.register_users(num_of_users)[user_num]
    print(user_dict)
    response_obj = requests.post(route, json=user_dict["token"])
    assert response_obj.status_code == OKAY
    assert response_obj.json() == {}

    # Since uesr is logged out, they should not be able to create
    # a channel as token is invalid
    response = dummy_data.create_channel(1, user_dict['token'])
    assert response.status_code == 403

# #================================================================

#invalid token - jwt compliant
@pytest.mark.parametrize("num_of_users, user_num", [(1, 0), (2, 0), (4, 2)])
def test_logout_invalid_token(route, dummy_data, num_of_users, user_num):
    reset_call()
    user_dict = dummy_data.register_users(num_of_users)[user_num]
    response_obj = requests.post(route, json=user_dict["token"])
    assert response_obj.status_code == OKAY

    response_obj = requests.post(route, json=user_dict["token"])
    assert response_obj.status_code == 403

# invalid token - random string, not jwt compliant
def test_logout_invalid_random_token(route, dummy_data):
    reset_call()
    dummy_data.register_users(num_of_users=3)
    response_obj = requests.post(route, json="random token")
    assert response_obj.status_code == 403
