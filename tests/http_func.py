# Helper functions for HTTP Testing

import requests
import pytest
from src.config import url
from tests.http_helpers import GenerateTestData
from src.error import InputError, AccessError

# ===================================================== CHANNEL HTTP ==========================================

create_c = url + '/channels/create/v2'
def channels_create_v2_http(token,name,is_public):
    return requests.post(create_c, json = {
        'token': token,
        'name': name,
        'is_public': is_public,
    } )
    
detail_c = url + '/channel/details/v2'
def channel_details_v2_http(token,channel_id):
    return requests.get(detail_c, json = {
        'token': token,
        'channel_id':channel_id,
    })

list_c = url + '/channels/list/v2'
def channels_list_v2_http(token):
    return requests.get(list_c, json = {'token':token})

leave_c = url + '/channel/leave/v1'
def channel_leave_v1_http(token,channel_id):
    return requests.post(leave_c, json = {
        'token': token,
        'channel_id': channel_id,
    })

# ==================================================== DM HTTP ===============================================================

create_dm = url + 'dm/create/v1' 
def dm_create_v1_http(token, u_ids):
    return requests.post(create_dm, json = {
        'token': token,
        'u_ids': u_ids,
    })

list_dm = url + 'dm/list/v1'
def dm_list_v1_http(token):
    return requests.get(list_dm, json = {
        'token': token,
    })

detail_dm = url + 'dm/details/v1' 
def dm_details_v1_http(token, dm_id):
    return requests.get(detail_dm, json = {
        'token': token,
        'dm_id': dm_id,
    })

remove_dm = url + '/dm/remove/v1' 
def dm_remove_v1_http(token, dm_id):
    return requests.delete(remove_dm, json = {
        'token': token,
        'dm_id':dm_id,
    })

# ============================================================ MESSAGE HTTP ============================================================

send_message_c = url + 'message/send/v1'
def message_send_v1_http(token, channel_id, message):
    return requests.post(send_message_c, json = {
        'token': token,
        'channel_id': channel_id,
        'message': message,
    })

send_message_dm = url + 'message/senddm/v1'
def message_senddm_v1_http(token, dm_id, message):
    return requests.post(send_message_dm, json = {
        'token': token,
        'dm_id': dm_id,
        'message': message,
    })

remove_message = url + 'message/remove/v1'
def message_remove_v1_http(token, message_id):
    return requests.delete(remove_message, json = {
        'token': token,
        'message_id': message_id,
    })

share_message = url + 'message/share/v1'
def message_share_v1_http(token,og_message_id,message,channel_id,dm_id):
    print(channel_id)
    print(dm_id)
    return requests.post(share_message, json = {
        'token': token,
        'og_message_id': og_message_id,
        'message': message,
        'channel_id': channel_id,
        'dm_id': dm_id
    })
# =============== FIXTURES ==================================

# Clear
def reset_call():
    requests.delete(url + 'clear/v1')

# Create user base
@pytest.fixture()
def dummy_data():
    data_instance = GenerateTestData(url)
    return data_instance

 # ================================= SETUP ========================
@pytest.fixture
def setup(dummy_data):
    reset_call()

    # Create Owner, A and B
    users = dummy_data.register_users(num_of_users=3)
    owner = users[0]
    ### perahps try more descriptive lowercase variable names
    A = users[1]
    B = users[2]

    # Create Channel
    channel_obj = channels_create_v2_http(A['token'], 'test_channel', True)
    channel_info = channel_obj.json()
    channel_id = channel_info['channel_id']

    # Create DM
    u_ids = [B['auth_user_id']]
    dm_obj = dm_create_v1_http(A['token'], u_ids)
    dm_info = dm_obj.json()
    dm_id = dm_info['dm_id']

    return {
        'tokens':[owner['token'], A['token'], B['token']],
        'channel_id': channel_id,
        'dm_id': dm_id,
    }
