from src.server import channel_details_http, channels_list_http
from tests.http_func import channels_create_v2_http, channel_details_v2_http, channels_list_v2_http, channel_leave_v1_http, channel_invite_v2_http
from tests.http_func import dm_create_v1_http, dm_list_v1_http, dm_details_v1_http, dm_remove_v1_http
from tests.http_func import message_remove_v1_http, message_send_v1_http, message_senddm_v1_http,message_share_v1_http, message_react_v1_http
from tests.http_func import notifications_get_http
from tests.http_func import setup

from src.error import AccessError

OKAY = 200
# ==============================================================
import requests
import pytest
from src.config import url
from tests.http_helpers import GenerateTestData
from src.error import AccessError, InputError

#====================== Helper functions / Fixtures ===============
OKAY = 200

# Clear
def reset_call():
    requests.delete(url + 'clear/v1')
# ========================== HTTP TESTS ========================

# Invalid token: Tag
def test_invalid_token_tag(setup):

    setup_dict = setup
    token_A = setup_dict['tokens'][1]
    handle_B = setup_dict['handles'][2]
    dm_id = setup_dict['dm_id']

    # A tags B's handle to create notification
    message = 'Hey @{}'.format(handle_B)
    message_senddm_v1_http(token_A,dm_id,message)

    token = 12345
    response = notifications_get_http(token)
    assert response.status_code == AccessError.code

# Invalid token: React
def test_invalid_token_react(setup):

    setup_dict = setup
    token_A = setup_dict['tokens'][1]
    token_B = setup_dict['tokens'][2]
    dm_id = setup_dict['dm_id']

    # A send a message to dm
    message = 'React to this message to show react works!' 
    message_obj = message_senddm_v1_http(token_A,dm_id,message)
    message_info = message_obj.json()
    message_id = message_info['message_id']

    # B reacts to A's message in dm 
    message_react_v1_http(token_B,message_id,1)

    token = 12345
    response = notifications_get_http(token)
    assert response.status_code == AccessError.code

# Invalid token: Invite
def test_invalid_token_invite(setup):

    setup_dict = setup
    token_A = setup_dict['tokens'][1]
    u_id_B = setup_dict['auth_user_ids'][2]
    channel_id = setup_dict['channel_id']

    # A invites B to channel
    channel_invite_v2_http(token_A,channel_id,u_id_B)

    token = 12345
    response = notifications_get_http(token)
    assert response.status_code == AccessError.code

# ============================================ ROUTINE ============================================

# Working: Tag
def test_working_tag(setup):

    setup_dict = setup
    token_A = setup_dict['tokens'][1]
    token_B = setup_dict['tokens'][2]
    handle_A = setup_dict['handles'][1]
    handle_B = setup_dict['handles'][2]
    dm_id = setup_dict['dm_id']
    dm_name = 'testfirst1testlast1, testfirst2testlast2'

    # A tags B's handle to create notification
    message = 'Hey @{}'.format(handle_B)
    message_senddm_v1_http(token_A,dm_id,message)

    response = notifications_get_http(token_B)
    ret_obj = response.json()
    assert ret_obj["notifications"][0]["notification_message"] == "{} tagged you in {}: {}".format(handle_A,dm_name,message[:20])
    assert response.status_code == OKAY

# Working: react
def test_working_react(setup):

    setup_dict = setup
    token_A = setup_dict['tokens'][1]
    token_B = setup_dict['tokens'][2]
    handle_B = setup_dict['handles'][2]
    dm_id = setup_dict['dm_id']
    dm_name = 'testfirst1testlast1, testfirst2testlast2'

    # A send a message to dm
    message = 'React to this message to show react works!' 
    message_obj = message_senddm_v1_http(token_A,dm_id,message)
    message_info = message_obj.json()
    message_id = message_info['message_id']

    # B reacts to A's message in dm 
    message_react_v1_http(token_B,message_id,1)

    response = notifications_get_http(token_A)
    ret_obj = response.json()
    assert ret_obj["notifications"][0]["notification_message"] == "{} reacted to your message in {}".format(handle_B,dm_name)
    assert response.status_code == OKAY

# Working: Invite
def test_working_invite(setup):

    setup_dict = setup
    token_A = setup_dict['tokens'][1]
    token_B = setup_dict['tokens'][2]
    handle_A = setup_dict['handles'][1]
    u_id_B = setup_dict['auth_user_ids'][2]
    channel_id = setup_dict['channel_id']
    channel_name = 'test_channel'

    # A invites B to channel
    channel_invite_v2_http(token_A,channel_id,u_id_B)

    response = notifications_get_http(token_B)
    ret_obj = response.json()
    assert ret_obj["notifications"][0]["notification_message"] == "{} added you to {}".format(handle_A,channel_name)
    assert response.status_code == OKAY



