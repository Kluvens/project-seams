import requests
import pytest
from src.config import url
from tests.http_helpers import GenerateTestData
from src.error import InputError, AccessError

#====================== Helper functions / Fixtures ===============

def reset_call():
    requests.delete(url + 'clear/v1')

@pytest.fixture
def create_route():
    return url + "dm/create/v1"

@pytest.fixture()
def leave_route():
    return url + "dm/leave/v1"

@pytest.fixture()
def dummy_data():
    data_instance = GenerateTestData(url)
    return data_instance


# ===================== HTTP TESTS =====================================

# def test_create_token_error(create_route, dummy_data):
#     reset_call()

#     users = dummy_data.register_users(num_of_users=2)
#     u_ids = [users[1]['auth_user_id']]

#     dm_id_obj = requests.post(create_route, json={
#         'token': 'invalidtoken',
#         'u_ids': u_ids,
#     })
#     assert dm_id_obj.status_code == AccessError.code

# def test_create_duplicate(create_route, dummy_data):
#     reset_call()

#     users = dummy_data.register_users(num_of_users=2)
#     owner = users[0]['token']
#     u_ids = [users[1]['auth_user_id'], users[1]['auth_user_id']]

#     dm_id_obj = requests.post(create_route, json={
#         'token': owner,
#         'u_ids': u_ids,
#     })
#     assert dm_id_obj.status_code == InputError.code

# def test_create_invalid_user(create_route, dummy_data):
#     reset_call()

#     users = dummy_data.register_users(num_of_users=2)
#     owner = users[0]['token']
#     u_ids = [users[1]['auth_user_id'], users[1]['auth_user_id']+100]

#     dm_id_obj = requests.post(create_route, json={
#         'token': owner,
#         'u_ids': u_ids,
#     })
#     assert dm_id_obj.status_code == InputError.code

def test_invalid_token_type(leave_route,create_route,dummy_data):
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

    response = requests.post(leave_route,json = {
        'token':'12345',
        'dm_id': dm_id
        })
    assert response.status_code == AccessError.code

# invalid dm
def test_invalid_dm_id(create_route,leave_route,dummy_data):
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

    response = requests.post(leave_route,json = {
        'token': owner,
        'dm_id': dm_id+100,
        })
    assert response.status_code == InputError.code

# authorized user is not a member of dm
def test_user_not_in_dm(create_route,leave_route,dummy_data):
    reset_call()

    users = dummy_data.register_users(num_of_users=3)
    owner = users[0]['token']
    u_ids = [users[1]['auth_user_id']]
    other = users[2]['token']

    dm_id_obj = requests.post(create_route, json={
        'token': owner,
        'u_ids': u_ids,
    })
    dm_info = dm_id_obj.json()
    dm_id = dm_info['dm_id']


    response = requests.post(leave_route, json = {
        'token': other,
        'dm_id': dm_id,
    })
    assert response.status_code == AccessError.code

# routine behavior
def test_working_setup(create_route,leave_route,dummy_data):
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

    response = requests.post(leave_route, json = {
        'token': owner,
        'dm_id': dm_id,
    })
    assert response.status_code == 200

    response = requests.get(f"{url}/dm/details/v1", params={'token': owner, 'dm_id': dm_id})
    assert response.status_code == AccessError.code
