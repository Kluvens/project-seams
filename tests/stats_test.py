import requests
from requests import HTTPError
import pytest
from src.config import url
from src.error import InputError, AccessError
from src.auth import auth_register_v2, auth_logout_v1
from src.channels import channels_create_v2
from src.dms import dm_create_v1
from src.message import message_senddm_v1

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

    response = requests.get(f'{url}/user/stats/v1', params={'token': user1_dict['token']})
    assert response.status_code == OKAY
    stats_result = response.json()
    assert stats_result['user_stats']['involvement_rate'] == float(0)

    # second user
    user2_obj =  requests.post(f'{url}/auth/register/v2', json={"email": "hellounsw@gmail.com", "password": "hey123456", "name_first": "Bruce", "name_last": "Banner"})
    assert user2_obj.status_code == OKAY
    user2_dict = user2_obj.json()
    assert isinstance(user2_dict, dict)

    # third user
    user3_obj =  requests.post(f'{url}/auth/register/v2', json={"email": "kais@gmail.com", "password": "hey123456", "name_first": "Kais", "name_last": "Alz"})
    assert user3_obj.status_code == OKAY
    user3_dict = user3_obj.json()
    assert isinstance(user3_dict, dict)

    # fourth user
    user4_obj =  requests.post(f'{url}/auth/register/v2', json={"email": "james@gmail.com", "password": "hey123456", "name_first": "James", "name_last": "Cai"})
    assert user4_obj.status_code == OKAY
    user4_dict = user4_obj.json()
    assert isinstance(user4_dict, dict)

    channel_obj = requests.post(f'{url}/channels/create/v2', json={"token": user1_dict['token'], "name": "Kias_channel", "is_public": True})
    assert channel_obj.status_code == OKAY
    channel_dict = channel_obj.json()

    response = requests.post(f'{url}/channel/join/v2', json={'token': user2_dict['token'], 'channel_id': channel_dict['channel_id']})
    assert response.status_code == OKAY

    dm_obj = requests.post(f'{url}/dm/create/v1', json={'token': user1_dict['token'], 'u_ids': [user2_dict['auth_user_id'], user3_dict['auth_user_id']]})
    assert dm_obj.status_code == OKAY
    dm_dict = dm_obj.json()

    return [user1_dict, user2_dict, user3_dict, user4_dict, channel_dict, dm_dict]

def test_user_stats_invalid_token(setup):
    user1_dict = setup[0]

    token = user1_dict['token']

    response = requests.post(f'{url}/auth/logout/v1', json={'token': token})
    assert response.status_code == OKAY

    response = requests.get(f'{url}/user/stats/v1', params={'token': token})
    assert response.status_code == AccessError.code

