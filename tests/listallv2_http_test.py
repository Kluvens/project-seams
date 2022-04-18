import requests
import pytest
from src.config import url
from tests.http_helpers import GenerateTestData
from src.error import AccessError
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

#======================= Testing  =================================

def test_invalid_token_type(listall_route):
    reset_call()

    response = requests.get(listall_route, params = {'token': '1'})
    assert response.status_code == AccessError.code

def test_invalid_token(listall_route):
    reset_call()

    response = requests.get(listall_route, params = {'token': 'asdfgvasdg'})
    assert response.status_code == AccessError.code

def test_listall_public_and_private(listall_route, create_route, dummy_data):
    reset_call()
    
    user = dummy_data.register_users(num_of_users=2)
    users_return_dict1 = user[0]
    users_return_dict2 = user[1]
    
    ch1 = requests.post(create_route, json={
        'token': users_return_dict1['token'],
        'name': 'ch1',
        'is_public': False
    })

    ch2 = requests.post(create_route, json={
        'token': users_return_dict2['token'],
        'name': 'ch2',
        'is_public': True
    })

    list1 = requests.get(listall_route, params={
        'token': users_return_dict1['token']
    })

    assert list1.status_code == OKAY
    assert list1.json() == {
        'channels': [{'channel_id': ch1.json()['channel_id'], 'name': 'ch1'}, 
                    {'channel_id': ch2.json()['channel_id'], 'name': 'ch2'}]
    }

def test_listall_no_channels(listall_route, dummy_data):
    reset_call()
    
    user = dummy_data.register_users(num_of_users=1)
    users_return_dict = user[0]
    
    list1 = requests.get(listall_route, params={
        'token': users_return_dict['token']
    })

    assert list1.status_code == OKAY
    assert list1.json() == {'channels': []}

def test_multiple_users_and_channels(listall_route, create_route, dummy_data):
    reset_call()
    
    user = dummy_data.register_users(num_of_users=2)
    users_return_dict1 = user[0]
    users_return_dict2 = user[1]
    
    ch1 = requests.post(create_route, json={
        'token': users_return_dict1['token'],
        'name': 'ch1',
        'is_public': False
    })

    ch2 = requests.post(create_route, json={
        'token': users_return_dict1['token'],
        'name': 'ch2',
        'is_public': True
    })

    ch3 = requests.post(create_route, json={
        'token': users_return_dict2['token'],
        'name': 'ch3',
        'is_public': True
    })

    list1 = requests.get(listall_route, params={
        'token': users_return_dict1['token']
    })

    assert list1.status_code == OKAY
    assert list1.json() == {
        'channels': [{'channel_id': ch1.json()["channel_id"], 'name': 'ch1'},
                    {'channel_id': ch2.json()["channel_id"], 'name': 'ch2'},
                    {'channel_id': ch3.json()["channel_id"], 'name': 'ch3'}]
    }

