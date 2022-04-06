from os import remove
import requests
import pytest
from src.config import url
from tests.http_helpers import GenerateTestData
from src.error import InputError, AccessError

# ================ helper functions =====================================

def reset_call():
    requests.delete(url + 'clear/v1')

@pytest.fixture
def create_route():
    return url + 'dm/create/v1'

@pytest.fixture()
def dummy_data():
    data_instance = GenerateTestData(url)
    return data_instance

@pytest.fixture
def register_test_users(num_of_users):
    dummy_data = GenerateTestData(url)
    dummy_data.register_users(num_of_users)

@pytest.fixture()
def remove_route():
    return url + 'dm/remove/v1'

@pytest.fixture()
def leave_route():
    return url + 'dm/leave/v1'
    
# ================================= HTTP TESTS ==============================================

# invalid token
def test_invalid_token(remove_route,create_route,dummy_data):
    reset_call()

    users = dummy_data.register_users(num_of_users=2)
    owner = users[0]['token']
    u_ids = [users[1]['auth_user_id']]

    dm_id_obj = requests.post(create_route, json={
        'token': owner,
        'u_ids': u_ids,
    })
    dm_info = dm_id_obj.json()
    dm_id = dm_info['dm_id']

    response = requests.delete(remove_route, json = {
        'token': 'invalidtoken',
        'dm_id': dm_id,
    })
    assert response.status_code == AccessError.code

# dm_id is not valid
def test_invalid_dm_id(create_route,remove_route,dummy_data):
    reset_call()

    users = dummy_data.register_users(num_of_users=2)
    owner = users[0]['token']
    u_ids = [users[1]['auth_user_id']]

    dm_id_obj = requests.post(create_route, json={
        'token': owner,
        'u_ids': u_ids,
    })
    dm_info = dm_id_obj.json()
    dm_id = dm_info['dm_id']

    response = requests.delete(remove_route, json = {
        'token': owner,
        'dm_id': dm_id+100,
    })
    assert response.status_code == 400

# authorised user is not original dm creator/owner
def test_not_owner_remove(create_route,remove_route,dummy_data):
    reset_call()

    users = dummy_data.register_users(num_of_users=3)
    owner = users[0]['token']
    u_ids = [users[1]['auth_user_id'], users[2]['auth_user_id']]
    other = users[1]['token']

    dm_id_obj = requests.post(create_route, json={
        'token': owner,
        'u_ids': u_ids,
    })
    dm_info = dm_id_obj.json()
    dm_id = dm_info['dm_id']

    response = requests.delete(remove_route, json = {
        'token': other,
        'dm_id': dm_id,
    })
    assert response.status_code == AccessError.code

# authorised user is no longer in dm
def test_owner_not_in_dm(create_route,remove_route,dummy_data,leave_route):
    reset_call()

    users = dummy_data.register_users(num_of_users=3)
    owner = users[0]['token']
    u_ids = [users[1]['auth_user_id'], users[2]['auth_user_id']]

    dm_id_obj = requests.post(create_route, json={
        'token': owner,
        'u_ids': u_ids,
    })
    dm_info = dm_id_obj.json()
    dm_id = dm_info['dm_id']

    requests.post(leave_route, json = {
        'token': owner,
        'dm_id': dm_id,
    })

    response = requests.delete(remove_route, json = {
        'token': owner,
        'dm_id': dm_id,
    })
    assert response.status_code == AccessError.code


# routine setup
def test_working_setup(create_route,remove_route,dummy_data):
    reset_call()

    users = dummy_data.register_users(num_of_users=2)
    owner = users[0]['token']
    u_ids = [users[1]['auth_user_id']]

    dm_id_obj = requests.post(create_route, json={
        'token': owner,
        'u_ids': u_ids,
    })
    dm_info = dm_id_obj.json()
    dm_id = dm_info['dm_id']

    response = requests.delete(remove_route, json = {
        'token': owner,
        'dm_id': dm_id,
    })
    assert response.status_code == 200
