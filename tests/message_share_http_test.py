from pickle import TRUE
from turtle import reset
import requests
import pytest
from src.config import url
from tests.channel_leave_http_test import reset_call
from tests.http_helpers import GenerateTestData
from src.error import InputError, AccessError

from tests.http_func import channels_create_v2_http, channel_details_v2_http, channels_list_v2_http, channel_leave_v1_http
from tests.http_func import dm_create_v1_http, dm_list_v1_http, dm_details_v1_http, dm_remove_v1_http
from tests.http_func import message_remove_v1_http, message_send_v1_http, message_senddm_v1_http,message_share_v1_http
from tests.http_func import setup

OKAY = 200

# ======================================= SETUP =============================================
# s = setup()
# tokens = s['tokens'] 
# channel_id = s['channel_id']
# dm_id = s['dm_id']

def channel_dm(token,channel_id):
    '''
    CHANNEL TO DM
    In this setup there are 3 users - The global owner, A and B. 
    The global owner creates a dm to B ONLY and A and B are in a public channel together.
    A message is written in the channel (that includes A and B) by A.
    B will share the message to the DM.
    '''

    message_obj = message_send_v1_http(token,channel_id, 'testing from A channel')
    message_info = message_obj.json()
    message_id = message_info['message_id']
    return {'message_id': message_id}


def dm_channel(token,dm_id):

    '''
    DM TO CHANNEL
    In this setup there are 3 users - The global owner, A and B. 
    The global owner creates a dm to B ONLY and A and B are in a public channel together.
    A message is written in the DM by B. 
    B will share the message to the channel
    '''

    message_obj = message_senddm_v1_http(token,dm_id,'testing from B DM')
    message_info = message_obj.json()
    message_id = message_info['message_id']
    return {'message_id': message_id}

# ======================================= GENERATE USERS ====================================================

# Create user base
@pytest.fixture()
def dummy_data():
    data_instance = GenerateTestData(url)
    return data_instance

@pytest.fixture
def register_test_users(num_of_users):
    dummy_data = GenerateTestData(url)
    dummy_data.register_users(num_of_users)

# ======================================== OLD HTTP METHOD ==================================================
# # invalid channel_id
# def test_invalid_channel_id(create_route,leave_route,dummy_data):
#     reset_call()

#     user = dummy_data.register_users(num_of_users=1)[0]['token']

#     channel_id_obj = requests.post(create_route, json = {
#         'token':user,
#         'name': 'hello I am a channel',
#         'is_public':True,
#     })
#     channel_info = channel_id_obj.json()
#     channel_id = channel_info['channel_id']

#     response = requests.post(leave_route, json = {
#         'token':user,
#         'channel_id': channel_id+1000
#     })
#     assert response.status_code == InputError.code

def test_invalid_channel_old(dummy_data):
    reset_call()

    # Create Owner, A and B
    users = dummy_data.register_users(num_of_users=3)
    owner = users[0]
    A = users[1]
    B = users[2]

    # Create Channel
    channel_obj = channels_create_v2_http(A['token'],'test_channel',True)
    channel_info = channel_obj.json()
    channel_id = channel_info['channel_id']

    # Create DM
    u_ids = [B['auth_user_id']]
    dm_obj = dm_create_v1_http(owner['token'], u_ids)
    dm_info = dm_obj.json()
    dm_id = dm_info['dm_id']

    og_message_id = dm_channel(A['token'],dm_id)
    response = message_share_v1_http(B['token'],og_message_id,'invalid channel test',12345,-1)
    assert response.status_code == InputError.code
    
# ======================================= HTTP TESTS =========================================================

# # input: Invalid channel 
# def test_invalid_channel():
#     s = setup(dummy_data)
#     token_A = s['tokens'][1]
#     dm_id = s['dm_id']
#     token_B = s['tokens'][2]
#     og_message_id = dm_channel(token_A,dm_id)
#     response = message_share_v1_http(token_B,og_message_id,'invalid channel test','12345','-1')
#     assert response.status_code == InputError.code

# # input: Invalid dm 
# def test_invalid_dm():
#     s = setup(dummy_data)
#     channel_id = s['channel_id']
#     token_B = s['tokens'][2]
#     og_message_id = channel_dm(token_B,channel_id)
#     response = message_share_v1_http(token_B,og_message_id,'invalid dm test','-1','12345')
#     assert response.status_code == InputError.code

# # input: Both channel and dm id is not -1
# def test_neither_neg1_valid_ids():
#     token = setup()['tokens'][2]
#     channel_id = setup()['channel_id']
#     dm_id = setup()['dm_id']
#     og_message_id = channel_dm()
#     response = message_share_v1_http(token,og_message_id,'neither -1,both valid',channel_id,dm_id)
#     assert response.status_code == InputError.code 

