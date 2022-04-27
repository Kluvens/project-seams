import requests
import pytest
from src.config import url
from tests.http_helpers import GenerateTestData
from src.error import InputError, AccessError
import time
import random
import string
from datetime import datetime, timedelta

#====================== Helper functions / Fixtures ===============

OKAY = 200

def reset_call():
    requests.delete(url + 'clear/v1')

def start_request(token, channel_id, length):
    return requests.post(url + '/standup/start/v1', json={
        'token': token,
        'channel_id': channel_id,
        'length': length,
    })
def active_request(token, channel_id):
    return requests.get(url + '/standup/active/v1', params={
        'token': token,
        'channel_id': channel_id,
    })
def send_request(token, channel_id, message):
    return requests.post(url + '/standup/send/v1', json={
        'token': token,
        'channel_id': channel_id,
        'message': message,
    })
def create_request(token):
    return requests.post(url + "channels/create/v2", json={
        'token': token,
        'name': 'ch1',
        'is_public': True,
    })
def print_over_1000():
    letters = string.ascii_letters
    return (''.join(random.choice(letters) for i in range(1002)))

@pytest.fixture
def logout():
    return url + "auth/logout/v1"
#======================== Error Testing ============================
def test_start_no_channel(dummy_data):
    reset_call()

    user = dummy_data.register_users(num_of_users=1)
    users_return_dict = user[0]

    start = start_request(
        users_return_dict['token'], 
        0, 
        5,
    )
    assert start.status_code == InputError.code

def test_start_negative_length(dummy_data):
    reset_call()

    user = dummy_data.register_users(num_of_users=1)
    users_return_dict = user[0]

    ch1 = create_request(users_return_dict['token'])

    start = start_request(
        users_return_dict['token'], 
        ch1.json()['channel_id'], 
        -1,
    )
    assert start.status_code == InputError.code

def test_two_standups(dummy_data):
    reset_call()

    user = dummy_data.register_users(num_of_users=2)
    users_return_dict = user[0]
    users_return_dict1 = user[1]

    ch1 = create_request(users_return_dict['token'])

    start_request(
        users_return_dict['token'], 
        ch1.json()['channel_id'], 
        5,
    )
    start = start_request(
        users_return_dict1['token'], 
        ch1.json()['channel_id'], 
        5,
    )
    assert start.status_code == InputError.code

def test_user_not_in_channel(dummy_data):
    reset_call()

    user = dummy_data.register_users(num_of_users=2)
    users_return_dict = user[0]
    users_return_dict1 = user[1]

    ch1 = create_request(users_return_dict['token'])

    start = start_request(
        users_return_dict1['token'], 
        ch1.json()['channel_id'], 
        5,
    )
    assert start.status_code == AccessError.code

def test_active_invalid_channel(dummy_data):
    reset_call()

    user = dummy_data.register_users(num_of_users=1)
    users_return_dict = user[0]

    active = active_request(users_return_dict['token'], 0)

    assert active.status_code == InputError.code

def test_send_invalid_channel(dummy_data):
    reset_call()

    user = dummy_data.register_users(num_of_users=1)
    users_return_dict = user[0]

    send = send_request(
        users_return_dict['token'], 
        0, 
        'hello',
    )
    assert send.status_code == InputError.code

def test_send_invalid_standup(dummy_data):
    reset_call()

    user = dummy_data.register_users(num_of_users=1)
    users_return_dict = user[0]

    ch1 = create_request(users_return_dict['token'])

    send = send_request(
        users_return_dict['token'], 
        ch1.json()['channel_id'], 
        'hello',
    )
    assert send.status_code == InputError.code

def test_user_not_in_channel_send(dummy_data):
    reset_call()

    user = dummy_data.register_users(num_of_users=2)
    users_return_dict = user[0]
    users_return_dict1 = user[1]

    ch1 = create_request(users_return_dict['token'])

    start_request(
        users_return_dict['token'], 
        ch1.json()['channel_id'], 
        5,
    )
    send = send_request(
        users_return_dict1['token'], 
        ch1.json()['channel_id'], 
        'hello',
    )
    assert send.status_code == AccessError.code

def test_user_not_in_channel_active(dummy_data):
    reset_call()

    user = dummy_data.register_users(num_of_users=2)
    users_return_dict = user[0]
    users_return_dict1 = user[1]
    
    ch1 = create_request(users_return_dict['token'])

    start_request(
        users_return_dict['token'], 
        ch1.json()['channel_id'], 
        5,
    )
    active = active_request(
        users_return_dict1['token'], 
        ch1.json()['channel_id'],
    )
    assert active.status_code == AccessError.code

def test_send_over_1000(dummy_data):
    reset_call()

    user = dummy_data.register_users(num_of_users=1)
    users_return_dict = user[0]
    
    ch1 = create_request(users_return_dict['token'])
    
    start_request(
        users_return_dict['token'], 
        ch1.json()['channel_id'], 
        5,
    )
    send = send_request(
        users_return_dict['token'], 
        ch1.json()['channel_id'], 
        print_over_1000(),
    )
    assert send.status_code == InputError.code

