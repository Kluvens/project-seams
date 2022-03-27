import pytest
import requests
from src.config import url
from src.error import InputError, AccessError
from tests.http_helpers import GenerateTestData

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
InputError will occur when channel_id is not a valid channel
or when start is greater than the total number of messages in the channel
'''
# Testing case for when channel_id is invalid
def test_channel_messages_invalid_channel_InputError(dummy_data):
    reset_call()

    users_list = dummy_data.register_users(num_of_users=1)
    user0 = users_list[0]

    # Input invalid channel_id
    response = get_channel_messages(user0['token'], -1, 0)
    assert response.status_code == 400

# Testing case when start is invalid
def test_channel_messages_invalid_start_value_InputError(dummy_data, create_route):
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

    # Since no messages, 999999 is an invalid start value

    response = get_channel_messages(user0['token'], ch1_dict['channel_id'], 999999)
    assert response.status_code == 400

'''
AccessError will occur when a user is not a member of a valid channel_id
or if token is invalid
'''
@pytest.mark.parametrize("invalid_token", ["Hello", "-1", -1, "35235gfdsgfdsh"])
# Testing case for when the token is invalid
def test_channel_messages_invalid_token_AccessError(dummy_data, create_route, invalid_token):
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

    response = get_channel_messages(invalid_token, ch1_dict['channel_id'], 0)
    assert response.status_code == 403

# Testing case when authorised user is not a member of the valid channel_id
def test_channel_messages_unauthorised_user_AccessError(dummy_data, create_route):
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

    # user1 is not a member of the channel
    response = get_channel_messages(user1['token'], ch1_dict['channel_id'], 0)
    assert response.status_code == 403

# Testing case when channel messages is working with single user
def test_channel_messages_working_simple(dummy_data, create_route):
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

    start_number = 0
    message = "hello world bye world"
    
    # send_message_request() will output unique message_id
    send_message = send_message_request(user0["token"], ch1_dict["channel_id"], message)
    send_message = send_message.json()

    messages_output = get_channel_messages(user0['token'], ch1_dict['channel_id'], start_number)
    messages_output = messages_output.json()

    assert messages_output['start'] == start_number
    assert messages_output['end'] == -1
    assert messages_output['messages'][0]['message_id'] == send_message['message_id']
    assert messages_output['messages'][0]['u_id'] == user0['auth_user_id']
    assert messages_output['messages'][0]['message'] == message

# Testing case when channel messages is working with multiple user and multiple messages
def test_channel_messages_working_complex(dummy_data, create_route):
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

    post_channel_invite(user0['token'], ch1_dict['channel_id'], user1['auth_user_id'])

    start_number = 0
    message_one = "hello world"
    message_two = "bye world"

    # send_message_request() will output unique message_id
    response1 = send_message_request(user0['token'], ch1_dict['channel_id'], message_one)
    response2 = send_message_request(user1['token'], ch1_dict['channel_id'], message_two)

    send_message_one = response1.json()
    send_message_two = response2.json()

    messages_output = get_channel_messages(user0['token'], ch1_dict['channel_id'], start_number)
    messages_output = messages_output.json()

    assert messages_output['start'] == start_number
    assert messages_output['end'] == -1
    assert messages_output['messages'][0]['message_id'] == send_message_one['message_id']
    assert messages_output['messages'][0]['u_id'] == user0['auth_user_id']
    assert messages_output['messages'][0]['message'] == message_one
    assert messages_output['messages'][1]['message_id'] == send_message_two['message_id']
    assert messages_output['messages'][1]['u_id'] == user1['auth_user_id']
    assert messages_output['messages'][1]['message'] == message_two
