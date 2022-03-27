'''
This is testing module for the user/setnamess/v1 route.

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
    return url + "user/setname/v1"


def user_setname_request(route, token, name_first, name_last):
    return requests.put(
        route, json={
            "token" : token,
            "name_first" : name_first,
            "name_last" : name_last
        }
    )

def user_profile_request(token, u_id):
    return requests.get(
        url + "user/profile/v1", params={"token" : token, "u_id" : u_id})


#================ Testing Exception Handelling ====================


# Invalid token - non jwt compliant string.
@pytest.mark.parametrize("random_token", 
    [
        "",
        " ",
        123431532,
        "$%#!#(*&!~~~/*-+++-*=.@@@!2$QXQ!",
        "K5nposQGhC",
        "AERt57xvzMAP75M1SSZ4",
        "vziOn8qtcS0i",

        "v6zDYwO1PpLyMIAi8DP2LudrNehIoaQhxsG0Tb",

        """eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9eyJzd
        WIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9l
        IiwiaWF0IjoxNTE2MjM5MDIyfQ.OsYeNeIRzSGp0Ss2
        32RIL9xjKwsmo-c6slPSi0plpWE"""
    ]
)
def test_random_invalid_token(route, dummy_data, random_token):
    reset_call()
    users_list = dummy_data.register_users(num_of_users=4)
    response = user_setname_request(route, random_token, "Kais", "Alzubaidi")

    assert response.status_code == ACCESS_ERROR



# Invalid token - jwt compliant
def test_invalid_token(route, dummy_data):
    reset_call()
    users_list = dummy_data.register_users(num_of_users=1)
    user0_token = users_list[0]["token"]

    dummy_data.logout_request(user0_token)

    response = user_setname_request(route, user0_token, "Kais", "Alzubaidi")
    assert response.status_code == ACCESS_ERROR


@pytest.mark.parametrize("name_first, name_last",
    [
        #("Invalid_first_name", "valid_last_name")
        ("", "Kamehameha"),
        ("IhaveAveryveryveryveryVERYveryveryveryverylongfirstname", "shortlastname"),
        ("RYQzyzpuMeSGKTPWlOjDHgWxxdfgkWuFmTxDFhayvcGpKWFHksO", "Kakarot"),
        #("Valid_first_name", "Invalid_last_name")
        ("Nomralfirstname", "FuQbxeJoLPOjFYSLyzmdZFWIEvZWehLnOvTifxWgDPtYkIGmdWKL"),
        ("Vegeta", ""),
        ("Kais", "dWRsNOqDLKFZfjeGQJxkgxvWjRwtjVRCFAVgvhxBRaJEGymIMnK"),
        #("Invalid_first_name", "Invalid_last_name")
        ("", ""),
        ("DmqUflXCwCabBiTOscAcWLlLWBjzrZkSBhYHpjkEKOQotcxlmHP",
        "knEnDoDqWDBoEXpauFpIkoRBkoFCLechJCoKQidcIPVZZJvaOcc")
    ]
)
def test_invalid_name(route, dummy_data, name_first, name_last):
    reset_call()
    users_list = dummy_data.register_users(num_of_users=4)
    user2_token = users_list[2]["token"]
    response = user_setname_request(route, user2_token, name_first, name_last)

    assert response.status_code == INPUT_ERROR


#================ Testing route functionality =====================

@pytest.mark.parametrize("name_first, name_last", 
    [
        ("K", "aKEZKqxUQRWNKMzTfAGPeybIBLNEFipcHsRjzEczWagNZvDqJA"),
        ("vgKOSqkGNyQIvCsKerJJqyBljTmjGiYNUjQriodLzyUEsJcouq", "Q"),
        ("Kais", "Alzubaidi")
    ]
)
def test_setting_name(route, dummy_data, name_first, name_last):
    reset_call()
    users_list = dummy_data.register_users(num_of_users=4)
    user1_u_id = users_list[1]["auth_user_id"]
    user1_token = users_list[1]["token"]
    
    response = user_setname_request(route, user1_token, name_first, name_last)
    assert response.status_code == OKAY

    response = user_profile_request(user1_token, user1_u_id)
    user0_dict = json.loads(response.text)

    assert user0_dict["name_first"] == name_first
    assert user0_dict["name_last"] == name_last
    assert user0_dict["handle_str"] == (name_first + name_last).lower()[:20]
