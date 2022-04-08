import requests
import pytest
from src.config import url
from tests.http_helpers import GenerateTestData
from src.error import InputError, AccessError

from http_func import channels_create_v2_http, channel_details_v2_http, channels_list_v2_http, channel_leave_v1_http
from http_func import dm_create_v1_http, dm_list_v1_http, dm_details_v1_http, dm_remove_v1_http
from http_func import message_remove_v1_http, message_send_v1_http, message_senddm_v1_http

OKAY = 200

# =============== FIXTURES ==================================

# Clear
def reset_call():
    requests.delete(url + 'clear/v1')

# Create user base
@pytest.fixture()
def dummy_data():
    data_instance = GenerateTestData(url)
    return data_instance


# ======================================= HTTP TESTS =========================================================

# input: Invalid channel 

# input: Invalid dm 

# input: Both channel and dm id is not -1

# input: Invalid message id

# input: Message length > 1000

# access: Auth user not part of channel/dm they are sharing TO

# access: Invalid Token