# def test_neither_neg1_invalid_ids():
#     token = setup()['tokens'][2]
#     og_message_id = channel_dm()
#     response = message_share_v1_http(token,og_message_id,'neither -1,neither valid','123','456')
#     assert response.status_code == InputError.code 

# # input: Invalid message id
# def test_invalid_message_id_channeltodm():
#     token = setup()['tokens'][2]
#     dm_id = setup()['dm_id']
#     response = message_share_v1_http(token,'12345','invalid message id','-1',dm_id)
#     assert response.status_code == InputError.code

# def test_invalid_message_id_dmtochannel():
#     token = setup()['tokens'][2]
#     channel_id = setup()['channel_id']    
#     response = message_share_v1_http(token,'12345','invalid message id',channel_id,'-1')
#     assert response.status_code == InputError.code

# # input: Message length > 1000

# message = '''Thus Spoke Zarathustra A Book for All and None
#     When Zarathustra was thirty years old he left his home and the lake of his home 
#     and went into the mountains. Here he enjoyed his spirit and his solitude and for 
#     ten years he did not tire of it. But at last his heart transformed,  one morning 
#     he arose with the dawn, stepped before the sun and spoke thus to it: 
#     “You great star! What would your happiness be if you had not those for whom you shine 
#     For ten years you have come up here to my cave: you would have tired of your light 
#     and of this route without me, my eagle and my snake. But we awaited you every morning, 
#     took your overflow from you and blessed you for it. Behold! I am weary of my wisdom, 
#     like a bee that has gathered too much honey. I need hands that reach out. 
#     I want to bestow and distribute until the wise among human beings have once again 
#     enjoyed their folly, and the poor once again their wealth. For this I must descend into
#     the depths, as you do evenings when you go behind the sea and bring light even to the 
#     underworld, you super-rich star! Like you, I must go down as the human beings say, 
#     to whom I want to descend. So bless me now, you quiet eye that can look upon even an 
#     all too great happiness without envy! Bless the cup that wants to flow over, such that 
#     water flows golden from it and everywhere carries the reflection of your bliss! 
#     Behold! This cup wants to become empty again, and Zarathustra wants to become human again.”
#     Thus began Zarathustras going under.'''

# def test_message_over_1000_channeltodm(message):
    
#     token = setup()['tokens'][2]
#     og_message_id = channel_dm()
#     dm_id = setup()['dm_id']

#     response = message_share_v1_http(token,og_message_id,message,'-1',dm_id)
#     assert response.status_code == InputError.code

# def test_message_over_1000_dmtochannel(message):
    
#     token = setup()['tokens'][2]
#     og_message_id = dm_channel()
#     channel_id = setup()['channel_id']

#     response = message_share_v1_http(token,og_message_id,message,channel_id,'-1')
#     assert response.status_code == InputError.code

# # access: Auth user not part of channel/dm they are sharing TO
# def test_user_not_member_channeltodm():
#     token = setup()['tokens'][1]
#     og_message_id = channel_dm()
#     dm_id = setup()['dm_id']
#     response = message_share_v1_http(token,og_message_id,'not member of dm to share to','-1',dm_id)
#     assert response.status_code == AccessError.code

# def test_user_not_member_dmtochannel():
#     token = setup()['tokens'][0]
#     og_message_id = dm_channel()
#     channel_id = setup()['channel_id']
#     response = message_share_v1_http(token,og_message_id,'not member of channel to share to',channel_id,'-1')
#     assert response.status_code == AccessError.code

# # access: Invalid Token
# def test_invalid_token_channeltodm():
    
#     og_message_id = channel_dm()
#     dm_id = setup()['dm_id']
#     response = message_share_v1_http('abcde',og_message_id,'invalid token, channel/dm','-1',dm_id)
#     assert response.status_code == AccessError.code 

# def test_invalid_token_dmtochannel():
    
#     og_message_id = dm_channel()
#     channel_id = setup()['channel_id']
#     response = message_share_v1_http('abcde',og_message_id,'invalid token, channel/dm',channel_id,'-1')
#     assert response.status_code == AccessError.code 

# # Routine Behavior 

# def test_working_share_channeltodm():
#     token = setup()['tokens'][2]
#     og_message_id = channel_dm()
#     dm_id = setup()['dm_id']
#     response = message_share_v1_http(token,og_message_id,'Working channel share to DM','-1',dm_id)
#     assert response.status_code == OKAY

# def test_working_share_channeltodm():
#     token = setup()['tokens'][2]
#     og_message_id = dm_channel()
#     channel_id = setup()['channel_id']
#     response = message_share_v1_http(token,og_message_id,'Working DM share to channel',channel_id,'-1')
#     assert response.status_code == OKAY

