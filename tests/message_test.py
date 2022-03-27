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
    user1_obj = requests.post(
        f'{url}/auth/register/v2',
        json={"email": "unswisgreat@unsw.edu.au", "password": "unsw123456", "name_first": "Tony", "name_last": "Stark"})
    assert user1_obj.status_code == OKAY
    user1_dict = user1_obj.json()
    assert isinstance(user1_dict, dict) and 'token' in user1_dict and isinstance(user1_dict['token'], str)

    # second user
    user2_obj =  requests.post(
        f'{url}/auth/register/v2',
        json={"email": "hellounsw@gmail.com", "password": "hey123456", "name_first": "Bruce", "name_last": "Banner"})
    user2_dict = user2_obj.json()

    dm_obj = requests.post(
        f'{url}/dm/create/v1',
        json={"token": user1_dict['token'], "u_ids": [user2_dict["auth_user_id"]]})
    assert dm_obj.status_code == OKAY
    dm_dict = dm_obj.json()

    return [user1_dict, user2_dict, dm_dict]

def test_message_senddm_token_error(setup):
    dm_dict = setup[2]

    dm_id = dm_dict['dm_id']
    message = "This is very good"

    response = requests.post(
        f'{url}/message/senddm/v1',
        json={"token": 'invalidtoken', "dm_id": dm_id, "message": message})
    assert response.status_code == AccessError.code

def test_message_senddm_working(setup):
    user1_dict = setup[0]
    dm_dict = setup[2]

    token = user1_dict['token']
    dm_id = dm_dict['dm_id']
    message = "This is very good"

    response = requests.post(
        f'{url}/message/senddm/v1',
        json={"token": token, "dm_id": dm_id, "message": message})
    assert response.status_code == OKAY

    message = "This is very good and very good"

    response = requests.post(
        f'{url}/message/senddm/v1',
        json={"token": token, "dm_id": dm_id, "message": message})
    assert response.status_code == OKAY

    message = "This is very, very good"
    response = requests.post(
        f'{url}/message/senddm/v1',
        json={"token": token, "dm_id": dm_id, "message": message})
    assert response.status_code == OKAY
    # the messages in dm should have three messages

def test_message_senddm_dm_id_invalid(setup):
    user1_dict = setup[0]
    dm_dict = setup[2]

    token = user1_dict['token']
    dm_id = dm_dict['dm_id']
    message = "This is very good"

    response = requests.post(
        f'{url}/message/senddm/v1',
        json={"token": token, "dm_id": dm_id+100, "message": message})
    assert response.status_code == InputError.code

def test_message_senddm_short_len(setup):
    user1_dict = setup[0]
    dm_dict = setup[2]

    token = user1_dict['token']
    dm_id = dm_dict['dm_id']

    response = requests.post(
        f'{url}/message/senddm/v1',
        json={"token": token, "dm_id": dm_id, "message": ""})
    assert response.status_code == InputError.code

def test_message_senddm_long_len(setup):
    user1_dict = setup[0]
    dm_dict = setup[2]

    token = user1_dict['token']
    dm_id = dm_dict['dm_id']
    message = "This is very goodd"*500

    response = requests.post(
        f'{url}/message/senddm/v1',
        json={"token": token, "dm_id": dm_id, "message": message})
    assert response.status_code == InputError.code

def test_message_senddm_not_member(setup):
    dm_dict = setup[2]

    user_obj =  requests.post(
        f'{url}/auth/register/v2',
        json={"email": "hellosssunsw@gmail.com", "password": "hey12345678", "name_first": "Bruces", "name_last": "Banners"})
    user_dict = user_obj.json()

    token = user_dict['token']
    dm_id = dm_dict['dm_id']
    message = "This is very goodd"

    response = requests.post(
        f'{url}/message/senddm/v1',
        json={"token": token, "dm_id": dm_id, "message": message})
    assert response.status_code == AccessError.code