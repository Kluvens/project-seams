import pytest
import requests
from src import message
from src.config import url
from src.error import InputError, AccessError
from tests.http_helpers import GenerateTestData

def reset_call():
    requests.delete(url + 'clear/v1')

def send_message_request(token, channel_id, message):
    response = requests.post(url + "/message/send/v1", 
        json={
            "token" : token,
            "channel_id" : channel_id,
            "message" : message,
        })

    return response

@pytest.fixture
def create_route():
    return url + "channels/create/v2"

def get_channel_messages(token, channel_id, start):
    response = requests.get(url + "/channel/messages/v2",
        params={
            "token" : token,
            "channel_id" : channel_id,
            "start" : start,
        })
    return response

def post_channel_invite(token, channel_id, u_id):
    response = requests.post(url + "/channel/invite/v2",
        json={
            "token" : token,
            "channel_id" : channel_id,
            "u_id" : u_id,
        })
    return response

def delete_message_remove(token, message_id):
    response = requests.delete(url + "/message/remove/v1",
        json={
            "token" : token,
            "message_id" : message_id,
        })
    return response

'''
InputError when message is less than 1
'''
def test_channelmessages_less_than_one(dummy_data, create_route):
    reset_call()

    users_list = dummy_data.register_users(num_of_users=1)
    user0 = users_list[0]
    ch1 = requests.post(create_route, json={
        'token': user0["token"],
        'name': 'ch1',
        'is_public': True
    })
    assert ch1.status_code == 200
    ch1_dict = ch1.json()

    message = ''
    response = send_message_request(user0['token'], ch1_dict['channel_id'], message)
    assert response.status_code == InputError.code

'''
InputError when message is more than 1000
'''
def test_channelmessages_more_than_thousand(dummy_data, create_route):
    reset_call()

    users_list = dummy_data.register_users(num_of_users=1)
    user0 = users_list[0]
    ch1 = requests.post(create_route, json={
        'token': user0["token"],
        'name': 'ch1',
        'is_public': True
    })
    assert ch1.status_code == 200
    ch1_dict = ch1.json()

    message = 'hello'*500
    response = send_message_request(user0['token'], ch1_dict['channel_id'], message)
    assert response.status_code == InputError.code

def test_channel_messages_invalid_token(dummy_data, create_route):
    reset_call()

    users_list = dummy_data.register_users(num_of_users=1)
    user0 = users_list[0]
    ch1 = requests.post(create_route, json={
        'token': user0["token"],
        'name': 'ch1',
        'is_public': True
    })
    assert ch1.status_code == 200
    ch1_dict = ch1.json()

    message = 'hello, how are you'
    response = send_message_request("invalid_token", ch1_dict['channel_id'], message)
    assert response.status_code == AccessError.code

'''
channel doesn't exist
'''
def test_channel_messages_channel_doesnot_exist(dummy_data):
    reset_call()

    users_list = dummy_data.register_users(num_of_users=1)
    user0 = users_list[0]

    message = 'hello, how are you'
    response = send_message_request(user0['token'], 0, message)
    assert response.status_code == InputError.code

'''
not authorised user
'''
def test_channel_messages_not_auth(dummy_data, create_route):
    reset_call()

    users_list = dummy_data.register_users(num_of_users=2)
    user0 = users_list[0]
    user1 = users_list[1]
    ch1 = requests.post(create_route, json={
        'token': user0["token"],
        'name': 'ch1',
        'is_public': True
    })
    assert ch1.status_code == 200
    ch1_dict = ch1.json()

    message = 'hello, how are you'
    response = send_message_request(user1['token'], ch1_dict['channel_id'], message)
    assert response.status_code == AccessError.code

'''
InputError will occur when message_id is not a valid channel message within a channel/DM
'''
# Testing case for when message_id is invalid
def test_channel_messages_remove_invalid_message_id_InputError(dummy_data, create_route):
    reset_call()

    users_list = dummy_data.register_users(num_of_users=1)
    user0 = users_list[0]
    ch1 = requests.post(create_route, json={
        'token': user0["token"],
        'name': 'ch1',
        'is_public': True
    })
    assert ch1.status_code == 200
    ch1_dict = ch1.json()

    message = "hello world bye world"
    send_message_request(user0['token'], ch1_dict['channel_id'], message)

    response = delete_message_remove(user0['token'], -1)
    assert response.status_code == 400

'''
AccessError will occur when a user is not a member/owner of a valid channel_id or either not a global owner
or if token is invalid
'''
@pytest.mark.parametrize("invalid_token", ["Hello", "-1", -1, "35235gfdsgfdsh"])
# Testing case for when the token is invalid
def test_channel_messages_remove_invalid_token_AccessError(dummy_data, create_route, invalid_token):
    reset_call()

    users_list = dummy_data.register_users(num_of_users=1)
    user0 = users_list[0]
    ch1 = requests.post(create_route, json={
        'token': user0["token"],
        'name': 'ch1',
        'is_public': True
    })
    assert ch1.status_code == 200
    ch1_dict = ch1.json()

    message = "hello world bye world"
    send_message = send_message_request(user0['token'], ch1_dict['channel_id'], message)
    send_message = send_message.json()
    
    response = delete_message_remove(invalid_token, send_message["message_id"])
    assert response.status_code == AccessError.code

# Testing case when authorised user is not a member of the valid channel_id
def test_channel_messages_remove_unauthorised_user_AccessError(dummy_data, create_route):
    reset_call()

    users_list = dummy_data.register_users(num_of_users=2)
    user0 = users_list[0]
    user1 = users_list[1]
    ch1 = requests.post(create_route, json={
        'token': user0["token"],
        'name': 'ch1',
        'is_public': True
    })
    assert ch1.status_code == 200
    ch1_dict = ch1.json()

    message = "hello world"
    send_message = send_message_request(user0['token'], ch1_dict['channel_id'], message)
    send_message = send_message.json()

    response = delete_message_remove(user1['token'], send_message["message_id"])
    assert response.status_code == AccessError.code

# Testing case when message_remove is working
def test_channel_messages_remove_working(dummy_data, create_route):
    reset_call()
    
    users_list = dummy_data.register_users(num_of_users=2)
    user0 = users_list[0]
    user1 = users_list[1]
    ch1 = requests.post(create_route, json={
        'token': user0["token"],
        'name': 'ch1',
        'is_public': True
    })
    assert ch1.status_code == 200
    ch1_dict = ch1.json()

    post_channel_invite(user0["token"], ch1_dict['channel_id'], user1['auth_user_id'])
    message_one = "hello world"
    message_two = "bye world"
    message_three = "hello darkness"

    # Send message from owner of channel
    response1 = send_message_request(user0['token'], ch1_dict['channel_id'], message_one)
    # Send message from member of channel
    response2 = send_message_request(user1['token'], ch1_dict['channel_id'], message_two)

    send_message_request(user0['token'], ch1_dict['channel_id'], message_three)

    send_message_one = response1.json()
    send_message_two = response2.json()

    # Remove messages 1 and 2 from channel
    delete_message_remove(user0['token'], send_message_one["message_id"])
    delete_message_remove(user1['token'], send_message_two["message_id"])
    
    messages_output = get_channel_messages(user0['token'], ch1_dict['channel_id'], 0)
    messages_output = messages_output.json()
    
    assert messages_output['messages'][0]['message'] == message_three
