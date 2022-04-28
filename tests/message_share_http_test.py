from pickle import TRUE
import requests
import pytest
from src.config import url
from tests.http_helpers import GenerateTestData
from src.error import InputError, AccessError

from tests.http_func import channels_create_v2_http, channel_details_v2_http, channels_list_v2_http, channel_leave_v1_http
from tests.http_func import dm_create_v1_http, dm_list_v1_http, dm_details_v1_http, dm_remove_v1_http
from tests.http_func import message_remove_v1_http, message_send_v1_http, message_senddm_v1_http,message_share_v1_http
from tests.http_func import setup

OKAY = 200

# ======================================= SETUP =============================================
'''
Channel: Users A and B, where A is the creator of the channel
DM: Owner and B, where the Owner sends a DM to User B
'''

def channel_dm(setup_dict):
    '''
    CHANNEL TO DM
    In this setup there are 3 users - The global owner, A and B. 
    The global owner creates a dm to B ONLY and A and B are in a public channel together.
    A message is written in the channel (that includes A and B) by A.
    B will share the message to the DM.
    '''
    s = setup_dict
    tokens = s['tokens'] 
    channel_id = s['channel_id']

    message_obj = message_send_v1_http(tokens[1],channel_id, 'testing from A channel')
    message_info = message_obj.json()
    message_id = message_info['message_id']
    return {'message_id': message_id}


def dm_channel(setup_dict):

    '''
    DM TO CHANNEL
    In this setup there are 3 users - The global owner, A and B. 
    The global owner creates a dm to B ONLY and A and B are in a public channel together.
    A message is written in the DM by B. 
    B will share the message to the channel
    '''
    s = setup_dict
    tokens = s['tokens'] 
    dm_id = s['dm_id']

    message_obj = message_senddm_v1_http(tokens[2],dm_id,'testing from B DM')
    message_info = message_obj.json()
    message_id = message_info['message_id']
    return {'message_id': message_id}

# ======================================= HTTP TESTS =========================================================

# input: Invalid channel 
def test_invalid_channel(setup):
    setup_dict = setup
    token = setup_dict['tokens'][1]
    og_message_id = dm_channel(setup_dict)["message_id"]
    response = message_share_v1_http(token,og_message_id,'invalid channel test','12345','-1')
    assert response.status_code == InputError.code

# input: Invalid dm 
def test_invalid_dm(setup):
    setup_dict = setup
    token = setup_dict['tokens'][1]
    og_message_id = channel_dm(setup_dict)["message_id"]
    response = message_share_v1_http(token,og_message_id,'invalid dm test','-1','12345')
    assert response.status_code == InputError.code

# input: Both channel and dm id is not -1
def test_neither_neg1_valid_ids(setup):
    setup_dict = setup
    token = setup_dict['tokens'][1]
    channel_id = setup_dict['channel_id']
    dm_id = setup_dict['dm_id']
    og_message_id = channel_dm(setup_dict)["message_id"]
    response = message_share_v1_http(token,og_message_id,'neither -1,both valid',channel_id,dm_id)
    assert response.status_code == InputError.code 


def test_neither_neg1_invalid_ids(setup):
    setup_dict = setup
    token = setup_dict['tokens'][1]
    og_message_id = channel_dm(setup_dict)["message_id"]
    response = message_share_v1_http(token,og_message_id,'neither -1,neither valid','123','456')
    assert response.status_code == InputError.code 

# input: Invalid message id
def test_invalid_message_id_channeltodm(setup):
    setup_dict = setup
    token = setup_dict['tokens'][1]
    og_message_id = channel_dm(setup_dict)["message_id"]
    dm_id = setup_dict['dm_id']
    response = message_share_v1_http(token,'12345','invalid message id','-1',dm_id)
    assert response.status_code == InputError.code

def test_invalid_message_id_dmtochannel(setup):
    setup_dict = setup
    token = setup_dict['tokens'][1]
    og_message_id = dm_channel(setup_dict)["message_id"]
    channel_id = setup_dict['channel_id']

    response = message_share_v1_http(token, -12345, 'invalid message id',channel_id,'-1')
    assert response.status_code == InputError.code

