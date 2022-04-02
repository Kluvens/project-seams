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
    user2_dict = setup[1]
    channel_dict = setup[2]
    dm_dict = setup[3]

    token = user1_dict['token']
    dm_id = dm_dict['dm_id']

    for num in range(10):
        response = requests.post(f'{url}/message/senddm/v1', json={'token': token, 'dm_id': dm_id, 'message': "I love you"})
        assert response.status_code == OKAY
    
    # for num in range(10):
    #     message_senddm_v1(token, dm_id, "I love you")

    response = requests.post(f'{url}/auth/logout/v1', json={'token': token})
    assert response.status_code == OKAY
    
    response = requests.post(f'{url}/message/pin/v1', json={'token': token, 'message_id': 0})
    assert response.status_code == AccessError.code

def test_message_pin_no_permission_channel():
    pass

def test_message_pin_no_permission_dm():
    pass

def test_message_pin_invalid_message():
    pass

def test_message_pin_already_pinned():
    pass

def test_message_pin_working(setup):
    user1_dict = setup[0]
    user2_dict = setup[1]
    channel_dict = setup[2]
    dm_dict = setup[3]

    token = user1_dict['token']
    dm_id = dm_dict['dm_id']

    for num in range(10):
        response = requests.post(f'{url}/message/senddm/v1', json={'token': token, 'dm_id': dm_id, 'message': "I love you"})
        assert response.status_code == OKAY
        message_id = response.json()['message_id']
    
    # for num in range(10):
    #     message_senddm_v1(token, dm_id, "I love you")

    # response = requests.post(f'{url}/auth/logout/v1', json={'token': token})
    # assert response.status_code == OKAY
    
    response = requests.post(f'{url}/message/pin/v1', json={'token': token, 'message_id': message_id})
    assert response.status_code == OKAY


