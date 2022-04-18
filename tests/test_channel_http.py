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
    assert isinstance(user1_dict, dict) and 'token' in user1_dict and isinstance(user1_dict['token'], str)

    # second user
    user2_obj =  requests.post(f'{url}/auth/register/v2', json={"email": "hellounsw@gmail.com", "password": "hey123456", "name_first": "Bruce", "name_last": "Banner"})
    user2_dict = user2_obj.json()

    # create first channel
    channel1_obj = requests.post(f'{url}/channels/create/v2', json={"token": user1_dict['token'], "name": "Kias_channel", "is_public": True})
    channel1_dict = channel1_obj.json()
    assert isinstance(channel1_dict, dict) and 'channel_id' in channel1_dict and isinstance(channel1_dict['channel_id'], int)

    # create second channel
    channel2_obj = requests.post(f'{url}/channels/create/v2', json={"token": user2_dict['token'], "name": "my_channel", "is_public": False})
    channel2_dict = channel2_obj.json()

    return [user1_dict, user2_dict, channel1_dict, channel2_dict]

def test_channel_create_token_error(setup):
    user_dict = setup[0]
    token = user_dict['token']
    assert isinstance(token, str)

    response = requests.post(f"{url}/channels/create/v2", json={"token": 'invalid_token', "name": "Kias_channel", "is_public": True})
    assert response.status_code == AccessError.code

def test_channel_create_inputError_less_than_1(setup):
    user_dict = setup[0]
    token = user_dict['token']

    response = requests.post(f"{url}/channels/create/v2", json={"token": token, "name": "", "is_public": False})
    assert response.status_code == InputError.code  

def test_channel_create_inputError_more_than_20(setup):
    user_dict = setup[0]
    token = user_dict['token']

    response = requests.post(f"{url}/channels/create/v2", json={"token": token, "name": "hahahahahaahahahahahamustbemorethantwentyletters", "is_public": False})
    assert response.status_code == InputError.code

def test_channel_details_working_single_member(setup):
    user_dict = setup[0]
    channel_dict = setup[2]

    token = user_dict['token']
    auth_user_id = user_dict['auth_user_id']
    channel_id = channel_dict['channel_id']

    response = requests.get(f'{url}/channel/details/v2', params={'token': token, 'channel_id': channel_id})
    assert response.status_code == OKAY
    first_channel_details = response.json()

    assert first_channel_details['name'] == "Kias_channel"
    assert first_channel_details["is_public"] == True
    assert first_channel_details["owner_members"] == [
        {
            "u_id": auth_user_id,
            "email": "unswisgreat@unsw.edu.au",
            "name_first": "Tony",
            "name_last": "Stark",
            "handle_str": "tonystark",
        }
    ]
    assert first_channel_details["all_members"] == [
        {
            "u_id": auth_user_id,
            "email": "unswisgreat@unsw.edu.au",
            "name_first": "Tony",
            "name_last": "Stark",
            "handle_str": "tonystark",
        }
    ]

def test_channel_create_and_details_working(setup):
    user1_dict = setup[0]
    user2_dict = setup[1]
    channel_dict = setup[2]

    token = user1_dict['token']
    auth_user_id = user1_dict['auth_user_id']
    u_id = user2_dict['auth_user_id']
    channel_id = channel_dict['channel_id']
    assert isinstance(channel_id, int)

    response = requests.post(f'{url}/channel/invite/v2', json={'token': token, 'channel_id': channel_id, 'u_id': u_id})
    assert response.status_code == OKAY
    
    response = requests.get(f'{url}/channel/details/v2', params={'token': token, 'channel_id': channel_id})
    assert response.status_code == OKAY
    first_channel_details = response.json()

    assert first_channel_details['name'] == "Kias_channel"
    assert first_channel_details["is_public"] == True
    assert len(first_channel_details["owner_members"]) == 1
    assert first_channel_details["owner_members"] == [
        {
            "u_id": auth_user_id,
            "email": "unswisgreat@unsw.edu.au",
            "name_first": "Tony",
            "name_last": "Stark",
            "handle_str": "tonystark",
        }
    ]
    assert len(first_channel_details["all_members"]) == 2
    assert first_channel_details['all_members'] == [
        {
            "u_id": auth_user_id,
            "email": "unswisgreat@unsw.edu.au",
            "name_first": "Tony",
            "name_last": "Stark",
            "handle_str": "tonystark",
        },
        {
            "u_id": u_id,
            "email": "hellounsw@gmail.com",
            "name_first": "Bruce",
            "name_last": "Banner",
            "handle_str": "brucebanner",
        }
    ]

