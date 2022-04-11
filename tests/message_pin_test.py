import requests
from requests import HTTPError
import pytest
from src.config import url
from src.error import InputError, AccessError
from src.auth import auth_register_v2, auth_logout_v1
from src.channels import channels_create_v2
from src.dms import dm_create_v1
from src.message import message_pin_v1, message_senddm_v1

OKAY = 200

@pytest.fixture
def setup():
    # setup data_store
    requests.delete(f'{url}/clear/v1')

    # first user
    user1_obj = requests.post(f'{url}/auth/register/v2', json={"email": "unswisgreat@unsw.edu.au", "password": "unsw123456", "name_first": "Tony", "name_last": "Stark"})
    assert user1_obj.status_code == OKAY
    user1_dict = user1_obj.json()
    assert isinstance(user1_dict, dict) and 'token' in user1_dict and isinstance(user1_dict['token'], str)

    # second user
    user2_obj =  requests.post(f'{url}/auth/register/v2', json={"email": "hellounsw@gmail.com", "password": "hey123456", "name_first": "Bruce", "name_last": "Banner"})
    assert user2_obj.status_code == OKAY
    user2_dict = user2_obj.json()
    assert isinstance(user2_dict, dict)

    channel_obj = requests.post(f'{url}/channels/create/v2', json={"token": user1_dict['token'], "name": "Kias_channel", "is_public": True})
    assert channel_obj.status_code == OKAY
    channel_dict = channel_obj.json()

    dm_obj = requests.post(f'{url}/dm/create/v1', json={'token': user1_dict['token'], 'u_ids': [user2_dict['auth_user_id']]})
    assert dm_obj.status_code == OKAY
    dm_dict = dm_obj.json()

    return [user1_dict, user2_dict, channel_dict, dm_dict]

def test_message_pin_invalid_token(setup):
    user1_dict = setup[0]
    dm_dict = setup[3]

    token = user1_dict['token']
    dm_id = dm_dict['dm_id']

    for _ in range(10):
        response = requests.post(f'{url}/message/senddm/v1', json={'token': token, 'dm_id': dm_id, 'message': "I love you"})
        assert response.status_code == OKAY
        message_id = response.json()['message_id']

    response = requests.post(f'{url}/auth/logout/v1', json={'token': token})
    assert response.status_code == OKAY
    
    response = requests.post(f'{url}/message/pin/v1', json={'token': token, 'message_id': message_id})
    assert response.status_code == AccessError.code

def test_message_pin_no_permission_channel(setup):
    user1_dict = setup[0]
    user2_dict = setup[1]
    channel_dict = setup[2]

    token = user1_dict['token']
    token_second = user2_dict['token']
    u_id_second = user2_dict['auth_user_id']

    response = requests.post(f'{url}/channel/join/v2', json={'token': token_second, 'channel_id': channel_dict['channel_id']})
    assert response.status_code == OKAY

    response = requests.post(f'{url}/message/send/v1', json={'token': token, 'channel_id': channel_dict['channel_id'], 'message': "I love you"})
    assert response.status_code == OKAY
    message_id = response.json()['message_id']

    response = requests.post(f'{url}/message/pin/v1', json={'token': token_second, 'message_id': message_id})
    assert response.status_code == AccessError.code

    response = requests.post(f'{url}/message/pin/v1', json={'token': token, 'message_id': message_id})
    assert response.status_code == OKAY

    response = requests.post(f'{url}/channel/addowner/v1', json={'token': token, 'channel_id': channel_dict['channel_id'], 'u_id': u_id_second})
    assert response.status_code == OKAY

    response = requests.get(f'{url}/channel/details/v2', params={'token': token, 'channel_id': channel_dict['channel_id']})
    assert response.status_code == OKAY
    details = response.json()
    assert u_id_second in [member['u_id'] for member in details['owner_members']]

    response = requests.post(f'{url}/message/pin/v1', json={'token': token_second, 'message_id': message_id})
    assert response.status_code == InputError.code

def test_message_pin_no_permission_dm(setup):
    user1_dict = setup[0]
    user2_dict = setup[1]
    dm_dict = setup[3]

    token = user1_dict['token']
    token_second = user2_dict['token']
    dm_id = dm_dict['dm_id']

    for _ in range(10):
        response = requests.post(f'{url}/message/senddm/v1', json={'token': token, 'dm_id': dm_id, 'message': "I love you"})
        assert response.status_code == OKAY
        message_id = response.json()['message_id']

    response = requests.post(f'{url}/message/pin/v1', json={'token': token_second, 'message_id': message_id})
    assert response.status_code == AccessError.code


def test_message_pin_invalid_message(setup):
    user1_dict = setup[0]
    dm_dict = setup[3]

    token = user1_dict['token']
    dm_id = dm_dict['dm_id']

    for _ in range(10):
        response = requests.post(f'{url}/message/senddm/v1', json={'token': token, 'dm_id': dm_id, 'message': "I love you"})
        assert response.status_code == OKAY
        message_id = response.json()['message_id']
    
    response = requests.post(f'{url}/message/pin/v1', json={'token': token, 'message_id': message_id+100})
    assert response.status_code == InputError.code

def test_message_pin_already_pinned(setup):
    user1_dict = setup[0]
    dm_dict = setup[3]

    token = user1_dict['token']
    dm_id = dm_dict['dm_id']

    for _ in range(10):
        response = requests.post(f'{url}/message/senddm/v1', json={'token': token, 'dm_id': dm_id, 'message': "I love you"})
        assert response.status_code == OKAY
        message_id = response.json()['message_id']
    
    response = requests.post(f'{url}/message/pin/v1', json={'token': token, 'message_id': message_id})
    assert response.status_code == OKAY

    response = requests.post(f'{url}/message/pin/v1', json={'token': token, 'message_id': message_id})
    assert response.status_code == InputError.code

