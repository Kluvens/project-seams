import pytest
import datetime
import threading
import requests
from src.config import url
from src.error import InputError, AccessError
from tests.http_helpers import GenerateTestData

OKAY = 200

def reset_call():
    requests.delete(url + 'clear/v1')

def message_sendlater_request(token, channel_id, message, time_sent):
    response = requests.post(url + "/message/sendlater/v1", 
        json={
            "token" : token,
            "channel_id" : channel_id,
            "message" : message,
            "time_sent" : time_sent,
        })
    return response

def message_sendlaterdm_request(token, dm_id, message, time_sent):
    response = requests.post(url + "/message/sendlaterdm/v1", 
        json={
            "token" : token,
            "dm_id" : dm_id,
            "message" : message,
            "time_sent" : time_sent,
        })
    return response

def send_message_request(token, channel_id, message):
    response = requests.post(url + "/message/send/v1", 
        json={
            "token" : token,
            "channel_id" : channel_id,
            "message" : message,
        })
    return response

def send_dm_message_request(token, dm_id, message):
    response = requests.post(url + "/message/senddm/v1", 
        json={
            "token" : token,
            "dm_id" : dm_id,
            "message" : message,
        })
    return response

@pytest.fixture
def create_route():
    return url + "channels/create/v2"

def get_channel_messages(token, channel_id, start):
    response = requests.get(url + "/channel/messages/v2",
        params={
            "token" : token,
            "channel_id" : channel_id,
            "start" : start,
        })
    return response

def post_channel_invite(token, channel_id, u_id):
    response = requests.post(url + "/channel/invite/v2",
        json={
            "token" : token,
            "channel_id" : channel_id,
            "u_id" : u_id,
        })
    return response

'''
InputError will occur when channel_id is not a valid
or the length of message is more than 1000 characters or time_sent is a time in the past.
'''
@pytest.mark.parametrize("invalid_channel_id", [-488445, -7474, -1, -49864864651651654])
# Testing case for when channel_id is invalid
def test_messages_sendlater_invalid_channel_id_InputError(dummy_data, create_route, invalid_channel_id):
    reset_call()

    users_list = dummy_data.register_users(num_of_users=1)
    user0 = users_list[0]
    ch1 = requests.post(create_route, json={
        'token': user0["token"],
        'name': 'ch1',
        'is_public': True
    })
    assert ch1.status_code == OKAY

    message = "hello world"
    time = datetime.datetime.now().replace(microsecond=0) + datetime.timedelta(0, 5)
    time_sent = time.timestamp()

    response = message_sendlater_request(user0['token'], invalid_channel_id, message, time_sent)
    assert response.status_code == InputError.code

def test_sendlater_message_less_than_one_InputError(dummy_data, create_route):
    reset_call()

    users_list = dummy_data.register_users(num_of_users=1)
    user0 = users_list[0]
    ch1 = requests.post(create_route, json={
        'token': user0["token"],
        'name': 'ch1',
        'is_public': True
    })
    assert ch1.status_code == 200
    ch1_dict = ch1.json()

    time = datetime.datetime.now().replace(microsecond=0) + datetime.timedelta(0, 5)
    time_sent = time.timestamp()
    message = ''

    response = message_sendlater_request(user0['token'], ch1_dict['channel_id'], message, time_sent)
    assert response.status_code == InputError.code

'''
InputError when message is more than 1000
'''
def test_sendlater_message_more_than_thousand_InputError(dummy_data, create_route):
    reset_call()

    users_list = dummy_data.register_users(num_of_users=1)
    user0 = users_list[0]
    ch1 = requests.post(create_route, json={
        'token': user0["token"],
        'name': 'ch1',
        'is_public': True
    })
    assert ch1.status_code == 200
    ch1_dict = ch1.json()

    time = datetime.datetime.now().replace(microsecond=0) + datetime.timedelta(0, 5)
    time_sent = time.timestamp()
    message = 'hello'*5000

    response = message_sendlater_request(user0['token'], ch1_dict['channel_id'], message, time_sent)
    assert response.status_code == InputError.code

def test_sendlater_past_InputError(dummy_data, create_route):
    reset_call()

    users_list = dummy_data.register_users(num_of_users=1)
    user0 = users_list[0]
    ch1 = requests.post(create_route, json={
        'token': user0["token"],
        'name': 'ch1',
        'is_public': True
    })
    assert ch1.status_code == OKAY
    ch1_dict = ch1.json()

    message = "hello world"
    time = datetime.datetime.now().replace(microsecond=0) - datetime.timedelta(0, 5)
    time_sent = time.timestamp()

    response = message_sendlater_request(user0['token'], ch1_dict['channel_id'], message, time_sent)
    assert response.status_code == InputError.code

'''
AccessError will occur when a user is not a member/owner of a valid channel_id or either not a global owner
or if token is invalid
'''
@pytest.mark.parametrize("invalid_token", ["Hello", "-1", -1, "35235gfdsgfdsh"])
# Testing case for when the token is invalid
def test_sendlater_invalid_token_AccessError(dummy_data, create_route, invalid_token):
    reset_call()

    reset_call()

    users_list = dummy_data.register_users(num_of_users=1)
    user0 = users_list[0]
    ch1 = requests.post(create_route, json={
        'token': user0["token"],
        'name': 'ch1',
        'is_public': True
    })
    assert ch1.status_code == 200
    ch1_dict = ch1.json()

    time = datetime.datetime.now().replace(microsecond=0) + datetime.timedelta(0, 5)
    time_sent = time.timestamp()
    message = "hello world bye world"
    
    response = message_sendlater_request(invalid_token, ch1_dict['channel_id'], message, time_sent)
    assert response.status_code == AccessError.code

