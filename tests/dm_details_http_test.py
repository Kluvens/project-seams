import requests
import pytest
from src.config import url
from tests.http_helpers import GenerateTestData

#====================== Helper functions / Fixtures ===============

def reset_call():
    requests.delete(url + 'clear/v1')

@pytest.fixture
def detail_route():
    return url + '/dm/details/v1'

@pytest.fixture
def create_route():
    return url + '/dm/create/v1'

@pytest.fixture()
def dummy_data():
    data_instance = GenerateTestData(url)
    return data_instance

@pytest.fixture
def register_test_users(num_of_users):
    dummy_data = GenerateTestData(url)
    dummy_data.register_users(num_of_users)

#======================= Testing  =================================
def test_dms_no_uid(detail_route, dummy_data, create_route):
    reset_call()
    
    user = dummy_data.register_users(num_of_users=3)
    users_return_dict1 = user[0]
    
    requests.post(create_route, json={
        'token': users_return_dict1['token'],
        'u_ids': [],
    })
    
    detail1 = requests.get(detail_route, params={
        'token': users_return_dict1['token'],
        'dm_id': 0,
    })

    assert detail1.status_code == 200
    assert detail1.json() == {           
        'name': 'jakerenzella',
        'members': [{'email': 'owner@seams.com',
                    'handle_str': 'jakerenzella',
                    'name_first': 'Jake',
                    'name_last': 'Renzella',
                    'u_id': 0}],
    }

def test_dms_one_uid(detail_route, dummy_data, create_route):
    reset_call()
    
    user = dummy_data.register_users(num_of_users=3)
    users_return_dict1 = user[0]
    users_return_dict2 = user[1]
    
    requests.post(create_route, json={
        'token': users_return_dict1['token'],
        'u_ids': [users_return_dict2['auth_user_id']],
    })
    
    detail1 = requests.get(detail_route, params={
        'token': users_return_dict1['token'],
        'dm_id': 0,
    })

    assert detail1.status_code == 200
    assert detail1.json() == {
        'name': 'jakerenzella, testfirst1testlast1',
        'members': [{'email': 'owner@seams.com',
                    'handle_str': 'jakerenzella',
                    'name_first': 'Jake',
                    'name_last': 'Renzella',
                    'u_id': 0},
                    {'email': 'dummy1@seams.com',
                    'handle_str': 'testfirst1testlast1',
                    'name_first': 'testfirst1',
                    'name_last': 'testlast1',
                    'u_id': 1}],
        }

def test_dms_two_uid(detail_route, dummy_data, create_route):
    reset_call()
    
    user = dummy_data.register_users(num_of_users=3)
    users_return_dict1 = user[0]
    users_return_dict2 = user[1]
    users_return_dict3 = user[2]
    
    requests.post(create_route, json={
        'token': users_return_dict1['token'],
        'u_ids': [users_return_dict2['auth_user_id'], users_return_dict3['auth_user_id']],
    })
    
    detail1 = requests.get(detail_route, params={
        'token': users_return_dict1['token'],
        'dm_id': 0,
    })

    assert detail1.status_code == 200
    assert detail1.json() == {
        'name': 'jakerenzella, testfirst1testlast1, testfirst2testlast2',
        'members': [{'email': 'owner@seams.com',
                    'handle_str': 'jakerenzella',
                    'name_first': 'Jake',
                    'name_last': 'Renzella',
                    'u_id': 0},
                    {'email': 'dummy1@seams.com',
                    'handle_str': 'testfirst1testlast1',
                    'name_first': 'testfirst1',
                    'name_last': 'testlast1',
                    'u_id': 1},
                    {'email': 'dummy2@seams.com',
                    'handle_str': 'testfirst2testlast2',
                    'name_first': 'testfirst2',
                    'name_last': 'testlast2',
                    'u_id': 2}],
        }

def test_two_dms(detail_route, dummy_data, create_route):
    reset_call()
    
    user = dummy_data.register_users(num_of_users=3)
    users_return_dict1 = user[0]
    users_return_dict2 = user[1]
    
    requests.post(create_route, json={
        'token': users_return_dict1['token'],
        'u_ids': [],
    })
    requests.post(create_route, json={
        'token': users_return_dict2['token'],
        'u_ids': [users_return_dict1['auth_user_id']],
    })  
    detail1 = requests.get(detail_route, params={
        'token': users_return_dict1['token'],
        'dm_id': 0,
    })
    assert detail1.status_code == 200
    assert detail1.json() == {
        'name': 'jakerenzella',
        'members': [{'email': 'owner@seams.com',
                    'handle_str': 'jakerenzella',
                    'name_first': 'Jake',
                    'name_last': 'Renzella',
                    'u_id': 0}],
    }
