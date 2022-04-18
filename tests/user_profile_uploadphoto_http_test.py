# HTTP TESTS FOR UPLOAD PHOTO

# from tests.http_func import channels_create_v2_http, channel_details_v2_http, channels_list_v2_http, channel_leave_v1_http
# from tests.http_func import dm_create_v1_http, dm_list_v1_http, dm_details_v1_http, dm_remove_v1_http
# from tests.http_func import message_remove_v1_http, message_send_v1_http, message_senddm_v1_http,message_share_v1_http
# from tests.http_func import uploadphoto_http
# from tests.http_func import setup

import requests
from requests import HTTPError
import pytest
from src.config import url
from src.error import InputError, AccessError

OKAY = 200

test_img = 'http://i.pinimg.com/236x/df/f6/9b/dff69b1f561c480aae6be7fcdfafe518.jpg'

test_img_width = 236
test_img_height = 238

@pytest.fixture()
def setup():
    # setup data_store
    requests.delete(f'{url}/clear/v1')

    user1_obj = requests.post(f'{url}/auth/register/v2', json={"email": "unswisgreat@unsw.edu.au", "password": "unsw123456", "name_first": "Tony", "name_last": "Stark"})
    assert user1_obj.status_code == OKAY
    user1_dict = user1_obj.json()
    assert isinstance(user1_dict, dict) and 'token' in user1_dict and isinstance(user1_dict['token'], str)

    return [user1_dict]

# ================================================== HTTP TESTS ===================================

# Input Error: img_url returns HTTP status other than 200 when retrieving photo
def test_retrieve_photo_error(setup):
    token = setup[0]['token']
    wrong_img_url = 'http://i.pinimg.com/36x/df/f6/9b/dff69b1f561c480aae6be7fcdfafe518.jpg'
    x_start = 10
    x_end = 220
    y_start = 10
    y_end = 210
    response = requests.post(f'{url}/user/profile/uploadphoto/v1', json = {
        'token': token,
        'img_url': wrong_img_url,
        'x_start': x_start,
        'y_start':y_start,
        'x_end': x_end,
        'y_end': y_end,
    })
    assert response.status_code == InputError.code 

# Input Error: x_start, y_start, x_end, y_end not within dimensions of photo
def test_x_start_outofrange(setup):
    token = setup[0]['token']
    img_url = test_img
    x_start = -1
    x_end = 220
    y_start = 10
    y_end = 210
    response = requests.post(f'{url}/user/profile/uploadphoto/v1', json = {
        'token': token,
        'img_url': img_url,
        'x_start': x_start,
        'y_start':y_start,
        'x_end': x_end,
        'y_end': y_end,
    })
    assert response.status_code == InputError.code 

def test_x_end_outofrange(setup):
    token = setup[0]['token']
    img_url = test_img
    x_start = 10
    x_end = test_img_width + 1
    y_start = 10
    y_end = 210
    response = requests.post(f'{url}/user/profile/uploadphoto/v1', json = {
        'token': token,
        'img_url': img_url,
        'x_start': x_start,
        'y_start':y_start,
        'x_end': x_end,
        'y_end': y_end,
    })
    assert response.status_code == InputError.code 

def test_y_start_outofrange(setup):
    token = setup[0]['token']
    img_url = test_img
    x_start = 10
    x_end = 220
    y_start = -1
    y_end = 210
    response = requests.post(f'{url}/user/profile/uploadphoto/v1', json = {
        'token': token,
        'img_url': img_url,
        'x_start': x_start,
        'y_start':y_start,
        'x_end': x_end,
        'y_end': y_end,
    })
    assert response.status_code == InputError.code 

def test_y_end_outofrange(setup):
    token = setup[0]['token']
    img_url = test_img
    x_start = 10
    x_end = 220
    y_start = 10
    y_end = test_img_height + 1
    response = requests.post(f'{url}/user/profile/uploadphoto/v1', json = {
        'token': token,
        'img_url': img_url,
        'x_start': x_start,
        'y_start':y_start,
        'x_end': x_end,
        'y_end': y_end,
    })
    assert response.status_code == InputError.code 

# Input Error: x_end <= x_start, y_end <= y_start
def test_x2_is_x1(setup):
    token = setup[0]['token']
    img_url = test_img
    x_start = 10
    x_end = 10
    y_start = 10
    y_end = 210
    response = requests.post(f'{url}/user/profile/uploadphoto/v1', json = {
        'token': token,
        'img_url': img_url,
        'x_start': x_start,
        'y_start':y_start,
        'x_end': x_end,
        'y_end': y_end,
    })
    assert response.status_code == InputError.code 

def test_x2_smallerthan_x1(setup):
    token = setup[0]['token']
    img_url = test_img
    x_start = 10
    x_end = 9
    y_start = 10
    y_end = 210
    response = requests.post(f'{url}/user/profile/uploadphoto/v1', json = {
        'token': token,
        'img_url': img_url,
        'x_start': x_start,
        'y_start':y_start,
        'x_end': x_end,
        'y_end': y_end,
    })
    assert response.status_code == InputError.code 

def test_y2_is_y1(setup):
    token = setup[0]['token']
    img_url = test_img
    x_start = 10
    x_end = 220
    y_start = 10
    y_end = 10
    response = requests.post(f'{url}/user/profile/uploadphoto/v1', json = {
        'token': token,
        'img_url': img_url,
        'x_start': x_start,
        'y_start':y_start,
        'x_end': x_end,
        'y_end': y_end,
    })
    assert response.status_code == InputError.code 

def test_y2_smallerthan_y1(setup):
    token = setup[0]['token']
    img_url = test_img
    x_start = 10
    x_end = 220
    y_start = 10
    y_end = 9
    response = requests.post(f'{url}/user/profile/uploadphoto/v1', json = {
        'token': token,
        'img_url': img_url,
        'x_start': x_start,
        'y_start':y_start,
        'x_end': x_end,
        'y_end': y_end,
    })
    assert response.status_code == InputError.code 

# Input Error: photo is not jpg
def test_not_jpg(setup):
    token = setup[0]['token']
    img_url = 'http://i.stack.imgur.com/ILTQq.png'
    x_start = 10
    x_end = 220
    y_start = 10
    y_end = 210
    response = requests.post(f'{url}/user/profile/uploadphoto/v1', json = {
        'token': token,
        'img_url': img_url,
        'x_start': x_start,
        'y_start':y_start,
        'x_end': x_end,
        'y_end': y_end,
    })
    assert response.status_code == InputError.code 

# Access Error: Token is invalid
def test_invalid_token(setup):
    img_url = test_img
    x_start = 10
    x_end = 220
    y_start = 10
    y_end = 210
    response = requests.post(f'{url}/user/profile/uploadphoto/v1', json = {
        'token': 'invalid_token',
        'img_url': img_url,
        'x_start': x_start,
        'y_start':y_start,
        'x_end': x_end,
        'y_end': y_end,
    })
    assert response.status_code == AccessError.code 

# Routine Behavior 
def test_working_uploadphoto(setup):
    token = setup[0]['token']
    img_url = test_img
    x_start = 10
    x_end = 120
    y_start = 10
    y_end = 110
    response = requests.post(f'{url}/user/profile/uploadphoto/v1', json = {
        'token': token,
        'img_url': img_url,
        'x_start': x_start,
        'y_start':y_start,
        'x_end': x_end,
        'y_end': y_end,
    })
    assert response.status_code == OKAY
