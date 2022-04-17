import requests
import pytest
from src.config import url
from tests.http_helpers import GenerateTestData
from src.error import InputError, AccessError
import time
from datetime import datetime, timedelta
from src.data_store import data_store

#====================== Helper functions / Fixtures ===============

OKAY = 200

def reset_call():
    requests.delete(url + 'clear/v1')

@pytest.fixture
def start():
    return url + '/standup/start/v1'

@pytest.fixture
def active():
    return url + '/standup/active/v1'

@pytest.fixture
def send():
    return url + '/standup/send/v1'

@pytest.fixture
def create_route():
    return url + "channels/create/v2"

@pytest.fixture()
def dummy_data():
    data_instance = GenerateTestData(url)
    return data_instance

#======================== Error Testing ============================
def test_start_no_channel(dummy_data, start):
    reset_call()

    user = dummy_data.register_users(num_of_users=1)
    users_return_dict = user[0]

    start = requests.post(start, json={
        'token': users_return_dict['token'],
        'channel_id': 0,
        'length': 5,
    }) 
    assert start.status_code == InputError.code

def test_start_negative_length(create_route, dummy_data, start):
    reset_call()

    user = dummy_data.register_users(num_of_users=1)
    users_return_dict = user[0]

    ch1 = requests.post(create_route, json={
        'token': users_return_dict['token'],
        'name': 'ch1',
        'is_public': True
    })
    start = requests.post(start, json={
        'token': users_return_dict['token'],
        'channel_id': ch1.json()['channel_id'],
        'length': -1,
    }) 
    assert start.status_code == InputError.code

def test_two_active_standups(create_route, dummy_data, start):
    reset_call()

    user = dummy_data.register_users(num_of_users=2)
    users_return_dict = user[0]
    users_return_dict1 = user[1]

    ch1 = requests.post(create_route, json={
        'token': users_return_dict['token'],
        'name': 'ch1',
        'is_public': True
    })
    requests.post(start, json={
        'token': users_return_dict['token'],
        'channel_id': ch1.json()['channel_id'],
        'length': 5,
    })
    start = requests.post(start, json={
        'token': users_return_dict1['token'],
        'channel_id': ch1.json()['channel_id'],
        'length': 5,
    }) 
    assert start.status_code == InputError.code

def test_user_not_in_channel(create_route, dummy_data, start):
    reset_call()

    user = dummy_data.register_users(num_of_users=1)
    users_return_dict = user[0]
    ch1 = requests.post(create_route, json={
        'token': users_return_dict['token'],
        'name': 'ch1',
        'is_public': True
    })
    start = requests.post(start, json={
        'token': 'saiodifjoasdjfio',
        'channel_id': ch1.json()['channel_id'],
        'length': 5,
    }) 
    assert start.status_code == AccessError.code

def test_active_invalid_channel(dummy_data, active):
    reset_call()

    user = dummy_data.register_users(num_of_users=1)
    users_return_dict = user[0]

    active = requests.get(active, params = {
        'token': users_return_dict['token'],
        'channel_id': 0,
    })
    assert active.status_code == InputError.code

def test_send_invalid_channel(dummy_data, send):
    reset_call()

    user = dummy_data.register_users(num_of_users=1)
    users_return_dict = user[0]

    send = requests.post(send, json={
        'token': users_return_dict['token'],
        'channel_id': 0,
        'message': 'hello',
    })
    assert send.status_code == InputError.code

def test_send_invalid_standup(create_route, dummy_data, send):
    reset_call()

    user = dummy_data.register_users(num_of_users=1)
    users_return_dict = user[0]

    ch1 = requests.post(create_route, json={
        'token': users_return_dict['token'],
        'name': 'ch1',
        'is_public': True
    })
    send = requests.post(send, json={
        'token': users_return_dict['token'],
        'channel_id': ch1.json()['channel_id'],
        'message': 'hello',
    })
    assert send.status_code == InputError.code

def test_user_not_in_channel_send(create_route, dummy_data, send, start):
    reset_call()

    user = dummy_data.register_users(num_of_users=1)
    users_return_dict = user[0]
    ch1 = requests.post(create_route, json={
        'token': users_return_dict['token'],
        'name': 'ch1',
        'is_public': True
    })
    requests.post(start, json={
        'token': users_return_dict['token'],
        'channel_id': ch1.json()['channel_id'],
        'length': 0.1,
    }) 
    send = requests.post(send, json={
        'token': 'saiodifjoasdjfio',
        'channel_id': ch1.json()['channel_id'],
        'message': 'hello',
    }) 
    assert send.status_code == AccessError.code

def test_user_not_in_channel_active(create_route, dummy_data, active, start):
    reset_call()

    user = dummy_data.register_users(num_of_users=1)
    users_return_dict = user[0]
    
    ch1 = requests.post(create_route, json={
        'token': users_return_dict['token'],
        'name': 'ch1',
        'is_public': True
    })
    requests.post(start, json={
        'token': users_return_dict['token'],
        'channel_id': ch1.json()['channel_id'],
        'length': 5,
    }) 
    active = requests.get(active, params = {
        'token': 'ASDFASDF',
        'channel_id': ch1.json()['channel_id'],
    })
    assert active.status_code == AccessError.code

