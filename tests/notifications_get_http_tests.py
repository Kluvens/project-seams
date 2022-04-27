from http_func import channels_create_v2_http, channel_details_v2_http, channels_list_v2_http, channel_leave_v1_http
from http_func import dm_create_v1_http, dm_list_v1_http, dm_details_v1_http, dm_remove_v1_http
from http_func import message_remove_v1_http, message_send_v1_http, message_senddm_v1_http,message_share_v1_http
from http_func import upload_photo, notifications_http
from http_func import setup

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

def reset_call():
    requests.delete(url + 'clear/v1')

@pytest.fixture()
def dummy_data():
    data_instance = GenerateTestData(url)
    return data_instance

@pytest.fixture
def register_test_users(num_of_users):
    dummy_data = GenerateTestData(url)
    dummy_data.register_users(num_of_users)

@pytest.fixture
def create_route():
    return url + "channels/create/v2"

# ========================== HTTP TESTS ========================

# Invalid token
def test_invalid_token():
    token = '12345'
    response = notifications_http(token)
    assert response.status_code == AccessError.code

# Routine Behavior test
def test_working_notifications_get():
    token = setup()['tokens'][1]
    response = notifications_http(token)
    assert response.status_code == OKAY

# ==========================================================
'''
Reacts:
Create A and B
Create channel
A and B join channel
A messages channel
B reacts to A's message in channel
A receives a notification
Call notification get
'''

'''
Tagging:
Create A and B
Create DM
A and B join DM
A messages channel including @B_handle
B recieves notification 
Call notification get
'''

'''

'''