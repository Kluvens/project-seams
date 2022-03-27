import requests
from requests import HTTPError
import pytest
from src.config import url
from src.error import InputError, AccessError

OKAY = 200

@pytest.fixture
def setup():
    # setup data_store
    requests.delete(f'{url}/clear/v1')

    # first user
    user1_obj = requests.post(f'{url}/auth/register/v2', json={"email": "unswisgreat@unsw.edu.au", "password": "unsw123456", "name_first": "Tony", "name_last": "Stark"})
    assert user1_obj.status_code == OKAY
    user1_dict = user1_obj.json()

    # second user
    user2_obj =  requests.post(f'{url}/auth/register/v2', json={"email": "hellounsw@gmail.com", "password": "hey123456", "name_first": "Bruce", "name_last": "Banner"})
    user2_dict = user2_obj.json()

    # create first channel
    channel1_obj = requests.post(f'{url}/channels/create/v2', json={"token": user1_dict['token'], "name": "Kias_channel", "is_public": True})
    channel1_dict = channel1_obj.json()

    # create second channel
    channel2_obj = requests.post(f'{url}/channels/create/v2', json={"token": user2_dict['token'], "name": "my_channel", "is_public": False})
    channel2_dict = channel2_obj.json()

    return [user1_dict, user2_dict, channel1_dict, channel2_dict]

# def test_admin_user_remove_working(setup):
#     user1_dict = setup[0]
#     user2_dict = setup[1]
#     channel_dict = setup[2]

#     token = user1_dict['token']
#     u_id = user2_dict['auth_user_id']
#     channel_id = channel_dict['channel_id']

#     response = requests.post(f'{url}/channel/invite/v2', json={'token': token, 'channel_id': channel_id, 'u_id': u_id})
#     assert response.status_code == OKAY
    
#     response = requests.delete(f"{url}/admin/user/remove/v1", json={'token': token, 'u_id': u_id})
#     assert response.status_code == OKAY

#     response = requests.post(f"{url}/channel/details/v2", json={'token': token, 'channel_id': channel_id})
#     assert response.status_code == OKAY

#     details_list = response.json()
#     assert isinstance(details_list, dict)

def test_admin_user_remove_token_error(setup):
    user_dict = setup[1]
    u_id = user_dict['auth_user_id']

    response = requests.delete(f'{url}/admin/user/remove/v1', json={'token': "invalidtoken", 'u_id': u_id})
    assert response.status_code == AccessError.code

def test_admin_user_remove_invalid_user(setup):
    user1_dict = setup[0]
    user2_dict = setup[1]

    token = user1_dict['token']
    u_id = user2_dict['auth_user_id']

    response = requests.delete(f'{url}/admin/user/remove/v1', json={'token': token, 'u_id': u_id+100})
    assert response.status_code == InputError.code

def test_admin_user_remove_only_global_user(setup):
    user1_dict = setup[0]

    token = user1_dict['token']
    u_id = user1_dict['auth_user_id']

    response = requests.delete(f'{url}/admin/user/remove/v1', json={'token': token, 'u_id': u_id})
    assert response.status_code == InputError.code

def test_admin_user_remove_not_global_user(setup):
    user1_dict = setup[0]
    user2_dict = setup[1]

    token = user2_dict['token']
    u_id = user1_dict['auth_user_id']

    response = requests.delete(f'{url}/admin/user/remove/v1', json={'token': token, 'u_id': u_id})
    assert response.status_code == AccessError.code

def test_admin_permission_token_error(setup):
    OWNER = 1

    user_dict = setup[1]
    u_id = user_dict['auth_user_id']

    response = requests.post(f'{url}/admin/userpermission/change/v1', json={"token": "invalidtoken", "u_id": u_id, "permission_id": OWNER})
    assert response.status_code == AccessError.code

def test_admin_permission_invalid_u_id(setup):
    OWNER = 1

    user1_dict = setup[0]
    user2_dict = setup[1]
    token = user1_dict['token']
    u_id = user2_dict['auth_user_id']

    response = requests.post(f'{url}/admin/userpermission/change/v1', json={"token": token, "u_id": u_id+100, "permission_id": OWNER})
    assert response.status_code == InputError.code

def test_admin_permission_only_global_owner(setup):
    MEMBER = 2

    user_dict = setup[0]
    token = user_dict['token']
    u_id = user_dict['auth_user_id']

    response = requests.post(f'{url}/admin/userpermission/change/v1', json={"token": token, "u_id": u_id, "permission_id": MEMBER})
    assert response.status_code == InputError.code

def test_admin_permission_id_invalid(setup):
    INVALID = 3

    user1_dict = setup[0]
    user2_dict = setup[1]
    token = user1_dict['token']
    u_id = user2_dict['auth_user_id']

    response = requests.post(f'{url}/admin/userpermission/change/v1', json={"token": token, "u_id": u_id, "permission_id": INVALID})
    assert response.status_code == InputError.code

def test_admin_permission_already(setup):
    OWNER = 1

    user1_dict = setup[0]
    user2_dict = setup[1]
    token = user1_dict['token']
    u_id = user2_dict['auth_user_id']

    response = requests.post(f'{url}/admin/userpermission/change/v1', json={"token": token, "u_id": u_id, "permission_id": OWNER})
    assert response.status_code == OKAY

    response = requests.post(f'{url}/admin/userpermission/change/v1', json={"token": token, "u_id": u_id, "permission_id": OWNER})
    assert response.status_code == InputError.code

def test_admin_permission_not_global_owner(setup):
    MEMBER = 2

    user1_dict = setup[0]
    user2_dict = setup[1]
    token = user2_dict['token']
    u_id = user1_dict['auth_user_id']

    response = requests.post(f'{url}/admin/userpermission/change/v1', json={"token": token, "u_id": u_id, "permission_id": MEMBER})
    assert response.status_code == AccessError.code

def test_admin_permission_working(setup):
    OWNER = 1
    MEMBER = 2

    user1_dict = setup[0]
    user2_dict = setup[1]
    user3_obj = requests.post(f'{url}/auth/register/v2', json={"email": "howareyou@outlook.com", "password": "hey12345678", "name_first": "Bruces", "name_last": "Banners"})
    user3_dict = user3_obj.json()

    token = user1_dict['token']
    token_second = user2_dict['token']
    token_thrid = user3_dict['token']

    u_id = user1_dict['auth_user_id']
    u_id2 = user2_dict['auth_user_id']
    u_id3 = user3_dict['auth_user_id']

    response = requests.post(f'{url}/admin/userpermission/change/v1', json={"token": token, "u_id": u_id2, "permission_id": OWNER})
    assert response.status_code == OKAY

    response = requests.post(f'{url}/admin/userpermission/change/v1', json={"token": token_second, "u_id": u_id3, "permission_id": OWNER})
    assert response.status_code == OKAY

    response = requests.post(f'{url}/admin/userpermission/change/v1', json={"token": token_second, "u_id": u_id, "permission_id": MEMBER})
    assert response.status_code == OKAY

    response = requests.post(f'{url}/admin/userpermission/change/v1', json={"token": token_thrid, "u_id": u_id, "permission_id": OWNER})
    assert response.status_code == OKAY

    response = requests.post(f'{url}/admin/userpermission/change/v1', json={"token": token, "u_id": u_id2, "permission_id": MEMBER})
    assert response.status_code == OKAY

    response = requests.post(f'{url}/admin/userpermission/change/v1', json={"token": token, "u_id": u_id3, "permission_id": MEMBER})
    assert response.status_code == OKAY