def test_channel_details_token_error(setup):
    channel_dict = setup[2]

    channel_id = channel_dict['channel_id']
    assert isinstance(channel_id, int)

    response = requests.get(f'{url}/channel/details/v2', params={'token': 'invalidtoken', 'channel_id': channel_id})
    assert response.status_code == AccessError.code
    
def test_channel_details_invalid_channel_id(setup):
    user_dict = setup[0]
    channel_dict = setup[2]

    token = user_dict['token']
    channel_id = channel_dict['channel_id']

    response = requests.get(f'{url}/channel/details/v2', params={'token': token, 'channel_id': channel_id+100})    
    assert response.status_code == InputError.code

def test_channel_details_invalid_auth_id(setup):
    user2_dict = setup[1]
    channel_dict = setup[2]

    token_second = user2_dict['token']
    channel_id = channel_dict['channel_id']

    response = requests.get(f"{url}/channel/details/v2", params={"token": token_second, "channel_id": channel_id})
    assert response.status_code == AccessError.code

def test_add_owner_working(setup):
    user1_dict = setup[0]
    user2_dict = setup[1]
    channel_dict = setup[2]

    token = user1_dict['token']
    auth_user_id = user1_dict['auth_user_id']
    channel_id = channel_dict['channel_id']
    u_id = user2_dict['auth_user_id']

    response = requests.post(f'{url}/channel/invite/v2', json={'token': token, 'channel_id': channel_id, 'u_id': u_id})
    assert response.status_code == OKAY

    response = requests.post(f"{url}/channel/addowner/v1", json={"token": token, "channel_id": channel_id, "u_id": u_id})
    response.status_code == OKAY

    response = requests.get(f"{url}/channel/details/v2", params={"token": token, "channel_id": channel_id})
    assert response.status_code == OKAY
    
    first_channel_details = response.json()

    assert first_channel_details['name'] == "Kias_channel"
    assert first_channel_details["is_public"] == True
    assert len(first_channel_details["owner_members"]) == 2
    assert first_channel_details["owner_members"] == [
        {
            "u_id": auth_user_id,
            "email": "unswisgreat@unsw.edu.au",
            "name_first": "Tony",
            "name_last": "Stark",
            "handle_str": "tonystark",
        },
        {
            "u_id": u_id,
            "email": "hellounsw@gmail.com",
            "name_first": "Bruce",
            "name_last": "Banner",
            "handle_str": "brucebanner",
        }
    ]
    assert len(first_channel_details['all_members']) == 2
    assert first_channel_details['all_members'] == [
        {
            "u_id": auth_user_id,
            "email": "unswisgreat@unsw.edu.au",
            "name_first": "Tony",
            "name_last": "Stark",
            "handle_str": "tonystark",
        },
        {
            "u_id": u_id,
            "email": "hellounsw@gmail.com",
            "name_first": "Bruce",
            "name_last": "Banner",
            "handle_str": "brucebanner",
        }
    ]

def test_add_owner_token_error(setup):
    user1_dict = setup[0]
    user2_dict = setup[1]
    channel_dict = setup[2]

    token = user1_dict['token']
    channel_id = channel_dict['channel_id']
    u_id = user2_dict['auth_user_id']

    response = requests.post(f"{url}/channel/invite/v2", json={"token": token, "channel_id": channel_id, "u_id": u_id})
    assert response.status_code == OKAY

    response = requests.post(f"{url}/channel/addowner/v1", json={"token": "invalid_token", "channel_id": channel_id, "u_id": u_id})
    assert response.status_code == AccessError.code

def test_add_owner_channel_id_invalid(setup):
    user1_dict = setup[0]
    user2_dict = setup[1]
    channel_dict = setup[2]

    token = user1_dict['token']
    u_id = user2_dict['auth_user_id']
    channel_id = channel_dict['channel_id']

    response = requests.post(f"{url}/channel/invite/v2", json={"token": token, "channel_id": channel_id, "u_id": u_id})
    assert response.status_code == OKAY

    response = requests.post(f"{url}/channel/addowner/v1", json={"token": token, "channel_id": channel_id+100, "u_id": u_id})
    assert response.status_code == InputError.code

