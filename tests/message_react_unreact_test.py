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

@pytest.fixture
def route():
    return url + "search/v1"


def search_request(route, token, query):
    return requests.get(
        url + "search/v1", params={"token" : token, "query_str" : query})



@pytest.fixture
def setup(dummy_data):
    reset_call()
    users_list = dummy_data.register_users(num_of_users=5)
    user0_token = users_list[0]["token"]
    user1_token = users_list[1]["token"]
    channels_list = dummy_data.create_multiple_channels(num_of_channels=2, token=user0_token)
    ch0 = channels_list[0]["channel_id"]
    u_ids = [users_list[1]["auth_user_id"], users_list[1]["auth_user_id"]]
    dummy_data.invite_users(user0_token, ch0, u_ids, num_of_users=2)

    return {
        "channel_id" : ch0,
        "user0" : user0_token,
        "user1" : user1_token,
        "uid0" : users_list[0]["auth_user_id"],
        "uid1" : users_list[1]["auth_user_id"]
    }

@pytest.fixture
def dummy_messages():
    return [
        "Hhello, how are you?! hhhaha missed you bro",
        "Hhhhi, I am good!\n How are you?",
        "yeahhh not too bad!, what are YoU DoiNg today>?"
    ]

def get_message_ids(messages_list):
    message_ids = []
    for message in messages_list:
        message_ids.append(
            message["message_id"]
        )
    return message_ids

def get_messages(messages_list):
    return [message["message"] for message in messages_list] 

def is_this_message_pinned(message_id, messages_list):
    for message in messages_list:
        if message_id == message["message_id"]:
            if message["is_pinned"]:
                return True
    return False

def is_this_user_reacted(message_id, messages_list):
    for message in messages_list:
        if message_id == message["message_id"]:
            if message["reacts"]["is_this_user_reacted"]:
                return True
    return False

def get_react_dict(message_id, messages_list):
    for message in messages_list:
        if message["message_id"] == message_id:
            return message["reacts"][0]

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

@pytest.mark.parametrize("msg", ["hHH", "!", "u"])
def test_dms_and_msgs(
    route, dummy_messages, setup, msg, dummy_data):
    ch0 = setup["channel_id"]
    user0_token = setup["user0"]
    user1_token = setup["user1"]

    dm_id = dummy_data.create_dm(user0_token, [setup["uid1"]])["dm_id"]

    msg1_dict = dummy_data.send_dm(user0_token, dm_id, dummy_messages[0])
    
    msg2_dict = dummy_data.send_message(user1_token, ch0, dummy_messages[1])
    dummy_data.pin_msg(user0_token, msg2_dict["message_id"])

    msg3_dict = dummy_data.send_dm(user1_token, dm_id, dummy_messages[2])

    dummy_data.react_to_message(user0_token, msg3_dict["message_id"], 1)
    dummy_data.react_to_message(user1_token, msg3_dict["message_id"], 1)
 
    response = search_request(route, user0_token, msg)
    messages_list = response.json()["messages"]
    print(messages_list)
    assert isinstance(messages_list, list)

    return_msg_ids = get_message_ids(messages_list)
    return_msg_ids.sort()
    expected = [msg1_dict["message_id"], msg2_dict["message_id"], msg3_dict["message_id"]]
    expected.sort()
    
    assert return_msg_ids == expected
    
    return_messages = get_messages(messages_list)
  
    for message in return_messages:
        assert message in dummy_messages

    react_dict = get_react_dict(msg3_dict["message_id"], messages_list)
    print(react_dict)
    assert react_dict["react_id"] == 1
    assert setup["uid0"] in react_dict["u_ids"]
    assert setup["uid1"] in react_dict["u_ids"]
    assert react_dict["is_this_user_reacted"]

    assert(is_this_message_pinned(msg2_dict["message_id"], messages_list))


################################# Unreact #################################

'''
InputError will occur when message_id is not a valid channel message within a channel/DM or react_id is not valid or message is hasn't been reacted
'''
# Testing case for when message_id is invalid
@pytest.mark.parametrize("invalid_message_id", [-9999, -55, 145, 9999])
def test_unreact_invalid_message_id_InputError(dummy_data, create_route, invalid_message_id):
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