def test_user_stats_working(setup):
    user1_dict = setup[0]
    user2_dict = setup[1]
    user3_dict = setup[2]
    user4_dict = setup[3]
    channel_dict = setup[4]
    dm_dict = setup[5]

    token = user1_dict['token']
    token_second = user2_dict['token']
    token_third = user3_dict['token']
    token_fourth = user4_dict['token']

    response = requests.get(f'{url}/user/stats/v1', params={'token': token})
    assert response.status_code == OKAY

    stats_result = response.json()
    assert isinstance(stats_result,dict)

    assert isinstance(stats_result['user_stats']["channels_joined"][0], dict) 
    assert len(stats_result['user_stats']["channels_joined"]) == 1
    assert len(stats_result['user_stats']["dms_joined"]) == 1
    assert len(stats_result['user_stats']["messages_sent"]) == 0
    assert isinstance(stats_result['user_stats']['involvement_rate'], float)

    response = requests.post(f'{url}/message/send/v1', json={'token': token, 'channel_id': channel_dict['channel_id'], 'message': "I love you"})
    assert response.status_code == OKAY

    response = requests.post(f'{url}/message/senddm/v1', json={'token': token, 'dm_id': dm_dict['dm_id'], 'message': "I love you"})
    assert response.status_code == OKAY

    response = requests.get(f'{url}/user/stats/v1', params={'token': token})
    assert response.status_code == OKAY

    stats_result = response.json()
    assert isinstance(stats_result,dict)

    assert isinstance(stats_result['user_stats']["channels_joined"][0], dict) 
    assert len(stats_result['user_stats']["channels_joined"]) == 1
    assert len(stats_result['user_stats']["dms_joined"]) == 1
    assert len(stats_result['user_stats']["messages_sent"]) == 2
    assert stats_result['user_stats']['involvement_rate'] == float(1)

    response = requests.get(f'{url}/user/stats/v1', params={'token': token_second})
    assert response.status_code == OKAY

    stats_result = response.json()
    assert isinstance(stats_result,dict)

    assert len(stats_result['user_stats']["channels_joined"]) == 1
    assert len(stats_result['user_stats']["dms_joined"]) == 1
    assert len(stats_result['user_stats']["messages_sent"]) == 0
    assert stats_result['user_stats']['involvement_rate'] == float(0.5)

    response = requests.get(f'{url}/user/stats/v1', params={'token': token_third})
    assert response.status_code == OKAY

    stats_result = response.json()
    assert isinstance(stats_result,dict)

    assert len(stats_result['user_stats']["channels_joined"]) == 0
    assert len(stats_result['user_stats']["dms_joined"]) == 1
    assert len(stats_result['user_stats']["messages_sent"]) == 0
    assert stats_result['user_stats']['involvement_rate'] == float(0.25)

    response = requests.get(f'{url}/user/stats/v1', params={'token': token_fourth})
    assert response.status_code == OKAY

    stats_result = response.json()
    assert isinstance(stats_result,dict)

    assert len(stats_result['user_stats']["channels_joined"]) == 0
    assert len(stats_result['user_stats']["dms_joined"]) == 0
    assert len(stats_result['user_stats']["messages_sent"]) == 0
    assert stats_result['user_stats']['involvement_rate'] == float(0)

    channel_obj = requests.post(f'{url}/channels/create/v2', json={"token": token_second, "name": "Kias_channel", "is_public": True})
    assert channel_obj.status_code == OKAY
    channel_second_dict = channel_obj.json()

    response = requests.post(f'{url}/message/send/v1', json={'token': token_second, 'channel_id': channel_second_dict['channel_id'], 'message': "I love you"})
    assert response.status_code == OKAY

    for _ in range(10):
        response = requests.post(f'{url}/message/send/v1', json={'token': token, 'channel_id': channel_second_dict['channel_id'], 'message': "ten more messages"})
        assert response.status_code == OKAY

    for _ in range(10):
        response = requests.post(f'{url}/message/senddm/v1', json={'token': token, 'dm_id': dm_dict['dm_id'], 'message': "I love you"})
        assert response.status_code == OKAY

    response = requests.get(f'{url}/user/stats/v1', params={'token': token})
    assert response.status_code == OKAY

    stats_result = response.json()
    assert isinstance(stats_result,dict)

    assert isinstance(stats_result['user_stats']["channels_joined"][0], dict) 
    assert len(stats_result['user_stats']["channels_joined"]) == 1
    assert len(stats_result['user_stats']["dms_joined"]) == 1
    assert len(stats_result['user_stats']["messages_sent"]) == 2 + 10 + 10
    assert stats_result['user_stats']['involvement_rate'] == float((1+1+2+10+10)/(2+1+3+10+10))

def test_users_stats_invalid_token(setup):
    user1_dict = setup[0]

    token = user1_dict['token']

    response = requests.post(f'{url}/auth/logout/v1', json={'token': token})
    assert response.status_code == OKAY

    response = requests.get(f'{url}/users/stats/v1', params={'token': token})
    assert response.status_code == AccessError.code

def test_usersstats_working(setup):
    user1_dict = setup[0]
    user2_dict = setup[1]
    user3_dict = setup[2]
    user4_dict = setup[3]

    token = user1_dict['token']
    
    response = requests.get(f'{url}/users/stats/v1', params={'token': token})
    assert response.status_code == OKAY

    stats_result = response.json()
    assert isinstance(stats_result,dict)

    assert len(stats_result['workspace_stats']["channels_exist"]) == 1
    assert len(stats_result['workspace_stats']["dms_exist"]) == 1
    assert len(stats_result['workspace_stats']["messages_exist"]) == 0
    assert stats_result['workspace_stats']['utilization_rate'] == float(3/4)