#=========================== Testing ===============================

def test_active_standup(create_route, dummy_data, active, start):
    reset_call()
    
    user = dummy_data.register_users(num_of_users=1)
    users_return_dict = user[0]
    
    ch1 = requests.post(create_route, json={
        'token': users_return_dict['token'],
        'name': 'ch1',
        'is_public': True
    })
    requests.post(start, json={
        'token': users_return_dict['token'],
        'channel_id': ch1.json()['channel_id'],
        'length': 5,
    }) 
    active = requests.get(active, params = {
        'token': users_return_dict['token'],
        'channel_id': ch1.json()['channel_id'],
    })
    assert active.status_code == OKAY
    assert active.json()['is_active'] == True

def test_not_active_standup_empty_message(create_route, dummy_data, active, start):
    reset_call()
    
    user = dummy_data.register_users(num_of_users=1)
    users_return_dict = user[0]
    
    ch1 = requests.post(create_route, json={
        'token': users_return_dict['token'],
        'name': 'ch1',
        'is_public': True
    })
    requests.post(start, json={
        'token': users_return_dict['token'],
        'channel_id': ch1.json()['channel_id'],
        'length': 0.1,
    }) 
    time.sleep(1)
    active = requests.get(active, params = {
        'token': users_return_dict['token'],
        'channel_id': ch1.json()['channel_id'],
    })

    assert active.status_code == OKAY
    assert active.json() == {'is_active': False, 'time_finish': None}

def test_not_active_standup_message(create_route, dummy_data, active, start, send):
    reset_call()
    
    user = dummy_data.register_users(num_of_users=1)
    users_return_dict = user[0]
    
    ch1 = requests.post(create_route, json={
        'token': users_return_dict['token'],
        'name': 'ch1',
        'is_public': True
    })
    requests.post(start, json={
        'token': users_return_dict['token'],
        'channel_id': ch1.json()['channel_id'],
        'length': 0.1,
    }) 
    requests.post(send, json={
        'token': users_return_dict['token'],
        'channel_id': ch1.json()['channel_id'],
        'message': 'hello',
    })
    time.sleep(1)
    active = requests.get(active, params = {
        'token': users_return_dict['token'],
        'channel_id': ch1.json()['channel_id'],
    })

    assert active.status_code == OKAY
    assert active.json() == {'is_active': False, 'time_finish': None}

def test_no_standup(create_route, dummy_data, active):
    reset_call()
    
    user = dummy_data.register_users(num_of_users=1)
    users_return_dict = user[0]
    
    ch1 = requests.post(create_route, json={
        'token': users_return_dict['token'],
        'name': 'ch1',
        'is_public': True
    })

    active = requests.get(active, params = {
        'token': users_return_dict['token'],
        'channel_id': ch1.json()['channel_id'],
    })

    assert active.status_code == OKAY
    assert active.json() == {'is_active': False, 'time_finish': None}

def test_start_standup(create_route, dummy_data, start):
    reset_call()
    
    user = dummy_data.register_users(num_of_users=1)
    users_return_dict = user[0]
    
    ch1 = requests.post(create_route, json={
        'token': users_return_dict['token'],
        'name': 'ch1',
        'is_public': True
    })
    start = requests.post(start, json={
        'token': users_return_dict['token'],
        'channel_id': ch1.json()['channel_id'],
        'length': 5,
    }) 
    assert start.status_code == OKAY
    assert start.json()['time_finish'] - (datetime.now()+timedelta(seconds=5)).timestamp() < 1

def test_send_standup(create_route, dummy_data, start, send):
    reset_call()

    user = dummy_data.register_users(num_of_users=1)
    users_return_dict = user[0]
    
    ch1 = requests.post(create_route, json={
        'token': users_return_dict['token'],
        'name': 'ch1',
        'is_public': True
    })
    start = requests.post(start, json={
        'token': users_return_dict['token'],
        'channel_id': ch1.json()['channel_id'],
        'length': 0.1,
    }) 
    send = requests.post(send, json={
        'token': users_return_dict['token'],
        'channel_id': ch1.json()['channel_id'],
        'message': 'hello',
    })
    assert start.status_code == OKAY
    assert send.json() == {}

def test_send_standup(create_route, dummy_data, start, send):
    reset_call()

    user = dummy_data.register_users(num_of_users=1)
    users_return_dict = user[0]
    
    ch1 = requests.post(create_route, json={
        'token': users_return_dict['token'],
        'name': 'ch1',
        'is_public': True
    })
    start = requests.post(start, json={
        'token': users_return_dict['token'],
        'channel_id': ch1.json()['channel_id'],
        'length': 0.1,
    }) 
    send = requests.post(send, json={
        'token': users_return_dict['token'],
        'channel_id': ch1.json()['channel_id'],
        'message': 'hello',
    })
    assert start.status_code == OKAY
    assert send.json() == {}