def test_add_owner_u_id_invalid(setup):
    user1_dict = setup[0]
    user2_dict = setup[1]
    channel_dict = setup[2]

    token = user1_dict['token']
    u_id = user2_dict['auth_user_id']
    channel_id = channel_dict['channel_id']

    response = requests.post(f"{url}/channel/invite/v2", json={"token": token, "channel_id": channel_id, "u_id": u_id})
    assert response.status_code == OKAY

    response = requests.post(f"{url}/channel/addowner/v1", json={"token": token, "channel_id": channel_id, "u_id": u_id+100})
    assert response.status_code == InputError.code

def test_add_owner_u_id_not_member(setup):
    user1_dict = setup[0]
    user2_dict = setup[1]
    channel_dict = setup[2]

    token = user1_dict['token']
    u_id = user2_dict['auth_user_id']
    channel_id = channel_dict['channel_id']

    response = requests.post(f"{url}/channel/addowner/v1", json={"token": token, "channel_id": channel_id, "u_id": u_id})
    assert response.status_code == InputError.code

def test_add_owner_u_id_already_owner(setup):
    user1_dict = setup[0]
    user2_dict = setup[1]
    channel_dict = setup[2]

    token = user1_dict['token']
    u_id = user2_dict['auth_user_id']
    channel_id = channel_dict['channel_id']

    response = requests.post(f'{url}/channel/invite/v2', json={'token': token, 'channel_id': channel_id, 'u_id': u_id})
    assert response.status_code == OKAY

    response = requests.post(f"{url}/channel/addowner/v1", json={"token": token, "channel_id": channel_id, "u_id": u_id})
    response.status_code == OKAY

    response = requests.post(f"{url}/channel/addowner/v1", json={"token": token, "channel_id": channel_id, "u_id": u_id})
    assert response.status_code == InputError.code

def test_add_owner_no_permission(setup):
    user1_dict = setup[0]
    user2_dict = setup[1]
    channel_dict = setup[2]
    user3_obj = requests.post(f'{url}/auth/register/v2', json={"email": "howareyou@outlook.com", "password": "hey12345678", "name_first": "Bruces", "name_last": "Banners"})
    user3_dict = user3_obj.json()

    token = user1_dict['token']
    token_second = user2_dict['token']
    channel_id = channel_dict['channel_id']
    u_id = user2_dict['auth_user_id']
    u_next_id = user3_dict['auth_user_id']

    response = requests.post(f'{url}/channel/invite/v2', json={'token': token, 'channel_id': channel_id, 'u_id': u_id})
    assert response.status_code == OKAY

    response = requests.post(f'{url}/channel/invite/v2', json={'token': token, 'channel_id': channel_id, 'u_id': u_next_id})
    assert response.status_code == OKAY

    response = requests.post(f"{url}/channel/addowner/v1", json={"token": token_second, "channel_id": channel_id, "u_id": u_next_id})
    assert response.status_code == AccessError.code

def test_add_owner_good_permission(setup):
    user1_dict = setup[0]
    user2_dict = setup[1]
    channel_dict = setup[3]
    user3_obj = requests.post(f'{url}/auth/register/v2', json={"email": "howareyou@outlook.com", "password": "hey12345678", "name_first": "Bruces", "name_last": "Banners"})
    user3_dict = user3_obj.json()

    token = user1_dict['token']
    token_second = user2_dict['token']
    channel_id = channel_dict['channel_id']
    u_id = user1_dict['auth_user_id']
    u_next_id = user3_dict['auth_user_id']

    response = requests.post(f'{url}/channel/invite/v2', json={'token': token_second, 'channel_id': channel_id, 'u_id': u_id})
    assert response.status_code == OKAY

    response = requests.post(f'{url}/channel/invite/v2', json={'token': token_second, 'channel_id': channel_id, 'u_id': u_next_id})
    assert response.status_code == OKAY

    response = response = response = requests.post(f"{url}/channel/addowner/v1", json={"token": token, "channel_id": channel_id, "u_id": u_next_id})
    assert response.status_code == OKAY