# input: Message length > 1000
@pytest.fixture
def message():
    return '''Thus Spoke Zarathustra A Book for All and None
    When Zarathustra was thirty years old he left his home and the lake of his home 
    and went into the mountains. Here he enjoyed his spirit and his solitude and for 
    ten years he did not tire of it. But at last his heart transformed,  one morning 
    he arose with the dawn, stepped before the sun and spoke thus to it: 
    “You great star! What would your happiness be if you had not those for whom you shine 
    For ten years you have come up here to my cave: you would have tired of your light 
    and of this route without me, my eagle and my snake. But we awaited you every morning, 
    took your overflow from you and blessed you for it. Behold! I am weary of my wisdom, 
    like a bee that has gathered too much honey. I need hands that reach out. 
    I want to bestow and distribute until the wise among human beings have once again 
    enjoyed their folly, and the poor once again their wealth. For this I must descend into
    the depths, as you do evenings when you go behind the sea and bring light even to the 
    underworld, you super-rich star! Like you, I must go down as the human beings say, 
    to whom I want to descend. So bless me now, you quiet eye that can look upon even an 
    all too great happiness without envy! Bless the cup that wants to flow over, such that 
    water flows golden from it and everywhere carries the reflection of your bliss! 
    Behold! This cup wants to become empty again, and Zarathustra wants to become human again.”
    Thus began Zarathustras going under.'''

def test_message_over_1000_channeltodm(setup, message):
    
    setup_dict = setup
    token = setup_dict['tokens'][1]
    og_message_id = channel_dm(setup_dict)["message_id"]
    dm_id = setup_dict['dm_id']
    response = message_share_v1_http(token,og_message_id,message,'-1',dm_id)
    assert response.status_code == InputError.code

def test_message_over_1000_dmtochannel(setup, message):
    
    setup_dict = setup
    token = setup_dict['tokens'][1]
    og_message_id = dm_channel(setup_dict)["message_id"]
    channel_id = setup_dict['channel_id']

    response = message_share_v1_http(token,og_message_id,message,channel_id,-1)
    assert response.status_code == InputError.code

# access: Auth user not part of channel/dm they are sharing TO
def test_user_not_member_channeltodm(setup):
    setup_dict = setup
    token = setup_dict['tokens'][2]
    og_message_id = channel_dm(setup_dict)["message_id"]
    dm_id = setup_dict['dm_id']
    response = message_share_v1_http(token,og_message_id,'not member of dm to share to',-1,dm_id)
    assert response.status_code == AccessError.code

def test_user_not_member_dmtochannel(setup):
    setup_dict = setup
    token = setup_dict['tokens'][0]
    og_message_id = dm_channel(setup_dict)["message_id"]
    channel_id = setup_dict['channel_id']
    response = message_share_v1_http(token,og_message_id,'not member of channel to share to',channel_id, -1)
    assert response.status_code == AccessError.code

# access: Invalid Token
def test_invalid_token_channeltodm(setup):
    setup_dict = setup
    og_message_id = channel_dm(setup_dict)["message_id"]
    dm_id = setup_dict['dm_id']
    response = message_share_v1_http('abcde',og_message_id,'invalid token, channel/dm',-1,dm_id)
    assert response.status_code == AccessError.code 

def test_invalid_token_dmtochannel(setup):
    setup_dict = setup
    og_message_id = dm_channel(setup_dict)["message_id"]
    channel_id = setup_dict['channel_id']
    response = message_share_v1_http('abcde',og_message_id,'invalid token, channel/dm',channel_id, -1)
    assert response.status_code == AccessError.code 


# # Routine Behavior 
def test_working_share_channeltodm(setup):
    setup_dict = setup

    token = setup_dict['tokens'][1]
    og_message_id = channel_dm(setup_dict)["message_id"]
    channel_id = setup_dict['channel_id']
    response = message_share_v1_http(token, og_message_id, 'Working DM share to channel', channel_id, -1)
    assert response.status_code == OKAY


def test_working_share_dmtochannel(setup):
    setup_dict = setup

    token = setup_dict['tokens'][1]
    og_message_id = dm_channel(setup_dict)["message_id"]
    channel_id = setup_dict['channel_id']
    response = message_share_v1_http(token, og_message_id, 'Working DM share to channel', channel_id, -1)
    assert response.status_code == OKAY
