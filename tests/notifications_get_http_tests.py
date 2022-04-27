from tests.http_func import channels_create_v2_http, channel_details_v2_http, channels_list_v2_http, channel_leave_v1_http
from tests.http_func import dm_create_v1_http, dm_list_v1_http, dm_details_v1_http, dm_remove_v1_http
from tests.http_func import message_remove_v1_http, message_send_v1_http, message_senddm_v1_http,message_share_v1_http
from tests.http_func import upload_photo, notifications_http
from tests.http_func import setup
from src.error import AccessError

OKAY = 200

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