def test_remove_owner_working(setup):
    user1_dict = setup[0]
    user2_dict = setup[1]
    channel_dict = setup[2]

    token = user1_dict['token']
    auth_user_id = user1_dict['auth_user_id']
    channel_id = channel_dict['channel_id']
    u_id = user2_dict['auth_user_id']

    response = requests.post(f'{url}/channel/invite/v2', json={'token': token, 'channel_id': channel_id, 'u_id': u_id})
    assert response.status_code == OKAY

    response = requests.post(f"{url}/channel/addowner/v1", json={"token": token, "channel_id": channel_id, "u_id": u_id})
    response.status_code == OKAY

    response = requests.post(f"{url}/channel/removeowner/v1", json={"token": token, "channel_id": channel_id, "u_id": u_id})
    assert response.status_code == OKAY

    response = requests.get(f"{url}/channel/details/v2", params={"token": token, "channel_id": channel_id})
    assert response.status_code == OKAY

    first_channel_details = response.json()

    assert first_channel_details['name'] == "Kias_channel"
    assert first_channel_details["is_public"] == True
    assert len(first_channel_details["owner_members"]) == 1
    assert first_channel_details["owner_members"] == [
        {
            "u_id": auth_user_id,
            "email": "unswisgreat@unsw.edu.au",
            "name_first": "Tony",
            "name_last": "Stark",
            "handle_str": "tonystark",
        },
    ]
    assert len(first_channel_details['all_members']) == 2
    assert first_channel_details['all_members'] == [
        {
            "u_id": auth_user_id,
            "email": "unswisgreat@unsw.edu.au",
            "name_first": "Tony",
            "name_last": "Stark",
            "handle_str": "tonystark",
        },
        {
            "u_id": u_id,
            "email": "hellounsw@gmail.com",
            "name_first": "Bruce",
            "name_last": "Banner",
            "handle_str": "brucebanner",
        }
    ]

def test_remove_owner_token_error(setup):
    user1_dict = setup[0]
    user2_dict = setup[1]
    channel_dict = setup[2]

    token = user1_dict['token']
    channel_id = channel_dict['channel_id']
    u_id = user2_dict['auth_user_id']

    response = requests.post(f'{url}/channel/invite/v2', json={'token': token, 'channel_id': channel_id, 'u_id': u_id})
    assert response.status_code == OKAY

    response = requests.post(f"{url}/channel/addowner/v1", json={"token": token, "channel_id": channel_id, "u_id": u_id})
    response.status_code == OKAY

    response = requests.post(f"{url}/channel/removeowner/v1", json={"token": "invalidtoken", "channel_id": channel_id, "u_id": u_id})
    assert response.status_code == AccessError.code

def test_remove_owner_channel_id_invalid(setup):
    user1_dict = setup[0]
    user2_dict = setup[1]
    channel_dict = setup[2]

    token = user1_dict['token']
    channel_id = channel_dict['channel_id']
    u_id = user2_dict['auth_user_id']

    response = requests.post(f'{url}/channel/invite/v2', json={'token': token, 'channel_id': channel_id, 'u_id': u_id})
    assert response.status_code == OKAY

    response = requests.post(f"{url}/channel/addowner/v1", json={"token": token, "channel_id": channel_id, "u_id": u_id})
    response.status_code == OKAY

    response = requests.post(f"{url}/channel/removeowner/v1", json={"token": token, "channel_id": channel_id+100, "u_id": u_id})
    assert response.status_code == InputError.code

def test_remove_owner_u_id_invalid(setup):
    user1_dict = setup[0]
    user2_dict = setup[1]
    channel_dict = setup[2]

    token = user1_dict['token']
    channel_id = channel_dict['channel_id']
    u_id = user2_dict['auth_user_id']

    response = requests.post(f"{url}/channel/removeowner/v1", json={"token": token, "channel_id": channel_id, "u_id": u_id+100})
    assert response.status_code == InputError.code

def test_remove_owner_u_id_not_member(setup):
    user1_dict = setup[0]
    user2_dict = setup[1]
    channel_dict = setup[2]

    token = user1_dict['token']
    channel_id = channel_dict['channel_id']
    u_id = user2_dict['auth_user_id']

    response = requests.post(f"{url}/channel/removeowner/v1", json={"token": token, "channel_id": channel_id, "u_id": u_id})
    assert response.status_code == InputError.code

def test_remove_owner_u_id_the_only_owner(setup):
    user1_dict = setup[0]
    channel_dict = setup[2]

    token = user1_dict['token']
    channel_id = channel_dict['channel_id']
    auth_user_id = user1_dict['auth_user_id']

    response = requests.post(f"{url}/channel/removeowner/v1", json={"token": token, "channel_id": channel_id, "u_id": auth_user_id})
    assert response.status_code == InputError.code