def test_message_pin_working(setup):
    user1_dict = setup[0]
    dm_dict = setup[3]

    token = user1_dict['token']
    dm_id = dm_dict['dm_id']

    for _ in range(10):
        response = requests.post(f'{url}/message/senddm/v1', json={'token': token, 'dm_id': dm_id, 'message': "I love you"})
        assert response.status_code == OKAY
        message_id = response.json()['message_id']
    
    response = requests.post(f'{url}/message/pin/v1', json={'token': token, 'message_id': message_id})
    assert response.status_code == OKAY

def test_message_unpin_invalid_token(setup):
    user1_dict = setup[0]
    dm_dict = setup[3]

    token = user1_dict['token']
    dm_id = dm_dict['dm_id']

    for _ in range(10):
        response = requests.post(f'{url}/message/senddm/v1', json={'token': token, 'dm_id': dm_id, 'message': "I love you"})
        assert response.status_code == OKAY
        message_id = response.json()['message_id']
    
    response = requests.post(f'{url}/message/pin/v1', json={'token': token, 'message_id': message_id})
    assert response.status_code == OKAY

    response = requests.post(f'{url}/auth/logout/v1', json={'token': token})
    assert response.status_code == OKAY

    response = requests.post(f'{url}/message/unpin/v1', json={'token': token, 'message_id': message_id})
    assert response.status_code == AccessError.code

def test_message_unpin_already_unpinned(setup):
    user1_dict = setup[0]
    dm_dict = setup[3]

    token = user1_dict['token']
    dm_id = dm_dict['dm_id']

    for _ in range(10):
        response = requests.post(f'{url}/message/senddm/v1', json={'token': token, 'dm_id': dm_id, 'message': "I love you"})
        assert response.status_code == OKAY
        message_id = response.json()['message_id']
    
    response = requests.post(f'{url}/message/pin/v1', json={'token': token, 'message_id': message_id})
    assert response.status_code == OKAY

    response = requests.post(f'{url}/message/unpin/v1', json={'token': token, 'message_id': message_id})
    assert response.status_code == OKAY

    response = requests.post(f'{url}/message/unpin/v1', json={'token': token, 'message_id': message_id})
    assert response.status_code == InputError.code

def test_message_unpin_no_permission(setup):
    user1_dict = setup[0]
    user2_dict = setup[1]
    channel_dict = setup[2]

    token = user1_dict['token']
    token_second = user2_dict['token']
    u_id_second = user2_dict['auth_user_id']

    response = requests.post(f'{url}/channel/join/v2', json={'token': token_second, 'channel_id': channel_dict['channel_id']})
    assert response.status_code == OKAY

    response = requests.post(f'{url}/message/send/v1', json={'token': token, 'channel_id': channel_dict['channel_id'], 'message': "I love you"})
    assert response.status_code == OKAY
    message_id = response.json()['message_id']

    response = requests.post(f'{url}/message/pin/v1', json={'token': token_second, 'message_id': message_id})
    assert response.status_code == AccessError.code

    response = requests.post(f'{url}/message/pin/v1', json={'token': token, 'message_id': message_id})
    assert response.status_code == OKAY

    response = requests.post(f'{url}/message/unpin/v1', json={'token': token_second, 'message_id': message_id})
    assert response.status_code == AccessError.code

    response = requests.post(f'{url}/channel/addowner/v1', json={'token': token, 'channel_id': channel_dict['channel_id'], 'u_id': u_id_second})
    assert response.status_code == OKAY

    response = requests.get(f'{url}/channel/details/v2', params={'token': token, 'channel_id': channel_dict['channel_id']})
    assert response.status_code == OKAY
    details = response.json()
    assert u_id_second in [member['u_id'] for member in details['owner_members']]

    response = requests.post(f'{url}/message/pin/v1', json={'token': token_second, 'message_id': message_id})
    assert response.status_code == InputError.code

    response = requests.post(f'{url}/message/unpin/v1', json={'token': token_second, 'message_id': message_id})
    assert response.status_code == OKAY

def test_message_unpin_invalid_message(setup):
    user1_dict = setup[0]
    dm_dict = setup[3]

    token = user1_dict['token']
    dm_id = dm_dict['dm_id']

    for _ in range(10):
        response = requests.post(f'{url}/message/senddm/v1', json={'token': token, 'dm_id': dm_id, 'message': "I love you"})
        assert response.status_code == OKAY
        message_id = response.json()['message_id']
    
    response = requests.post(f'{url}/message/pin/v1', json={'token': token, 'message_id': message_id})
    assert response.status_code == OKAY

    response = requests.post(f'{url}/message/unpin/v1', json={'token': token, 'message_id': message_id+100})
    assert response.status_code == InputError.code

def test_message_unpin_working(setup):
    user1_dict = setup[0]
    dm_dict = setup[3]

    token = user1_dict['token']
    dm_id = dm_dict['dm_id']

    for _ in range(10):
        response = requests.post(f'{url}/message/senddm/v1', json={'token': token, 'dm_id': dm_id, 'message': "I love you"})
        assert response.status_code == OKAY
        message_id = response.json()['message_id']
    
    response = requests.post(f'{url}/message/pin/v1', json={'token': token, 'message_id': message_id})
    assert response.status_code == OKAY

    response = requests.post(f'{url}/message/unpin/v1', json={'token': token, 'message_id': message_id})
    assert response.status_code == OKAY

    response = requests.post(f'{url}/message/pin/v1', json={'token': token, 'message_id': message_id})
    assert response.status_code == OKAY
