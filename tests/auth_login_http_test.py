import json
import requests
import pytest
from src.config import url
from tests.http_helpers import GenerateTestData
from src.error import InputError
from requests import HTTPError
from src.helpers import decode_token

#====================== Helper functions / Fixtures ===============

def reset_call():
    requests.delete(url + 'clear/v1')


@pytest.fixture()
def dummy_data():
    data_instance = GenerateTestData(url)
    return data_instance


@pytest.fixture
def route():
    return url + "auth/login/v2"

#================= Testing Correctness ===========================


# Testing logging user functionality when we have a varying number
# of existing users
@pytest.mark.parametrize("num_of_users", [1, 2, 3, 4])
def test_login_existing_user(route, dummy_data, num_of_users):
    reset_call()
    registered_user_dict = dummy_data.register_users(num_of_users)[0]
    assert isinstance(registered_user_dict, dict)
    logged_in_user_dict = dummy_data.login(num_of_users=1)[0]
    assert (registered_user_dict['auth_user_id'] == 
        logged_in_user_dict['auth_user_id'])

    # assert (logged_in_user_dict['auth_user_id'] == 
        # decode_token(logged_in_user_dict['token']))


# Testing if logging in user multiple times will 
# generate unique session tokens



#==================Testing Exceptions=============================

@pytest.mark.parametrize("num_of_users", [1, 2, 3])

@pytest.mark.parametrize("email",
    [
    "dummy1@seams.com",
    "dummy2@seams.com",
    "dummy3@seams.com"
    ]
)

def test_does_email_exist(route, dummy_data, email, num_of_users):
    reset_call()
    dummy_data.register_users(num_of_users)
    with pytest.raises(HTTPError):
        requests.post(
            route, 
            json={"email" : email, "password" : "IamApassword"}
            ).raise_for_status()


# Choosing password that are very close the the actual
# password. Each parameter deals with a possible edge case
@pytest.mark.parametrize("email, password",
    [   
        ("owner@seams.com", "IAmanowner123"),
        ("dummy1@seams.com", "dummY1_123"),
        ("dummy2@seams.com", "dummY2_1234"),
        ("dummy3@seams.com", "AiahaHnqbu7pyoi3qmXhHtY99dlA")
    ]
)

def test_handelling_incorrect_password(route, dummy_data, email, password):
    reset_call()
    dummy_data.register_users(num_of_users=4)
    with pytest.raises(HTTPError):
        requests.post(
            route, 
            json={"email" : email, "password" : password}
            ).raise_for_status()
