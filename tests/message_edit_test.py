import pytest
import requests
from src.config import url
from src.error import InputError, AccessError
from tests.http_helpers import GenerateTestData

OKAY = 200
def reset_call():
    requests.delete(url + 'clear/v1')

@pytest.fixture()
def dummy_data():
    data_instance = GenerateTestData(url)
    return data_instance

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

def get_dm_messages(token, dm_id, start):
    response = requests.get(url + "/dm/messages/v1",
        params={
            "token" : token,
            "dm_id" : dm_id,
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

def put_message_edit(token, message_id, message):
    response = requests.put(url + "/message/edit/v1",
        json={
            "token" : token,
            "message_id" : message_id,
            "message" : message,
        })
    return response


'''
InputError will occur when message_id is not a valid
or the length of message is more than 1000 characters.
'''
# Testing case for when message_id is invalid
def test_channel_messages_edit_invalid_message_id_InputError(dummy_data, create_route):
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

    message_one = "hello world"
    send_message_request(user0['token'], ch1_dict['channel_id'], message_one)
    message_two = "bye world"

    response = put_message_edit(user0['token'], ch1_dict["channel_id"], message_two)
    assert response.status_code == InputError.code

# Testing case when the message string is more than 1000 characters long
def test_channel_messages_send_length_of_message_toolong_InputError(dummy_data, create_route): 
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

    message_one = "hello world"
    send_message_request(user0['token'], ch1_dict['channel_id'], message_one)

    message = "a"
    # Loop through to create a message with length greater than 1000 characters
    for i in range(1001):
        message += f" {i}"

    response = put_message_edit(user0['token'], ch1_dict["channel_id"], message)
    assert response.status_code == InputError.code

'''
AccessError will occur when a user is not a member/owner of a valid channel_id or either not a global owner
or if token is invalid
'''
@pytest.mark.parametrize("invalid_token", ["Hello", "-1", -1, "35235gfdsgfdsh"])
# Testing case for when the token is invalid
def test_channel_messages_edit_invalid_token_AccessError(dummy_data, create_route, invalid_token):
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

    message_one = "hello world"
    send_message_request(user0['token'], ch1_dict['channel_id'], message_one)
    message_two = "bye world"

    response = put_message_edit(invalid_token, ch1_dict["channel_id"], message_two)
    assert response.status_code == AccessError.code

# Testing case when authorised user is not a member of the valid channel_id
def test_channel_messages_edit_unauthorised_user_AccessError(dummy_data, create_route):
    reset_call()

    users_list = dummy_data.register_users(num_of_users=2)
    user0 = users_list[0]
    user1 = users_list[1]

    ch1 = requests.post(create_route, json={
        'token': user0["token"],
        'name': 'ch1',
        'is_public': True
    })
    assert ch1.status_code == OKAY
    ch1_dict = ch1.json()

    message_one = "hello world"
    send_message = send_message_request(user0["token"], ch1_dict["channel_id"], message_one)
    send_message = send_message.json()   
    message_two = "bye world"

    response = put_message_edit(user1["token"], send_message["message_id"], message_two)
    assert response.status_code == AccessError.code

# Testing case when message_edit is working
def test_channel_messages_edit_working(dummy_data, create_route):
    reset_call()
    
    users_list = dummy_data.register_users(num_of_users=2)
    user0 = users_list[0]
    user1 = users_list[1]
    
    ch1 = requests.post(create_route, json={
        'token': user0["token"],
        'name': 'ch1',
        'is_public': True
    })
    assert ch1.status_code == OKAY
    ch1_dict = ch1.json()
    
    post_channel_invite(user0["token"], ch1_dict['channel_id'], user1["auth_user_id"])

    message_one = "hello world"
    message_two = "bye world"

    response1 = send_message_request(user0['token'], ch1_dict['channel_id'], message_one)
    response2 = send_message_request(user1['token'], ch1_dict['channel_id'], message_two)
 
    send_message_one = response1.json()
    send_message_two = response2.json()

    # Edit messages from channel
    message_three = "alpha"
    message_four = "beta"
    
    put_message_edit(user0["token"], send_message_one['message_id'], message_three)
    put_message_edit(user1["token"], send_message_two['message_id'], message_four)

    # get_channel_messages will output a dictionary containing a message array.
    messages_output = get_channel_messages(user0['token'], ch1_dict["channel_id"], 0).json()

    assert messages_output['messages'][1]['message'] == message_three
    assert messages_output['messages'][0]['message'] == message_four

def test_dm_messages_edit_working(dummy_data):
    reset_call()
    
    users_list = dummy_data.register_users(num_of_users=2)
    user0 = users_list[0]
    user1 = users_list[1]
    dm_dict = dummy_data.create_dm(user0['token'], [users_list[1]['auth_user_id']])

    message_one = "hello world"
    message_two = "bye world"

    response1 = send_dm_message_request(user0['token'], dm_dict['dm_id'], message_one)
    response2 = send_dm_message_request(user1['token'], dm_dict['dm_id'], message_two)
 
    send_message_one = response1.json()
    send_message_two = response2.json()

    # Edit messages from channel
    message_three = "alpha"
    message_four = "beta"
    
    put_message_edit(user0["token"], send_message_one['message_id'], message_three)
    put_message_edit(user1["token"], send_message_two['message_id'], message_four)

    # get_channel_messages will output a dictionary containing a message array.
    messages_output = get_dm_messages(user0['token'], dm_dict["dm_id"], 0).json()

    assert messages_output['messages'][1]['message'] == message_three
    assert messages_output['messages'][0]['message'] == message_four
