'''
This is testing module for the user/profile/v1 route.

This module makes use of modularised fixtures which
can be found in src.conftest.py

Additionally, a helper class has been used
to generate dummy user test data to pass in
the server.

Author: Kais Alzubaidi, z5246721

'''


import pytest
import requests
from src.config import url
from src.error import InputError
from src.error import AccessError
import string
from tests.http_helpers import GenerateTestData
from tests.http_helpers import reset_call
from tests.http_helpers import is_success
import random
#====================== Helper functions / Fixtures ===============


@pytest.fixture
def route():
    return url + "search/v1"


def search_request(route, token, query):
    return requests.get(
        url + "search/v1", params={"token" : token, "query_str" : query})



@pytest.fixture
def setup(dummy_data):
    reset_call()
    users_list = dummy_data.register_users(num_of_users=5)
    user0_token = users_list[0]["token"]
    user1_token = users_list[1]["token"]
    channels_list = dummy_data.create_multiple_channels(num_of_channels=2, token=user0_token)
    ch0 = channels_list[0]["channel_id"]
    u_ids = [users_list[1]["auth_user_id"], users_list[1]["auth_user_id"]]
    dummy_data.invite_users(user0_token, ch0, u_ids, num_of_users=2)

    return {
        "channel_id" : ch0,
        "user0" : user0_token,
        "user1" : user1_token
    }

@pytest.fixture
def dummy_messages():
    return [
        "Hello, how are you!",
        "Hi, I am good!\n How are you?",
        "yeahhh not too bad!, what are YoU DoiNg today>?"
    ]

def get_message_ids(messages_list):
    message_ids = []
    for message in messages_list:
        message_ids.append(
            message["message_id"]
        )
    return message_ids

def get_messages(messages_list):
    return [message["message"] for message in messages_list] 

def is_this_message_pinned(message_id, messages_list):
    for message in messages_list:
        if message_id == message["message_id"]:
            if message["is_pinned"]:
                print("Hellsaidgohjsogjao;gj;sdao")
                return True
    return False

def is_this_user_reacted(message_id, messages_list):
    for message in messages_list:
        if message_id == message["message_id"]:
            if message["reacts"]["is_this_user_reacted"]:
                return True
    return False


# #===================== Testing Exceptions ========================

@pytest.mark.parametrize("query", [
    "", 
    # 1001 characters
    "HHhhHHhhNNAAaa" * 100
    ]
)
def test_invalid_query(dummy_data, route, query):
    reset_call()
    user0_dict = dummy_data.register_users(num_of_users=1)[0]
    print(type(query))
    response = search_request(route, user0_dict["token"], query)
    assert response.status_code == InputError.code


@pytest.mark.parametrize("invalid_token", ["Invalid", "ALgxTlxPcNyqczQTXQUZ"])
def test_rand_invalid_token(setup, route, invalid_token):
    response = search_request(route, invalid_token, "query")
    assert response.status_code == AccessError.code

# testing expired jwt complinat token
def test_invalid_token(route, dummy_data):
    reset_call()
    users_list = dummy_data.register_users(num_of_users=5)

    query_str = "Hey, how is it going?"
    for user in users_list:
        dummy_data.logout_request(user["token"])
        # user3 is the last to get logged out
        response = search_request(route, user["token"], query_str)
        assert response.status_code == AccessError.code


# #==================== Testing General Behaviour ==================
def test_return_type(route, setup):
    query_str = "Hi"
    response = search_request(route, setup["user0"], query_str)
    assert is_success(response.status_code)
    target_msgs = response.json()
    assert isinstance(target_msgs, dict)

    # query string is not in list
    assert target_msgs == {"messages" : []}




@pytest.mark.parametrize("msg", ["H", "!", "YOU", "you"])
def test_messages_with_reacts_and_pin(
    route, dummy_messages, setup, msg, dummy_data):
    ch0 = setup["channel_id"]
    user0_token = setup["user0"]
    user1_token = setup["user1"]


    msg1_dict = dummy_data.send_message(user0_token, ch0, dummy_messages[0])
    ## add react here
    msg2_dict = dummy_data.send_message(user1_token, ch0, dummy_messages[1])
    dummy_data.pin_msg(user0_token, msg2_dict["message_id"])
    msg3_dict = dummy_data.send_message(user0_token, ch0, dummy_messages[2])

    response = search_request(route, user0_token, msg)
    messages_list = response.json()["messages"]

    assert isinstance(messages_list, list)

    return_msg_ids = get_messages(messages_list)
    expected = [msg1_dict["message_id"], msg2_dict["message_id"], msg3_dict["message_id"]]

    assert return_msg_ids.sort() == expected.sort()
    
    return_messages = get_messages(messages_list)
    for message in return_messages:
        assert message in dummy_messages
    

    assert is_this_message_pinned(msg2_dict["message_id"], messages_list)

# def test_messages_no_pin_no_react(test_setup):
#     pass
