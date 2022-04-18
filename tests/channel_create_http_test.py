'''
This is a testing module for channels/create/v2

'''

import requests
import pytest
from src.config import url
from src.error import AccessError
from src.error import InputError

OKAY = 200


@pytest.fixture
def setup():
    # setup data_store
    requests.delete(f'{url}/clear/v1')

    # first user
    user1_obj = requests.post(
        url + "auth/register/v2", 
        json={
            "email": "unswisgreat@unsw.edu.au", 
            "password": "unsw123456", 
            "name_first": "Tony", 
            "name_last": "Stark"}
        )

    user1_dict = user1_obj.json()

    # second user
    user2_obj =  requests.post(
        f'{url}/auth/register/v2', 
        json={
            "email": "hellounsw@gmail.com",
            "password": "hey123456",
            "name_first":
            "Bruce",
            "name_last":
            "Banner"}
        )

    user2_dict = user2_obj.json()

    # create first channel
    channel1_obj = requests.post(
        f'{url}/channels/create/v2', 
        json={
            "token": user1_dict["token"],
            "name": "Kais_channel",
            "is_public": True}
        )

    channel1_dict = channel1_obj.json()

    # create second channel
    channel2_obj = requests.post(
        f'{url}/channels/create/v2',
        json={"token": user2_dict['token'],
        "name": "my_channel",
        "is_public": False}
    )

    channel2_dict = channel2_obj.json()

    return [user1_dict, user2_dict, channel1_dict, channel2_dict]


def test_channel_create_token_error(setup):
    response = requests.post(
        f"{url}/channels/create/v2", 
        json={
            "token": "Invalid token",
            "name": "Kias_channel",
            "is_public": True}
        )

    assert response.status_code == AccessError.code


def test_channel_create_inputError_more_than_20(setup):
    user_dict = setup[0]
    token = user_dict['token']

    response = requests.post(
        f"{url}/channels/create/v2",
        json={
            "token": token,
            "name": "hahahahahaahahahahahamustbemorethantwentyletters",
            "is_public": False}
        )

    assert response.status_code == InputError.code

def test_channel_details_working_single_member(setup):
    user_dict = setup[0]
    channel_dict = setup[2]

    token = user_dict['token']
    channel_id = channel_dict['channel_id']


    response = requests.get(
        f'{url}/channel/details/v2', 
        params={'token': token,
        'channel_id': int(channel_id)})
    
    assert response.status_code == OKAY
    first_channel_details = response.json()

    assert first_channel_details['name'] == "Kais_channel"
    assert first_channel_details["is_public"] == True
    ###### One error down channel details does not return an id #########
    # assert first_channel_details["channel_id"] == str(channel_id)
    assert isinstance(first_channel_details["owner_members"], list)

    assert isinstance(first_channel_details["all_members"], list)