def test_remove_owner_no_permission(setup):
    user1_dict = setup[0]
    user2_dict = setup[1]
    channel_dict = setup[2]
    user3_obj = requests.post(f'{url}/auth/register/v2', json={"email": "howareyou@outlook.com", "password": "hey12345678", "name_first": "Bruces", "name_last": "Banners"})
    user3_dict = user3_obj.json()

    token = user1_dict['token']
    token_second = user2_dict['token']
    channel_id = channel_dict['channel_id']
    u_id = user2_dict['auth_user_id']
    u_next_id = user3_dict['auth_user_id']

    response = requests.post(f'{url}/channel/invite/v2', json={'token': token, 'channel_id': channel_id, 'u_id': u_id})
    assert response.status_code == OKAY

    response = requests.post(f'{url}/channel/invite/v2', json={'token': token, 'channel_id': channel_id, 'u_id': u_next_id})
    assert response.status_code == OKAY

    response = requests.post(f"{url}/channel/addowner/v1", json={"token": token, "channel_id": channel_id, "u_id": u_next_id})
    assert response.status_code == OKAY

    response = requests.post(f"{url}/channel/removeowner/v1", json={"token": token_second, "channel_id": channel_id, "u_id": u_next_id})
    assert response.status_code == AccessError.code

def test_channel_invite_token_error(setup):
    user_dict = setup[0]
    channel_dict = setup[2]

    channel_id = channel_dict['channel_id']
    u_id = user_dict['auth_user_id']

    response = requests.post(f"{url}/channel/invite/v2", json={'token': "invalidtoken", "channel_id": channel_id, "u_id": u_id})
    assert response.status_code == AccessError.code


def test_channel_invite_invalid_channel_id(setup):
    user1_dict = setup[0]
    user2_dict = setup[1]
    channel_dict = setup[2]

    token = user1_dict['token']
    channel_id = channel_dict['channel_id']
    u_id = user2_dict['auth_user_id']

    response = requests.post(f"{url}/channel/invite/v2", json={'token': token, "channel_id": channel_id+100, "u_id": u_id})
    assert response.status_code == InputError.code

def test_channel_invite_invalid_user_id(setup):
    user1_dict = setup[0]
    user2_dict = setup[1]
    channel_dict = setup[2]

    token = user1_dict['token']
    channel_id = channel_dict['channel_id']
    u_id = user2_dict['auth_user_id']

    response = requests.post(f"{url}/channel/invite/v2", json={'token': token, "channel_id": channel_id, "u_id": u_id+100})
    assert response.status_code == InputError.code

def test_channel_invite_already_member(setup):
    user1_dict = setup[0]
    user2_dict = setup[1]
    channel_dict = setup[2]

    token = user1_dict['token']
    channel_id = channel_dict['channel_id']
    u_id = user2_dict['auth_user_id']

    response = requests.post(f"{url}/channel/invite/v2", json={'token': token, "channel_id": channel_id, "u_id": u_id})
    assert response.status_code == OKAY

    response = requests.post(f"{url}/channel/invite/v2", json={'token': token, "channel_id": channel_id, "u_id": u_id})
    assert response.status_code == InputError.code

def test_channel_invite_not_member(setup):
    user2_dict = setup[1]
    channel_dict = setup[2]
    user3_obj = requests.post(f'{url}/auth/register/v2', json={"email": "howareyou@outlook.com", "password": "hey12345678", "name_first": "Bruces", "name_last": "Banners"})
    user3_dict = user3_obj.json()

    token_second = user2_dict['token']
    channel_id = channel_dict['channel_id']
    u_id = user3_dict['auth_user_id']

    response = requests.post(f"{url}/channel/invite/v2", json={'token': token_second, "channel_id": channel_id, "u_id": u_id})
    assert response.status_code == AccessError.code

