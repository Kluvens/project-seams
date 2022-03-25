import requests
from requests import HTTPError
import pytest
from src.config import url

Access_Error = 403
Input_Error = 400

@pytest.fixture
def setup():
    # setup data_store
    requests.delete(f'{url}/clear/v1')

    # first user
    user1_obj = requests.post(f'{url}/auth/register/v2', json={"email": "unswisgreat@unsw.edu.au", "password": "unsw123456", "name_first": "Tony", "name_last": "Stark"})
    assert user1_obj.status_code == 200
    user1_dict = user1_obj.json()

    # second user
    user2_obj =  requests.post(f'{url}/auth/register/v2', json={"email": "hellounsw@gmail.com", "password": "hey123456", "name_first": "Bruce", "name_last": "Banner"})
    user2_dict = user2_obj.json()

    # create first channel
    channel1_obj = requests.post(f'{url}/channels/create/v2', json={"token": user1_dict['token'], "channel_name": "Kias_channel", "is_public": True})
    channel1_dict = channel1_obj.json()

    # create second channel
    channel2_obj = requests.post(f'{url}/channels/create/v2', json={"token": user2_dict['token'], "channel_name": "my_channel", "is_public": False})
    channel2_dict = channel2_obj.json()

    return [user1_dict, user2_dict, channel1_dict, channel2_dict]

def test_channel_create_token_error(setup):
    user_dict = setup[0]
    token = user_dict['token']
    assert isinstance(token, str)

    response = requests.post(f"{url}/channels/create/v2", json={"token": 'invalid_token', "channel_name": "Kias_channel", "is_public": True})
    assert response.status_code == Access_Error

def test_channel_create_inputError_less_than_1(setup):
    user_dict = setup[0]
    token = user_dict['token']

    response = requests.post(f"{url}/channels/create/v2", json={"token": token, "channel_name": "", "is_public": False})
    assert response.status_code == Input_Error  

def test_channel_create_inputError_more_than_20(setup):
    user_dict = setup[0]
    token = user_dict['token']

    response = requests.post(f"{url}/channels/create/v2", json={"token": token, "channel_name": "hahahahahaahahahahahamustbemorethantwentyletters", "is_public": False})
    assert response.status_code == Input_Error

def test_channel_details_working_single_member(setup):
    user_dict = setup[0]
    channel_dict = setup[2]

    token = user_dict['token']
    auth_user_id = user_dict['auth_user_id']
    channel_id = channel_dict['channel_id']

    response = requests.get(f'{url}/channel/details/v2', params={'token': token, 'channel_id': channel_id})
    assert response.status_code == 200
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
    assert response.status_code == 200
    
    response = requests.get(f'{url}/channel/details/v2', params={'token': token, 'channel_id': channel_id})
    assert response.status_code == 200
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
    assert response.status_code == 403
    
def test_channel_details_invalid_channel_id(setup):
    user_dict = setup[0]
    channel_dict = setup[2]

    token = user_dict['token']
    channel_id = channel_dict['channel_id']

    response = requests.get(f'{url}/channel/details/v2', params={'token': token, 'channel_id': channel_id+100})    
    assert response.status_code == Input_Error

def test_channel_details_invalid_auth_id(setup):
    user2_dict = setup[1]
    channel_dict = setup[2]

    token_second = user2_dict['token']
    channel_id = channel_dict['channel_id']

    response = requests.get(f"{url}/channel/details/v2", params={"token": token_second, "channel_id": channel_id})
    assert response.status_code == Access_Error

def test_add_owner_working(setup):
    user1_dict = setup[0]
    user2_dict = setup[1]
    channel_dict = setup[2]

    token = user1_dict['token']
    auth_user_id = user1_dict['auth_user_id']
    channel_id = channel_dict['channel_id']
    u_id = user2_dict['auth_user_id']

    response = requests.post(f'{url}/channel/invite/v2', json={'token': token, 'channel_id': channel_id, 'u_id': u_id})
    assert response.status_code == 200

    response = requests.post(f"{url}/channel/addowner/v1", json={"token": token, "channel_id": channel_id, "u_id": u_id})
    response.status_code == 200

    response = requests.get(f"{url}/channel/details/v2", params={"token": token, "channel_id": channel_id})
    assert response.status_code == 200
    
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
    assert response.status_code == 200

    response = requests.post(f"{url}/channel/addowner/v1", json={"token": "invalid_token", "channel_id": channel_id, "u_id": u_id})
    assert response.status_code == Access_Error

def test_add_owner_channel_id_invalid(setup):
    user1_dict = setup[0]
    user2_dict = setup[1]
    channel_dict = setup[2]

    token = user1_dict['token']
    u_id = user2_dict['auth_user_id']
    channel_id = channel_dict['channel_id']

    response = requests.post(f"{url}/channel/invite/v2", json={"token": token, "channel_id": channel_id, "u_id": u_id})
    assert response.status_code == 200

    response = requests.post(f"{url}/channel/addowner/v1", json={"token": token, "channel_id": channel_id+100, "u_id": u_id})
    assert response.status_code == Input_Error

