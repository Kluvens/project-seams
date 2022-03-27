#======================== Import Statements ======================
import pytest
import requests
from src.config import url
from src.error import InputError, AccessError
from tests.http_helpers import GenerateTestData

#======================== Helpers/Fixtures =======================

def reset_call():
    requests.delete(url + 'clear/v1')

@pytest.fixture()
def dummy_data():
    data_instance = GenerateTestData(url)
    return data_instance


def send_dm_request(token, dm_id, message):
    response = requests.post(url + "/message/senddm/v1", 
        json={
            "token" : token,
            "dm_id" : dm_id,
            "message" : message,
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


def post_dm_create(token, u_ids):
    response = requests.post(url + "/dm/create/v1",
        json={
            "token" : token,
            "u_ids" : u_ids,
        })
    return response


#========================== Testing Correctness ==================
'''
InputError will occur when dm_id is not a valid DM
or when start is greater than the total number of messages in the DM
'''
# Testing case when dm_id is invalid
def test_dm_messages_invalid_dm_id_InputError(dummy_data):
    reset_call()

    users_list = dummy_data.register_users(num_of_users=2)
    user0 = users_list[0]
    user1 = users_list[1]

    post_dm_create(user0["token"], [user1["auth_user_id"]])

    # Input invalid dm_id
    response = get_dm_messages(user0["token"], -1, 0)
    assert response.status_code == InputError.code

# Testing case when start is invalid
def test_dm_messages_invalid_start_value_InputError(dummy_data):
    reset_call()

    users_list = dummy_data.register_users(num_of_users=2)
    user0 = users_list[0]
    user1 = users_list[1]

    dm_channel = post_dm_create(user0["token"], [user1["auth_user_id"]])
    new_dm = dm_channel.json()

    # Since no messages, 9999 is an invalid start value
    response = get_dm_messages(user0['token'], new_dm['dm_id'], 9999)
    assert response.status_code == InputError.code

'''
AccessError will occur when a user is not a member of a valid DM
or if token is invalid
'''
@pytest.mark.parametrize("invalid_token", ["Hello", "-1", -1, "35235gfdsgfdsh"])
# Testing case for when the token is invalid
def test_dm_messages_invalid_token_AccessError(dummy_data, invalid_token):
    reset_call()

    users_list = dummy_data.register_users(num_of_users=2)
    user0 = users_list[0]
    user1 = users_list[1]

    dm_channel = post_dm_create(user0["token"], [user1["auth_user_id"]])
    new_dm = dm_channel.json()

    response = get_dm_messages(invalid_token, new_dm['dm_id'], 0)
    assert response.status_code == AccessError.code

# Testing case when authorised user is not a member of the valid dm_id
def test_dm_messages_unauthorised_user_AccessError(dummy_data):
    reset_call()

    users_list = dummy_data.register_users(num_of_users=3)
    user0 = users_list[0]
    user1 = users_list[1]
    user2 = users_list[2]

    dm_channel = post_dm_create(user0["token"], [user1["auth_user_id"]])
    new_dm = dm_channel.json()
    
    # user2 is not a member of the dm_id
    response = get_dm_messages(user2['token'], new_dm['dm_id'], 0)
    assert response.status_code == AccessError.code


# Testing case when dm messages is working (only one user sending a message)
def test_dm_messages_working_simple(dummy_data):
    reset_call()

    users_list = dummy_data.register_users(num_of_users=2)
    user0 = users_list[0]
    user1 = users_list[1]

    dm_channel = post_dm_create(user0["token"], [user1["auth_user_id"]])
    new_dm = dm_channel.json()

    start_number = 0
    message = "hello world bye world"

    # send_dm_request() will output unique message_id

    send_dm = send_dm_request(user0['token'], new_dm['dm_id'], message)
    send_dm = send_dm.json()

    # dm_messages_output = dm_messages_v1(uid_one['token'], new_dm['dm_id'], start_number)
    dm_messages_output = get_dm_messages(user0['token'], new_dm['dm_id'], start_number)
    dm_messages_output = dm_messages_output.json()

    assert dm_messages_output['start'] == start_number
    assert dm_messages_output['end'] == -1
    assert dm_messages_output['messages'][0]['message_id'] == send_dm['message_id']
    assert dm_messages_output['messages'][0]['u_id'] == user0['auth_user_id']
    assert dm_messages_output['messages'][0]['message'] == message

# Testing case when dm messages is working with multiple user and multiple messages
def test_dm_messages_working_complex(dummy_data):
    reset_call()

    users_list = dummy_data.register_users(num_of_users=3)
    user0 = users_list[0]
    user1 = users_list[1]
    user2 = users_list[2]
    
    dm_channel = post_dm_create(user0["token"], [user1["auth_user_id"], user2["auth_user_id"]])
    new_dm = dm_channel.json()

    start_number = 0
    message_one = "hello world"
    message_two = "bye world"
    
    # send_dm_request() will output unique message_id
    send_dm_one = send_dm_request(user0['token'], new_dm['dm_id'], message_one)
    send_dm_two = send_dm_request(user1['token'], new_dm['dm_id'], message_two)

    send_dm_one = send_dm_one.json()
    send_dm_two = send_dm_two.json()

    dm_messages_output = get_dm_messages(user2['token'], new_dm['dm_id'], start_number)
    dm_messages_output = dm_messages_output.json()

    assert dm_messages_output['start'] == start_number
    assert dm_messages_output['end'] == -1
    assert dm_messages_output['messages'][0]['message_id'] == send_dm_one['message_id']
    assert dm_messages_output['messages'][1]['message_id'] == send_dm_two['message_id']
    assert dm_messages_output['messages'][0]['u_id'] == user0['auth_user_id']
    assert dm_messages_output['messages'][1]['u_id'] == user1['auth_user_id']
    assert dm_messages_output['messages'][0]['message'] == message_one
    assert dm_messages_output['messages'][1]['message'] == message_two