# Testing case when authorised user is not a member of the valid channel_id
def test_sendlater_unauthorised_user_AccessError(dummy_data, create_route):
    reset_call()

    users_list = dummy_data.register_users(num_of_users=2)
    user0 = users_list[0]
    user1 = users_list[1]
    ch1 = requests.post(create_route, json={
        'token': user0["token"],
        'name': 'ch1',
        'is_public': True
    })
    assert ch1.status_code == 200
    ch1_dict = ch1.json()

    time = datetime.datetime.now().replace(microsecond=0) + datetime.timedelta(0, 5)
    time_sent = time.timestamp()
    message = "hello world bye world"

    response = message_sendlater_request(user1['token'], ch1_dict['channel_id'], message, time_sent)
    assert response.status_code == AccessError.code

################################# message_send_later_dm #################################

'''
InputError will occur when dm_id is not a valid
or the length of message is more than 1000 characters or time_sent is a time in the past.
'''
@pytest.mark.parametrize("invalid_dm_id", [-488445, -7474, -1, -49864864651651654])
# Testing case for when dm_id is invalid
def test_messages_sendlaterdm_invalid_dm_id_InputError(dummy_data, invalid_dm_id):
    reset_call()

    users_list = dummy_data.register_users(num_of_users=1)
    user0 = users_list[0]
    dummy_data.create_dm(user0['token'], [users_list[0]['auth_user_id']])

    message = "hello world"
    time = datetime.datetime.now().replace(microsecond=0) + datetime.timedelta(0, 5)
    time_sent = time.timestamp()

    response = message_sendlaterdm_request(user0['token'], invalid_dm_id, message, time_sent)
    assert response.status_code == InputError.code

def test_sendlaterdm_message_less_than_one_InputError(dummy_data):
    reset_call()

    users_list = dummy_data.register_users(num_of_users=1)
    user0 = users_list[0]
    dm_dict = dummy_data.create_dm(user0['token'], [users_list[0]['auth_user_id']])

    time = datetime.datetime.now().replace(microsecond=0) + datetime.timedelta(0, 5)
    time_sent = time.timestamp()
    message = ''

    response = message_sendlaterdm_request(user0['token'], dm_dict['dm_id'], message, time_sent)
    assert response.status_code == InputError.code

'''
InputError when message is more than 1000
'''
def test_sendlaterdm_message_more_than_thousand_InputError(dummy_data):
    reset_call()

    users_list = dummy_data.register_users(num_of_users=1)
    user0 = users_list[0]
    dm_dict = dummy_data.create_dm(user0['token'], [users_list[0]['auth_user_id']])

    time = datetime.datetime.now().replace(microsecond=0) + datetime.timedelta(0, 5)
    time_sent = time.timestamp()
    message = 'hello'*5000

    response = message_sendlaterdm_request(user0['token'], dm_dict['dm_id'], message, time_sent)
    assert response.status_code == InputError.code

def test_sendlaterdm_past_InputError(dummy_data):
    reset_call()

    users_list = dummy_data.register_users(num_of_users=1)
    user0 = users_list[0]
    dm_dict = dummy_data.create_dm(user0['token'], [users_list[0]['auth_user_id']])

    message = "hello world"
    time = datetime.datetime.now().replace(microsecond=0) - datetime.timedelta(0, 5)
    time_sent = time.timestamp()

    response = message_sendlaterdm_request(user0['token'], dm_dict['dm_id'], message, time_sent)
    assert response.status_code == InputError.code

'''
AccessError will occur when a user is not a member/owner of a valid channel_id or either not a global owner
or if token is invalid
'''
@pytest.mark.parametrize("invalid_token", ["Hello", "-1", -1, "35235gfdsgfdsh"])
# Testing case for when the token is invalid
def test_sendlaterdm_invalid_token_AccessError(dummy_data, create_route, invalid_token):
    reset_call()

    users_list = dummy_data.register_users(num_of_users=1)
    user0 = users_list[0]
    dm_dict = dummy_data.create_dm(user0['token'], [users_list[0]['auth_user_id']])

    time = datetime.datetime.now().replace(microsecond=0) + datetime.timedelta(0, 5)
    time_sent = time.timestamp()
    message = "hello world bye world"
    
    response = message_sendlaterdm_request(invalid_token, dm_dict['dm_id'], message, time_sent)
    assert response.status_code == AccessError.code

# Testing case when authorised user is not a member of the valid channel_id
def test_sendlaterdm_unauthorised_user_AccessError(dummy_data):
    reset_call()

    users_list = dummy_data.register_users(num_of_users=3)
    user0 = users_list[0]
    user1 = users_list[1]
    user2 = users_list[2]
    dm_dict = dummy_data.create_dm(user0['token'], [users_list[1]['auth_user_id']])

    time = datetime.datetime.now().replace(microsecond=0) + datetime.timedelta(0, 5)
    time_sent = time.timestamp()
    message = "hello world bye world"

    response = message_sendlaterdm_request(user2['token'], dm_dict['dm_id'], message, time_sent)
    assert response.status_code == AccessError.code

