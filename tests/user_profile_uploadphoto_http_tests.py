# HTTP TESTS FOR UPLOAD PHOTO

from http_func import channels_create_v2_http, channel_details_v2_http, channels_list_v2_http, channel_leave_v1_http
from http_func import dm_create_v1_http, dm_list_v1_http, dm_details_v1_http, dm_remove_v1_http
from http_func import message_remove_v1_http, message_send_v1_http, message_senddm_v1_http,message_share_v1_http
from http_func import upload_photo_http
from http_func import setup

from src.error import AccessError

OKAY = 200

test_img = 'http://i.pinimg.com/236x/df/f6/9b/dff69b1f561c480aae6be7fcdfafe518.jpg'

test_img_width = 236
test_img_height = 238

# ================================================== HTTP TESTS ===================================

# Input Error: img_url returns HTTP status other than 200 when retrieving photo
def test_retrieve_photo_error():
    token = setup()['tokens'][1]
    wrong_img_url = 'http://i.pinimg.com/36x/df/f6/9b/dff69b1f561c480aae6be7fcdfafe518.jpg'
    x_start = 10
    x_end = 220
    y_start = 10
    y_end = 210
    response = upload_photo_http(token, wrong_img_url, x_start, y_start, x_end, y_end)
    assert response.status_code == AccessError.code 

# Input Error: x_start, y_start, x_end, y_end not within dimensions of photo
def test_x_start_outofrange():
    token = setup()['tokens'][1]
    img_url = test_img
    x_start = -1
    x_end = 220
    y_start = 10
    y_end = 210
    response = upload_photo_http(token, img_url, x_start, y_start, x_end, y_end)
    assert response.status_code == AccessError.code 

def test_x_end_outofrange():
    token = setup()['tokens'][1]
    img_url = test_img
    x_start = 10
    x_end = test_img_width + 1
    y_start = 10
    y_end = 210
    response = upload_photo_http(token, img_url, x_start, y_start, x_end, y_end)
    assert response.status_code == AccessError.code 

def test_y_start_outofrange():
    token = setup()['tokens'][1]
    img_url = test_img
    x_start = 10
    x_end = 220
    y_start = -1
    y_end = 210
    response = upload_photo_http(token, img_url, x_start, y_start, x_end, y_end)
    assert response.status_code == AccessError.code 

def test_y_end_outofrange():
    token = setup()['tokens'][1]
    img_url = test_img
    x_start = 10
    x_end = 220
    y_start = 10
    y_end = test_img_height + 1
    response = upload_photo_http(token, img_url, x_start, y_start, x_end, y_end)
    assert response.status_code == AccessError.code 

# Input Error: x_end <= x_start, y_end <= y_start
def test_x2_is_x1():
    token = setup()['tokens'][1]
    img_url = test_img
    x_start = 10
    x_end = 10
    y_start = 10
    y_end = 210
    response = upload_photo_http(token, img_url, x_start, y_start, x_end, y_end)
    assert response.status_code == AccessError.code 

def test_x2_smallerthan_x1():
    token = setup()['tokens'][1]
    img_url = test_img
    x_start = 10
    x_end = 9
    y_start = 10
    y_end = 210
    response = upload_photo_http(token, img_url, x_start, y_start, x_end, y_end)
    assert response.status_code == AccessError.code 

def test_y2_is_y1():
    token = setup()['tokens'][1]
    img_url = test_img
    x_start = 10
    x_end = 220
    y_start = 10
    y_end = 10
    response = upload_photo_http(token, img_url, x_start, y_start, x_end, y_end)
    assert response.status_code == AccessError.code 

def test_y2_smallerthan_y1():
    token = setup()['tokens'][1]
    img_url = test_img
    x_start = 10
    x_end = 220
    y_start = 10
    y_end = 9
    response = upload_photo_http(token, img_url, x_start, y_start, x_end, y_end)
    assert response.status_code == AccessError.code 

# Input Error: photo is not jpg
def test_not_jpg():
    token = setup()['tokens'][1]
    img_url = 'http://i.stack.imgur.com/ILTQq.png'
    x_start = 10
    x_end = 220
    y_start = 10
    y_end = 210
    response = upload_photo_http(token, img_url, x_start, y_start, x_end, y_end)
    assert response.status_code == AccessError.code 

# Access Error: Token is invalid
def test_invalid_token():
    img_url = test_img
    x_start = 10
    x_end = 220
    y_start = 10
    y_end = 210
    response = upload_photo_http('12345', img_url, x_start, y_start, x_end, y_end)
    assert response.status_code == AccessError.code 

# Routine Behavior 
def test_working_uploadphoto():
    token = setup()['tokens'][1]
    img_url = test_img
    x_start = 10
    x_end = 220
    y_start = 10
    y_end = 210
    response = upload_photo_http(token, img_url, x_start, y_start, x_end, y_end)
    assert response.status_code == OKAY
