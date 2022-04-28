import requests
import pytest
from src.config import url
from tests.http_helpers import GenerateTestData
from src.error import AccessError, InputError

#====================== Helper functions / Fixtures ===============
OKAY = 200

def reset_call():
    requests.delete(url + 'clear/v1')

@pytest.fixture
def listall_route():
    return url + 'channels/listall/v2'

@pytest.fixture
def create_route():
    return url + "channels/create/v2"

@pytest.fixture
def leave_route():
    return url + 'channel/leave/v1'

@pytest.fixture()
def dummy_data():
    data_instance = GenerateTestData(url)
    return data_instance

@pytest.fixture
def register_test_users(num_of_users):
    dummy_data = GenerateTestData(url)
    dummy_data.register_users(num_of_users)

# ===================== HTTP TESTS =====================================

# invalid token
def test_invalid_token(leave_route, create_route, dummy_data):
    reset_call()

    user = dummy_data.register_users(num_of_users=1)[0]['token']

    channel_id_obj = requests.post(create_route, json = {
        'token':user,
        'name': 'hello I am a channel',
        'is_public':True,
    })
    channel_info = channel_id_obj.json()
    channel_id = channel_info['channel_id']

    response = requests.post(
        leave_route, 
        json = {'token': 'hello am not a token', 'channel_id': channel_id})
    assert response.status_code == AccessError.code

# invalid channel_id
def test_invalid_channel_id(create_route,leave_route,dummy_data):
    reset_call()

    user = dummy_data.register_users(num_of_users=1)[0]['token']

    channel_id_obj = requests.post(create_route, json = {
        'token':user,
        'name': 'hello I am a channel',
        'is_public':True,
    })
    channel_info = channel_id_obj.json()
    channel_id = channel_info['channel_id']

    response = requests.post(leave_route, json = {
        'token':user,
        'channel_id': channel_id+1000
    })
    assert response.status_code == InputError.code

# authorized user not a member of the channel
def test_not_user_in_channel(create_route,leave_route,dummy_data):
    reset_call()

    user = dummy_data.register_users(num_of_users=1)[0]['token']

    channel_id_obj = requests.post(create_route, json = {
        'token':user,
        'name': 'hello I am a channel',
        'is_public':True,
    })
    channel_info = channel_id_obj.json()
    channel_id = channel_info['channel_id']

    response = requests.post(leave_route, json = {
        'token': 'i am not from this channel',
        'channel_id': channel_id
    })
    assert response.status_code == AccessError.code

# routine behavior
def test_working_setup(create_route,leave_route,dummy_data):
    reset_call()

    user = dummy_data.register_users(num_of_users=1)[0]['token']

    channel_id_obj = requests.post(create_route, json = {
        'token':user,
        'name': 'hello I am a channel',
        'is_public':True,
    })
    channel_info = channel_id_obj.json()
    channel_id = channel_info['channel_id']

    response = requests.post(leave_route, json = {
        'token': user,
        'channel_id': channel_id
    })
    assert response.status_code == OKAY