def test_channel_invite_working(setup):
    user1_dict = setup[0]
    user2_dict = setup[1]
    user3_obj = requests.post(f'{url}/auth/register/v2', json={"email": "howareyou@outlook.com", "password": "hey12345678", "name_first": "Bruces", "name_last": "Banners"})
    user3_dict = user3_obj.json()
    channel1_dict = setup[2]
    channel2_dict = setup[3]

    token = user1_dict['token']
    token_second = user2_dict['token']
    token_third = user3_dict['token']
    u_id_one = user1_dict['auth_user_id']
    u_id_two = user2_dict['auth_user_id']
    u_id_three = user3_dict['auth_user_id']
    channel_id_one = channel1_dict['channel_id']
    channel_id_two = channel2_dict['channel_id']

    response = requests.post(f"{url}/channel/invite/v2", json={'token': token, "channel_id": channel_id_one, "u_id": u_id_two})
    assert response.status_code == OKAY

    response = requests.post(f"{url}/channel/invite/v2", json={'token': token_second, "channel_id": channel_id_one, "u_id": u_id_three})
    assert response.status_code == OKAY

    response = requests.get(f"{url}/channel/details/v2", params={'token': token, "channel_id": channel_id_one})
    assert response.status_code == OKAY 
    details_list = response.json()

    assert len(details_list['all_members']) == 3
    assert len(details_list['owner_members']) == 1

    response = requests.post(f"{url}/channel/invite/v2", json={'token': token_second, "channel_id": channel_id_two, "u_id": u_id_one})
    assert response.status_code == OKAY

    response = requests.post(f"{url}/channel/invite/v2", json={'token': token, "channel_id": channel_id_two, "u_id": u_id_three})
    assert response.status_code == OKAY

    response = requests.get(f"{url}/channel/details/v2", params={'token': token_third, "channel_id": channel_id_two})
    assert response.status_code == OKAY 
    details_list = response.json()

    assert len(details_list['all_members']) == 3
    assert len(details_list['owner_members']) == 1

def test_channel_join_token_error(setup):
    channel_dict = setup[2]

    channel_id = channel_dict['channel_id']
    assert isinstance(channel_id, int)

    response = requests.post(f"{url}/channel/join/v2", json={'token': "invalidtoken", "channel_id": channel_id})
    assert response.status_code == AccessError.code

def test_channel_join_invalid_invalid_channel_id(setup):
    channel_dict = setup[2]
    user2_dict = setup[1]

    token = user2_dict['token']
    channel_id = channel_dict['channel_id']
    assert isinstance(channel_id, int)

    response = requests.post(f"{url}/channel/join/v2", json={'token': token, "channel_id": channel_id+1000})
    assert response.status_code == InputError.code

def test_channel_join_already_member(setup):
    channel_dict = setup[2]
    user2_dict = setup[1]

    token = user2_dict['token']
    channel_id = channel_dict['channel_id']
    assert isinstance(channel_id, int)

    response = requests.post(f"{url}/channel/join/v2", json={'token': token, "channel_id": channel_id})
    assert response.status_code == OKAY

    response = requests.post(f"{url}/channel/join/v2", json={'token': token, "channel_id": channel_id})
    assert response.status_code == InputError.code

def test_channel_join_private(setup):
    user1_dict = setup[0]
    user2_dict = setup[1]
    user3_obj = requests.post(f'{url}/auth/register/v2', json={"email": "howareyou@outlook.com", "password": "hey12345678", "name_first": "Bruces", "name_last": "Banners"})
    user3_dict = user3_obj.json()
    channel2_dict = setup[3]

    token = user1_dict['token']
    token_second = user2_dict['token']
    token_third = user3_dict['token']
    channel_id_two = channel2_dict['channel_id']

    response = requests.post(f"{url}/channel/join/v2", json={'token': token, "channel_id": channel_id_two})
    assert response.status_code == OKAY

    response = requests.post(f"{url}/channel/join/v2", json={'token': token_third, "channel_id": channel_id_two})
    assert response.status_code == AccessError.code

    response = requests.get(f"{url}/channel/details/v2", params={'token': token_second, "channel_id": channel_id_two})
    assert response.status_code == OKAY
    details_list = response.json()
    assert details_list['is_public'] == False
    assert len(details_list['owner_members']) == 1
    assert len(details_list['all_members']) == 2

def test_channel_leave_working_one(setup):
    user_dict = setup[0]
    channel_dict = setup[2]

    token = user_dict['token']
    channel_id = channel_dict['channel_id']

    response = requests.post(f"{url}/channel/leave/v1", json={'token': token, 'channel_id': channel_id})
    assert response.status_code == OKAY

    assert isinstance(channel_id, int)
    response = requests.get(f"{url}/channel/details/v2", params={'token': token, 'channel_id': channel_id})
    assert response.status_code == AccessError.code

