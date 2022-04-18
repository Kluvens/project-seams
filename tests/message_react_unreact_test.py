import pytest
import requests
from src.config import url
from src.error import InputError, AccessError
from tests.http_helpers import GenerateTestData

OKAY = 200

def reset_call():
    requests.delete(url + 'clear/v1')

def message_react_request(token, message_id, react_id):
    response = requests.post(url + "/message/react/v1", 
        json={
            "token" : token,
            "message_id" : message_id,
            "react_id" : react_id,
        })
    return response

def message_unreact_request(token, message_id, react_id):
    response = requests.post(url + "/message/unreact/v1", 
        json={
            "token" : token,
            "message_id" : message_id,
            "react_id" : react_id,
        })
    return response

def send_message_request(token, channel_id, message):
    response = requests.post(url + "/message/send/v1", 
        json={
            "token" : token,
            "channel_id" : channel_id,
            "message" : message,
        })
    return response

def send_dm_message_request(token, dm_id, message):
    response = requests.post(url + "/message/senddm/v1", 
        json={
            "token" : token,
            "dm_id" : dm_id,
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

'''
InputError will occur when message_id is not a valid channel message within a channel/DM or react_id is not valid or message is already reacted
'''
# Testing case for when message_id is invalid
@pytest.mark.parametrize("invalid_message_id", [-9999, -55, 145, 9999])
def test_react_invalid_message_id_InputError(dummy_data, create_route, invalid_message_id):
    reset_call()

    users_list = dummy_data.register_users(num_of_users=1)
    user0 = users_list[0]
    ch1 = requests.post(create_route, json={
        'token': user0["token"],
        'name': 'ch1',
        'is_public': True
    })
    assert ch1.status_code == OKAY
    ch1_dict = ch1.json()

    message = "hello world bye world"
    send_message_request(user0['token'], ch1_dict['channel_id'], message)

    response = message_react_request(user0['token'], invalid_message_id, 1)
    assert response.status_code == InputError.code

@pytest.mark.parametrize("invalid_message_id", [-9999, -55, 145, 9999])
def test_react_invalid_dm_message_id_InputError(dummy_data, invalid_message_id):
    reset_call()

    users_list = dummy_data.register_users(num_of_users=1)
    user0 = users_list[0]
    dm_dict = dummy_data.create_dm(user0['token'], [users_list[0]['auth_user_id']])
    message = "hello world bye world"
    send_dm_message_request(user0['token'], dm_dict['dm_id'], message)

    response = message_react_request(user0['token'], invalid_message_id, 1)
    assert response.status_code == InputError.code

@pytest.mark.parametrize("invalid_react_id", [-9999, -55, 145, 9999])
def test_react_invalid_token_InputError(dummy_data, create_route, invalid_react_id):
    reset_call()

    users_list = dummy_data.register_users(num_of_users=1)
    user0 = users_list[0]
    ch1 = requests.post(create_route, json={
        'token': user0["token"],
        'name': 'ch1',
        'is_public': True
    })
    assert ch1.status_code == OKAY
    ch1_dict = ch1.json()

    message = "hello world bye world"
    send_message = send_message_request(user0['token'], ch1_dict['channel_id'], message)
    send_message = send_message.json()
    
    response = message_react_request(user0['token'], send_message['message_id'], invalid_react_id)
    assert response.status_code == InputError.code

@pytest.mark.parametrize("invalid_react_id", [-9999, -55, 145, 9999])
def test_dm_react_invalid_token_InputError(dummy_data, invalid_react_id):
    reset_call()

    users_list = dummy_data.register_users(num_of_users=1)
    user0 = users_list[0]
    dm_dict = dummy_data.create_dm(user0['token'], [users_list[0]['auth_user_id']])

    message = "hello world bye world"
    send_message = send_dm_message_request(user0['token'], dm_dict['dm_id'], message)
    send_message = send_message.json()
    
    response = message_react_request(user0['token'], send_message['message_id'], invalid_react_id)
    assert response.status_code == InputError.code

def test_react_already_InputError(dummy_data, create_route):
    '''
    Testing when user has already reacted the message.
    '''
    reset_call()

    users_list = dummy_data.register_users(num_of_users=1)
    user0 = users_list[0]
    ch1 = requests.post(create_route, json={
        'token': user0["token"],
        'name': 'ch1',
        'is_public': True
    })
    assert ch1.status_code == OKAY
    ch1_dict = ch1.json()

    message = "hello world bye world"
    send_message = send_message_request(user0['token'], ch1_dict['channel_id'], message)
    send_message = send_message.json()

    message_react_request(user0['token'], send_message['message_id'], 1)

    response = message_react_request(user0['token'], send_message['message_id'], 1)
    assert response.status_code == InputError.code

def test_dm_react_already_InputError(dummy_data):
    '''
    Testing when user has already reacted the message.
    '''
    reset_call()

    users_list = dummy_data.register_users(num_of_users=1)
    user0 = users_list[0]
    dm_dict = dummy_data.create_dm(user0['token'], [users_list[0]['auth_user_id']])

    message = "hello world bye world"
    send_message = send_dm_message_request(user0['token'], dm_dict['dm_id'], message)
    send_message = send_message.json()

    message_react_request(user0['token'], send_message['message_id'], 1)

    response = message_react_request(user0['token'], send_message['message_id'], 1)
    assert response.status_code == InputError.code

'''
AccessError will occur when a user is not a member/owner of a valid channel_id or either not a global owner
or if token is invalid
'''
@pytest.mark.parametrize("invalid_token", ["Hello", "-1", -1, "35235gfdsgfdsh"])
# Testing case for when the token is invalid
def test_react_invalid_token_AccessError(dummy_data, create_route, invalid_token):
    reset_call()

    users_list = dummy_data.register_users(num_of_users=1)
    user0 = users_list[0]
    ch1 = requests.post(create_route, json={
        'token': user0["token"],
        'name': 'ch1',
        'is_public': True
    })
    assert ch1.status_code == OKAY
    ch1_dict = ch1.json()

    message = "hello world bye world"
    send_message = send_message_request(user0['token'], ch1_dict['channel_id'], message)
    send_message = send_message.json()
    
    response = message_react_request(invalid_token, send_message['message_id'], 1)
    assert response.status_code == AccessError.code

@pytest.mark.parametrize("invalid_token", ["Hello", "-1", -1, "35235gfdsgfdsh"])
def test_dm_react_invalid_token_AccessError(dummy_data, invalid_token):
    reset_call()

    users_list = dummy_data.register_users(num_of_users=1)
    user0 = users_list[0]
    dm_dict = dummy_data.create_dm(user0['token'], [users_list[0]['auth_user_id']])

    message = "hello world bye world"
    send_message = send_dm_message_request(user0['token'], dm_dict['dm_id'], message)
    send_message = send_message.json()
    
    response = message_react_request(invalid_token, send_message['message_id'], 1)
    assert response.status_code == AccessError.code


################################# Unreact #################################

'''
InputError will occur when message_id is not a valid channel message within a channel/DM or react_id is not valid or message is hasn't been reacted
'''
# Testing case for when message_id is invalid
@pytest.mark.parametrize("invalid_message_id", [-9999, -55, 145, 9999])
def test_react_invalid_message_id_InputError(dummy_data, create_route, invalid_message_id):
    reset_call()

    users_list = dummy_data.register_users(num_of_users=1)
    user0 = users_list[0]
    ch1 = requests.post(create_route, json={
        'token': user0["token"],
        'name': 'ch1',
        'is_public': True
    })
    assert ch1.status_code == OKAY
    ch1_dict = ch1.json()

    message = "hello world bye world"
    send_message = send_message_request(user0['token'], ch1_dict['channel_id'], message)
    send_message = send_message.json()
    message_react_request(user0['token'], send_message['message_id'], 1)
    
    response = message_unreact_request(user0['token'], invalid_message_id, 1)
    assert response.status_code == InputError.code

@pytest.mark.parametrize("invalid_message_id", [-9999, -55, 145, 9999])
def test_dm_unreact_invalid_dm_message_id_InputError(dummy_data, invalid_message_id):
    reset_call()

    users_list = dummy_data.register_users(num_of_users=1)
    user0 = users_list[0]
    dm_dict = dummy_data.create_dm(user0['token'], [users_list[0]['auth_user_id']])
    message = "hello world bye world"
    
    send_message = send_dm_message_request(user0['token'], dm_dict['dm_id'], message)
    send_message = send_message.json()
    message_react_request(user0['token'], send_message['message_id'], 1)

    response = message_unreact_request(user0['token'], invalid_message_id, 1)
    assert response.status_code == InputError.code


@pytest.mark.parametrize("invalid_react_id", [-9999, -55, 549, 9999])
def test_unreact_invalid_token_InputError(dummy_data, create_route, invalid_react_id):
    reset_call()

    users_list = dummy_data.register_users(num_of_users=1)
    user0 = users_list[0]
    ch1 = requests.post(create_route, json={
        'token': user0["token"],
        'name': 'ch1',
        'is_public': True
    })
    assert ch1.status_code == OKAY
    ch1_dict = ch1.json()

    message = "hello world bye world"
    send_message = send_message_request(user0['token'], ch1_dict['channel_id'], message)
    send_message = send_message.json()
    message_react_request(user0['token'], send_message['message_id'], 1)

    response = message_unreact_request(user0['token'], send_message['message_id'], invalid_react_id)
    assert response.status_code == InputError.code

@pytest.mark.parametrize("invalid_react_id", [-9999, -55, 549, 9999])
def test_dm_unreact_invalid_token_InputError(dummy_data, invalid_react_id):
    reset_call()

    users_list = dummy_data.register_users(num_of_users=1)
    user0 = users_list[0]
    dm_dict = dummy_data.create_dm(user0['token'], [users_list[0]['auth_user_id']])
    message = "hello world bye world"

    send_message = send_dm_message_request(user0['token'], dm_dict['dm_id'], message)
    send_message = send_message.json()
    message_react_request(user0['token'], send_message['message_id'], 1)

    response = message_unreact_request(user0['token'], send_message['message_id'], invalid_react_id)
    assert response.status_code == InputError.code

def test_unreact_already_InputError(dummy_data, create_route):
    '''
    Testing when user has already reacted the message.
    '''
    reset_call()

    users_list = dummy_data.register_users(num_of_users=1)
    user0 = users_list[0]
    ch1 = requests.post(create_route, json={
        'token': user0["token"],
        'name': 'ch1',
        'is_public': True
    })
    assert ch1.status_code == OKAY
    ch1_dict = ch1.json()

    message = "hello world bye world"
    send_message = send_message_request(user0['token'], ch1_dict['channel_id'], message)
    send_message = send_message.json()

    message_react_request(user0['token'], send_message['message_id'], 1)
    message_unreact_request(user0['token'], send_message['message_id'], 1)

    response = message_unreact_request(user0['token'], send_message['message_id'], 1)
    assert response.status_code == InputError.code

def test_dm_unreact_already_InputError(dummy_data):
    '''
    Testing when user has already reacted the message.
    '''
    reset_call()

    users_list = dummy_data.register_users(num_of_users=1)
    user0 = users_list[0]
    dm_dict = dummy_data.create_dm(user0['token'], [users_list[0]['auth_user_id']])

    message = "hello world bye world"
    send_message = send_dm_message_request(user0['token'], dm_dict['dm_id'], message)
    send_message = send_message.json()

    message_react_request(user0['token'], send_message['message_id'], 1)
    message_unreact_request(user0['token'], send_message['message_id'], 1)

    response = message_unreact_request(user0['token'], send_message['message_id'], 1)
    assert response.status_code == InputError.code

'''
AccessError will occur when a user is not a member/owner of a valid channel_id or either not a global owner
or if token is invalid
'''
@pytest.mark.parametrize("invalid_token", ["Hello", "-1", -1, "35235gfdsgfdsh"])
# Testing case for when the token is invalid
def test_unreact_invalid_token_AccessError(dummy_data, create_route, invalid_token):
    reset_call()

    users_list = dummy_data.register_users(num_of_users=1)
    user0 = users_list[0]
    ch1 = requests.post(create_route, json={
        'token': user0["token"],
        'name': 'ch1',
        'is_public': True
    })
    assert ch1.status_code == OKAY
    ch1_dict = ch1.json()

    message = "hello world bye world"
    send_message = send_message_request(user0['token'], ch1_dict['channel_id'], message)
    send_message = send_message.json()
    message_react_request(user0['token'], send_message['message_id'], 1)

    response = message_unreact_request(invalid_token, send_message['message_id'], 1)
    assert response.status_code == AccessError.code

@pytest.mark.parametrize("invalid_token", ["Hello", "-1", -1, "35235gfdsgfdsh"])
def test_dm_unreact_invalid_token_AccessError(dummy_data, invalid_token):
    reset_call()

    users_list = dummy_data.register_users(num_of_users=1)
    user0 = users_list[0]
    dm_dict = dummy_data.create_dm(user0['token'], [users_list[0]['auth_user_id']])

    message = "hello world bye world"
    send_message = send_dm_message_request(user0['token'], dm_dict['dm_id'], message)
    send_message = send_message.json()
    message_react_request(user0['token'], send_message['message_id'], 1)

    response = message_unreact_request(invalid_token, send_message['message_id'], 1)
    assert response.status_code == AccessError.code

