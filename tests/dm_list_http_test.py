import requests
import pytest
from src.config import url
from tests.http_helpers import GenerateTestData

#====================== Helper functions / Fixtures ===============

def reset_call():
    requests.delete(url + 'clear/v1')

@pytest.fixture
def list_route():
    return url + '/dm/list/v1'

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

def test_invalid_token_type(list_route):
    reset_call()

    response = requests.get(list_route, json = {'token': '1'})
    assert response.status_code == 403

def test_invalid_token(list_route):
    reset_call()

    response = requests.get(list_route, json = {'token': 'asdfgvasdg'})
    assert response.status_code == 403

def test_no_dms(list_route, dummy_data):
    reset_call()
    
    user = dummy_data.register_users(num_of_users=1)
    users_return_dict1 = user[0]
    
    list1 = requests.get(list_route, json={
        'token': users_return_dict1['token'],
        'u_ids': [],
    })

    assert list1.status_code == 403
    
def test_dms_empty_uid_list(list_route, dummy_data, create_route):
    reset_call()
    
    user = dummy_data.register_users(num_of_users=3)
    users_return_dict1 = user[0]

    requests.post(create_route, json={
        'token': users_return_dict1['token'],
        'u_ids': [],
    })
    
    list1 = requests.get(list_route, params={
        'token': users_return_dict1['token']
    })

    assert list1.status_code == 200
    assert list1.json() == {'dms': [{'dm_id': 0, 'name': ''}]}
    
def test_dms_one_uid(list_route, dummy_data, create_route):
    reset_call()
    
    user = dummy_data.register_users(num_of_users=2)
    users_return_dict1 = user[0]
    users_return_dict2 = user[1]
    
    requests.post(create_route, json={
        'token': users_return_dict1['token'],
        'u_ids': [users_return_dict2['auth_user_id']],
    })
    list1 = requests.get(list_route, params={
        'token': users_return_dict1['token']
    })

    assert list1.status_code == 200
    assert list1.json() == {'dms': [{'dm_id': 0, 'name': 'testfirst1testlast1'}]}


def test_dms_two_uids(list_route, dummy_data, create_route):
    reset_call()
    
    user = dummy_data.register_users(num_of_users=3)
    users_return_dict1 = user[0]
    users_return_dict2 = user[1]
    users_return_dict3 = user[2]

    requests.post(create_route, json={
        'token': users_return_dict1['token'],
        'u_ids': [users_return_dict2['auth_user_id'], users_return_dict3['auth_user_id']],
    })
    
    list1 = requests.get(list_route, params={
        'token': users_return_dict1['token']
    })

    assert list1.status_code == 200
    assert list1.json() == {'dms': [{'dm_id': 0, 'name': 'testfirst1testlast1, testfirst2testlast2'}]}