def test_active_invalid_token(dummy_data, logout):
    reset_call()

    user = dummy_data.register_users(num_of_users=1)
    users_return_dict = user[0]
    
    ch1 = create_request(users_return_dict['token'])
    
    start_request(
        users_return_dict['token'], 
        ch1.json()['channel_id'], 
        5,
    )
    requests.post(logout, json={"token" : users_return_dict["token"]})
    active = active_request(
        users_return_dict["token"], 
        ch1.json()['channel_id'],
    )
    assert active.status_code == AccessError.code

def test_send_invalid_token(dummy_data, logout):
    reset_call()

    user = dummy_data.register_users(num_of_users=1)
    users_return_dict = user[0]
    
    ch1 = create_request(users_return_dict['token'])
    
    start_request(
        users_return_dict['token'], 
        ch1.json()['channel_id'], 
        5,
    ) 
    requests.post(logout, json={"token" : users_return_dict["token"]})

    send = send_request(
        users_return_dict['token'], 
        ch1.json()['channel_id'], 
        'hello',
    )
    assert send.status_code == AccessError.code

def test_start_invalid_token(dummy_data, logout):
    reset_call()

    user = dummy_data.register_users(num_of_users=1)
    users_return_dict = user[0]
    
    ch1 = create_request(users_return_dict['token'])
    
    requests.post(logout, json={"token" : users_return_dict["token"]})

    start = start_request(
        users_return_dict['token'], 
        ch1.json()['channel_id'], 
        5,
    ) 
    assert start.status_code == AccessError.code
#=========================== Testing ===============================

def test_active_standup(dummy_data):
    reset_call()
    
    user = dummy_data.register_users(num_of_users=1)
    users_return_dict = user[0]
    
    ch1 = create_request(users_return_dict['token'])

    start_request(
        users_return_dict['token'], 
        ch1.json()['channel_id'], 
        5,
    )
    active = active_request(
        users_return_dict['token'], 
        ch1.json()['channel_id'],
    )
    assert active.status_code == OKAY
    assert active.json()['is_active'] == True

def test_not_active_standup_empty_message(dummy_data):
    reset_call()
    
    user = dummy_data.register_users(num_of_users=1)
    users_return_dict = user[0]
    
    ch1 = create_request(users_return_dict['token'])

    start_request(
        users_return_dict['token'], 
        ch1.json()['channel_id'], 
        0.1,
    )
    time.sleep(1)
    active = active_request(
        users_return_dict['token'], 
        ch1.json()['channel_id'],
    )

    assert active.status_code == OKAY
    assert active.json() == {'is_active': False, 'time_finish': None}

def test_not_active_standup_message(dummy_data):
    reset_call()
    
    user = dummy_data.register_users(num_of_users=1)
    users_return_dict = user[0]
    
    ch1 = create_request(users_return_dict['token'])

    start_request(
        users_return_dict['token'], 
        ch1.json()['channel_id'], 
        0.1,
    )
    send_request(
        users_return_dict['token'], 
        ch1.json()['channel_id'], 
        'hello',
    )
    time.sleep(1)
    active = active_request(
        users_return_dict['token'], 
        ch1.json()['channel_id'],
    )

    assert active.status_code == OKAY
    assert active.json() == {'is_active': False, 'time_finish': None}

def test_no_standup(dummy_data):
    reset_call()
    
    user = dummy_data.register_users(num_of_users=1)
    users_return_dict = user[0]
    
    ch1 = create_request(users_return_dict['token'])

    active = active_request(
        users_return_dict['token'], 
        ch1.json()['channel_id'],
    )

    assert active.status_code == OKAY
    assert active.json() == {'is_active': False, 'time_finish': None}

def test_start_standup(dummy_data):
    reset_call()
    
    user = dummy_data.register_users(num_of_users=1)
    users_return_dict = user[0]
    
    ch1 = create_request(users_return_dict['token'])
    start = start_request(
        users_return_dict['token'], 
        ch1.json()['channel_id'], 
        5,
    )
    assert start.status_code == OKAY
    assert start.json()['time_finish'] - (datetime.now()+timedelta(seconds=5)).timestamp() < 1

def test_send_standup(dummy_data):
    reset_call()

    user = dummy_data.register_users(num_of_users=1)
    users_return_dict = user[0]
    
    ch1 = create_request(users_return_dict['token'])
    start_request(
        users_return_dict['token'], 
        ch1.json()['channel_id'], 
        5,
    )
    send = send_request(
        users_return_dict['token'], 
        ch1.json()['channel_id'], 
        'hello',
    )
    assert send.status_code == OKAY
    assert send.json() == {}

def test_multiple_active_requests(dummy_data):
    reset_call()
    
    user = dummy_data.register_users(num_of_users=1)
    users_return_dict = user[0]
    
    ch1 = create_request(users_return_dict['token'])
    start_request(
        users_return_dict['token'], 
        ch1.json()['channel_id'], 
        0.1,
    )
    time.sleep(1)
    active_request(
        users_return_dict['token'], 
        ch1.json()['channel_id'],
    )
    active2 = active_request(
        users_return_dict['token'], 
        ch1.json()['channel_id'],
    )
    assert active2.status_code == OKAY
    assert active2.json()['is_active'] == False