def test_add_owner_u_id_invalid(setup):
    user1_dict = setup[0]
    user2_dict = setup[1]
    channel_dict = setup[2]

    token = user1_dict['token']
    u_id = user2_dict['auth_user_id']
    channel_id = channel_dict['channel_id']

    response = requests.post(f"{url}/channel/invite/v2", json={"token": token, "channel_id": channel_id, "u_id": u_id})
    assert response.status_code == 200

    response = requests.post(f"{url}/channel/addowner/v1", json={"token": token, "channel_id": channel_id, "u_id": u_id+100})
    assert response.status_code == Input_Error

def test_add_owner_u_id_not_member(setup):
    user1_dict = setup[0]
    user2_dict = setup[1]
    channel_dict = setup[2]

    token = user1_dict['token']
    u_id = user2_dict['auth_user_id']
    channel_id = channel_dict['channel_id']

    response = requests.post(f"{url}/channel/addowner/v1", json={"token": token, "channel_id": channel_id, "u_id": u_id})
    assert response.status_code == Input_Error

def test_add_owner_u_id_already_owner(setup):
    user1_dict = setup[0]
    user2_dict = setup[1]
    channel_dict = setup[2]

    token = user1_dict['token']
    u_id = user2_dict['auth_user_id']
    channel_id = channel_dict['channel_id']

    response = requests.post(f'{url}/channel/invite/v2', json={'token': token, 'channel_id': channel_id, 'u_id': u_id})
    assert response.status_code == 200

    response = requests.post(f"{url}/channel/addowner/v1", json={"token": token, "channel_id": channel_id, "u_id": u_id})
    response.status_code == 200

    response = requests.post(f"{url}/channel/addowner/v1", json={"token": token, "channel_id": channel_id, "u_id": u_id})
    assert response.status_code == Input_Error

def test_add_owner_no_permission(setup):
    pass

def test_remove_owner_working(setup):
    user1_dict = setup[0]
    user2_dict = setup[1]
    channel_dict = setup[2]

    token = user1_dict['token']
    auth_user_id = user1_dict['auth_user_id']
    channel_id = channel_dict['channel_id']
    u_id = user2_dict['auth_user_id']

    response = requests.post(f'{url}/channel/invite/v2', json={'token': token, 'channel_id': channel_id, 'u_id': u_id})
    assert response.status_code == 200

    response = requests.post(f"{url}/channel/addowner/v1", json={"token": token, "channel_id": channel_id, "u_id": u_id})
    response.status_code == 200

    response = requests.post(f"{url}/channel/removeowner/v1", json={"token": token, "channel_id": channel_id, "u_id": u_id})
    assert response.status_code == 200

    response = requests.get(f"{url}/channel/details/v2", params={"token": token, "channel_id": channel_id})
    assert response.status_code == 200

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
    assert response.status_code == 200

    response = requests.post(f"{url}/channel/addowner/v1", json={"token": token, "channel_id": channel_id, "u_id": u_id})
    response.status_code == 200

    response = requests.post(f"{url}/channel/removeowner/v1", json={"token": "invalidtoken", "channel_id": channel_id, "u_id": u_id})
    assert response.status_code == Access_Error

def test_remove_owner_channel_id_invalid(setup):
    user1_dict = setup[0]
    user2_dict = setup[1]
    channel_dict = setup[2]

    token = user1_dict['token']
    channel_id = channel_dict['channel_id']
    u_id = user2_dict['auth_user_id']

    response = requests.post(f'{url}/channel/invite/v2', json={'token': token, 'channel_id': channel_id, 'u_id': u_id})
    assert response.status_code == 200

    response = requests.post(f"{url}/channel/addowner/v1", json={"token": token, "channel_id": channel_id, "u_id": u_id})
    response.status_code == 200

    response = requests.post(f"{url}/channel/removeowner/v1", json={"token": token, "channel_id": channel_id+100, "u_id": u_id})
    assert response.status_code == Input_Error

def test_remove_owner_u_id_invalid(setup):
    user1_dict = setup[0]
    user2_dict = setup[1]
    channel_dict = setup[2]

    token = user1_dict['token']
    channel_id = channel_dict['channel_id']
    u_id = user2_dict['auth_user_id']

    response = requests.post(f"{url}/channel/removeowner/v1", json={"token": token, "channel_id": channel_id, "u_id": u_id+100})
    assert response.status_code == Input_Error

def test_remove_owner_u_id_not_member(setup):
    user1_dict = setup[0]
    user2_dict = setup[1]
    channel_dict = setup[2]

    token = user1_dict['token']
    channel_id = channel_dict['channel_id']
    u_id = user2_dict['auth_user_id']

    response = requests.post(f"{url}/channel/removeowner/v1", json={"token": token, "channel_id": channel_id, "u_id": u_id})
    assert response.status_code == Input_Error

def test_remove_owner_u_id_the_only_owner(setup):
    user1_dict = setup[0]
    channel_dict = setup[2]

    token = user1_dict['token']
    channel_id = channel_dict['channel_id']
    auth_user_id = user1_dict['auth_user_id']

    response = requests.post(f"{url}/channel/removeowner/v1", json={"token": token, "channel_id": channel_id, "u_id": auth_user_id})
    assert response.status_code == Input_Error

def test_remove_owner_no_permission(setup):
    pass
