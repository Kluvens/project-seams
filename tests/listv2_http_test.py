import requests
import pytest
from src.config import url
from tests.http_helpers import GenerateTestData

#====================== Helper functions / Fixtures ===============

def reset_call():
    requests.delete(url + 'clear/v1')

@pytest.fixture
def list_route():
    return url + 'channels/list/v2'

@pytest.fixture
def create_route():
    return url + "channels/create/v2"

@pytest.fixture()
def dummy_data():
    data_instance = GenerateTestData(url)
    return data_instance

@pytest.fixture
def register_test_users(num_of_users):
    dummy_data = GenerateTestData(url)
    dummy_data.register_users(num_of_users)

#======================= Testing  =================================

def test_invalid_token_type(list_route):
    reset_call()

    response = requests.get(list_route, params = {'token': '1'})
    assert response.status_code == 403

def test_invalid_token(list_route):
    reset_call()

    response = requests.get(list_route, params = {'token': 'asdfgvasdg'})
    assert response.status_code == 403
        

def test_list_user_join_channel_public(list_route, create_route, dummy_data):
    reset_call()
    
    user = dummy_data.register_users(num_of_users=1)
    users_return_dict = user[0]
    
    ch1 = requests.post(create_route, json={
        'token': users_return_dict['token'],
        'name': 'ch1',
        'is_public': True
    })
    
    list1 = requests.get(list_route, params={
        'token': users_return_dict['token']
    })

    assert list1.status_code == 200
    assert list1.json() == {'channels': [{'channel_id': ch1.json()['channel_id'], 'name': 'ch1'}]}

def test_list_user_join_channel_private(list_route, create_route, dummy_data):
    reset_call()
    
    user = dummy_data.register_users(num_of_users=1)
    users_return_dict = user[0]
    
    ch1 = requests.post(create_route, json={
        'token': users_return_dict['token'],
        'name': 'ch1',
        'is_public': False
    })
    
    list1 = requests.get(list_route, params={
        'token': users_return_dict['token']
    })

    assert list1.status_code == 200
    assert list1.json() == {'channels': [{'channel_id': ch1.json()['channel_id'], 'name': 'ch1'}]}

def test_list_user_join_no_channel(list_route, dummy_data):
    reset_call()
    
    user = dummy_data.register_users(num_of_users=1)
    users_return_dict = user[0]
    
    list1 = requests.get(list_route, params={
        'token': users_return_dict['token']
    })

    assert list1.status_code == 200
    assert list1.json() == {'channels': []}

def test_list_user_some_channels(list_route, create_route, dummy_data):
    reset_call()
    
    user = dummy_data.register_users(num_of_users=2)
    users_return_dict1 = user[0]
    users_return_dict2 = user[1]
    
    ch1 = requests.post(create_route, json={
        'token': users_return_dict1['token'],
        'name': 'ch1',
        'is_public': False
    })

    requests.post(create_route, json={
        'token': users_return_dict2['token'],
        'name': 'ch2',
        'is_public': True
    })
    
    list1 = requests.get(list_route, params={
        'token': users_return_dict1['token']
    })

    assert list1.status_code == 200
    assert list1.json() == {'channels': [{'channel_id': ch1.json()['channel_id'], 'name': 'ch1'}]}

def test_list_user_multiple_channels(list_route, create_route, dummy_data):
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

    requests.post(create_route, json={
        'token': users_return_dict2['token'],
        'name': 'ch3',
        'is_public': True
    })
    
    list1 = requests.get(list_route, params={
        'token': users_return_dict1['token']
    })

    assert list1.status_code == 200
    assert list1.json() == {'channels': [{'channel_id': ch1.json()['channel_id'], 'name': 'ch1'}, 
                                        {'channel_id': ch2.json()['channel_id'], 'name': 'ch2'}]}