def test_channel_leave_working_two(setup):
    user1_dict = setup[0]
    user2_dict = setup[1]
    channel_dict = setup[2]

    token = user1_dict['token']
    token_second = user2_dict['token']
    channel_id = channel_dict['channel_id']

    response = requests.post(f"{url}/channel/join/v2", json={'token': token_second, 'channel_id': channel_id})
    assert response.status_code == OKAY

    response = requests.post(f"{url}/channel/leave/v1", json={'token': token, 'channel_id': channel_id})
    assert response.status_code == OKAY

    response = requests.get(f"{url}/channel/details/v2", params={'token': token_second, 'channel_id': channel_id})
    assert response.status_code == OKAY
    details_list = response.json()
    assert len(details_list['all_members']) == 1

def test_channel_leave_token_error(setup):
    channel_dict = setup[2]

    channel_id = channel_dict['channel_id']

    response = requests.post(f"{url}/channel/leave/v1", json={'token': 'invalidtoken', 'channel_id': channel_id})
    assert response.status_code == AccessError.code

def test_channel_leave_invalid_channel_id(setup):
    user_dict = setup[0]
    channel_dict = setup[2]

    token = user_dict['token']
    channel_id = channel_dict['channel_id']

    response = requests.post(f"{url}/channel/leave/v1", json={'token': token, 'channel_id': channel_id+100})
    assert response.status_code == InputError.code

def test_channel_leave_not_member(setup):
    user_dict = setup[1]
    channel_dict = setup[2]

    token = user_dict['token']
    channel_id = channel_dict['channel_id']

    response = requests.post(f"{url}/channel/leave/v1", json={'token': token, 'channel_id': channel_id})
    assert response.status_code == AccessError.code

def test_global_owner_non_member_cant_addowner_private(setup):
    user1_dict = setup[0]
    channel2_dict = setup[3]

    response = requests.post(f"{url}/channel/addowner/v1", json={"token": user1_dict['token'], "channel_id": channel2_dict['channel_id'], "u_id": user1_dict['auth_user_id']})
    assert response.status_code == AccessError.code

def test_global_owner_non_member_cant_addowner_public(setup):
    user1_dict = setup[0]
    user2_dict = setup[1]

    channel2_obj = requests.post(f'{url}/channels/create/v2', json={"token": user2_dict['token'], "name": "my_channel", "is_public": True})
    channel2_dict = channel2_obj.json()

    response = requests.post(f"{url}/channel/addowner/v1", json={"token": user1_dict['token'], "channel_id": channel2_dict['channel_id'], "u_id": user1_dict['auth_user_id']})
    assert response.status_code == AccessError.code

def test_global_owner_cannot_remove_only_owner(setup):
    user1_dict = setup[0]
    user2_dict = setup[1]

    channel2_obj = requests.post(f'{url}/channels/create/v2', json={"token": user2_dict['token'], "name": "my_channel", "is_public": True})
    channel2_dict = channel2_obj.json()

    response = requests.post(f"{url}/channel/join/v2", json={'token': user1_dict['token'], "channel_id": channel2_dict['channel_id']})
    assert response.status_code == OKAY

    response = requests.post(f"{url}/channel/removeowner/v1", json={"token": user1_dict['token'], "channel_id": channel2_dict['channel_id'], "u_id": user2_dict['auth_user_id']})
    assert response.status_code == InputError.code

def test_global_owner_nonmember_cannot_remove_owner(setup):
    user1_dict = setup[0]
    user2_dict = setup[1]
    user3_obj = requests.post(f'{url}/auth/register/v2', json={"email": "howareyou@outlook.com", "password": "hey12345678", "name_first": "Bruces", "name_last": "Banners"})
    user3_dict = user3_obj.json()

    channel2_obj = requests.post(f'{url}/channels/create/v2', json={"token": user2_dict['token'], "name": "my_channel", "is_public": True})
    channel2_dict = channel2_obj.json()

    response = requests.post(f"{url}/channel/join/v2", json={'token': user3_dict['token'], "channel_id": channel2_dict['channel_id']})
    assert response.status_code == OKAY

    response = requests.post(f"{url}/channel/addowner/v1", json={"token": user2_dict['token'], "channel_id": channel2_dict['channel_id'], "u_id": user3_dict['auth_user_id']})
    assert response.status_code == OKAY

    response = requests.post(f"{url}/channel/removeowner/v1", json={"token": user1_dict['token'], "channel_id": channel2_dict['channel_id'], "u_id": user3_dict['auth_user_id']})
    assert response.status_code == AccessError.code

