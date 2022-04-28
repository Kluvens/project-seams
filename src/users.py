'''
FILE DESCRIPTION : This file contains the implementations of all the user
routes
'''

############################### Import Statements ################
from src.data_store import data_store
from src.error import AccessError
from src.error import InputError
from src.helpers import check_if_token_exists
from src.helpers import decode_token
from src.helpers import generate_handle
from src.helpers import is_valid_name
from src.helpers import is_valid_email
from src.helpers import is_email_already_registered
from src.helpers import check_handlestr_unique
from src.helpers import get_user_idx
from src.helpers import check_u_id_exists
from src.helpers import return_exist_status
from src.helper import count_number_channels_exist, count_number_dms_exist, count_number_messages_sent, count_number_dms_joined, count_number_channels_joined, count_number_messages_exist
from src.helper import count_users_joined, count_number_users
from src.config import url
import urllib
from PIL import Image
import uuid
import os

##################### User Function Implementations ##############
def users_all_v1(token):
    '''
    This function displays all the user details
    that are registered in the database

    Arguments: token, type: str
    
    Exceptions: 
        - Throws an AccessError when an invalid token
        string is passed
    
    Return: A list of user dictionaries, where
    each dict has a key-value pair of
    u_id, email, name_first, name_last, handle_str

    '''
    if not check_if_token_exists(token):
        raise AccessError(description="Invalid Token")

    users = data_store.get()["users"]
    users_details = []
    for user in users:
        if user["exist_status"]:
            users_details.append({
                "u_id" : user["u_id"],
                "email" : user["email"],
                "name_first": user["name_first"],
                "name_last" : user["name_last"],
                "handle_str" : user["handle_str"],
                "profile_img_url" : user["profile_img_url"]
            })

    return {"users" : users_details}


def user_profile_v1(token, u_id):
    '''
    This function displays all the user details
    that belong to the u_id passed to the function

    Arguments: 
        - token, type: str
        - u_id, type: int 
    
    Exceptions: 
        - Throws an AccessError when an invalid token
        string is passed
        - Throws an AccessError when an invalid u_id
        is passed
    
    Return: A dictionary that has the follwing keys
    and their corresponding values:
    u_id, email, name_first, name_last, handle_str
    '''
    if not check_if_token_exists(token):
        raise AccessError(description="Invalid Token")
    
    data  = data_store.get()

    users = data["users"]
    exist_status = return_exist_status(users, u_id)

    if exist_status == False:
        users = data["removed_users"]

    if get_user_idx(users, u_id) is None:
        raise InputError(
            description="This u_id does not belong to a valid user")

    user_profile = {}
    for user in users:
        if u_id == user["u_id"]:
            user_profile = {
                "u_id" : u_id,
                "email" : user["email"],
                "name_first": user["name_first"],
                "name_last" : user["name_last"],
                "handle_str" : user["handle_str"],
                "profile_img_url" : user["profile_img_url"]
            }

    return {"user" : user_profile}


def user_setname_v1(token, name_first, name_last):
    '''
    This function updates the first and last names of
    the user with u_id that corresponds to the token passed.

    Arguments: 
        - token, type: str
        - name_first: str
        - name_last: str 
    
    Exceptions: 
        - Throws an AccessError when an invalid token
        string is passed
        - Throws an AccessError when an invalid u_id
        is passed
        - Throws an InputError when either the first
        or last names contain less than 1 characaters
        or more than 50 chatacters
    
    Returns: empty dictionary 
    '''

    if not check_if_token_exists(token):
        raise AccessError(description="Invalid Token")
    
    if not is_valid_name(name_first):
        raise InputError(description=
            "Invalid first name. First name must be between 1 and 50 characters inclusive")

    if not is_valid_name(name_last):
        raise InputError(description=
            "Invalid last name. Last name must be between 1 and 50 characters inclusive")

    u_id = decode_token(token)

    users = data_store.get()["users"]
    idx = get_user_idx(users, u_id)
    users[idx]["name_first"] = name_first
    users[idx]["name_last"] = name_last
    users[u_id]["handle_str"] = generate_handle(users, name_first, name_last)

    return {}


def user_profile_setemail_v1(token, email):
    '''
    This function updates the email of the user with
    the u_id that corresponds the token that has been
    passed.

    Arguments: 
        - token, type: str
        -email 
    
    Exceptions: 
        - Throws an AccessError when an invalid token
        string is passed
        - Throws an AccessError when an invalid u_id
        is passed
        - Throws an InputError when the email
        entered is invalid
        - Throws an InputError when the email
        entered is already used by another user
    
    Returns: empty dictionary 
    '''

    if not check_if_token_exists(token):
        raise AccessError(description="Invalid Token!")

    
    u_id = decode_token(token)
    users = data_store.get()["users"]


    if not check_u_id_exists(users, u_id):
        raise AccessError(description="u_id does not belong to a valid user")
    
    if not is_valid_email(email):
        raise InputError(description="Invalid Email!")

    
    users = data_store.get()["users"]

    if is_email_already_registered(users, email):
        raise InputError(description="Email already exists. Try entering another email.")


    idx = get_user_idx(users, u_id)
    users[idx]["email"] = email

    return {}



def user_profile_sethandle_v1(token, handle_str):
    '''
    This function updates the handle string of the user
    with the u_id that corresponds to the token passed. 

    Arguments: 
        - token, type: str
        - handle_str : str
    
    Exceptions: 
        - Throws an AccessError when an invalid token
        string is passed
        - Throws an AccessError when an invalid u_id
        is passed
        - Throws an InputError when the handle_Str
        already exists
        - Throws an InputError when the handle_str
        is not in between 3 and 20 characters
    
    Return: empty dictionary 
    '''

    if not check_if_token_exists(token):
        raise AccessError(description="Invalid Token")

    if len(handle_str) < 3 or len(handle_str) > 20:
        raise InputError(description="Handle string must be within 3 and 20 characters.")
    
    if not handle_str.isalnum():
        raise InputError(description=
            "Handle string must be consist of alphanumeric characters only.")

    u_id = decode_token(token)

    users = data_store.get()["users"]

    if not check_handlestr_unique(users, handle_str):
        raise InputError(description="Handle already exists!")

    idx = get_user_idx(users, u_id)
    users[idx]["handle_str"] = handle_str

    return {}

def user_stats_v1(token):
    '''
    the functions return the information about channels, dms and messages involved and an involvement rate

    Arguments:
        token - auth user who wants to get the info

    Exceptions:
        AccessError - invalid token

    Return:
        Dictionary of shape {
         channels_joined: [{num_channels_joined, time_stamp}],
         dms_joined: [{num_dms_joined, time_stamp}], 
         messages_sent: [{num_messages_sent, time_stamp}], 
         involvement_rate 
        }
    '''
    if check_if_token_exists(token) == False:
        raise AccessError(description="Error occured, invalid token'")
    
    auth_user_id = int(decode_token(token))

    num_channels_joined = count_number_channels_joined(auth_user_id)
    # print(num_channels_joined)
    # print("channels joined")
    num_dms_joined = count_number_dms_joined(auth_user_id)
    # print(num_dms_joined)
    # print("dms joined")
    num_messages_sent = count_number_messages_sent(auth_user_id)
    # print(num_messages_sent)
    # print("messages sent")
    num_channels_exist = count_number_channels_exist()
    # print(num_channels_exist)
    # print("channels exist")
    num_dms_exist = count_number_dms_exist()
    # print(num_dms_exist)
    # print("dms exist")
    num_messages_exist = count_number_messages_exist()
    # print(num_messages_exist)
    # print('messages exist')

    if (len(num_channels_exist) + len(num_dms_exist) + len(num_messages_exist) - 3) > 0:
        involvement_rate = (len(num_channels_joined) + len(num_dms_joined) + len(num_messages_sent) -3) / (len(num_channels_exist) + len(num_dms_exist) + len(num_messages_exist) -3)
    else:
        involvement_rate = 0

    user_stats = {
        'channels_joined': num_channels_joined,
        'dms_joined': num_dms_joined,
        'messages_sent': num_messages_sent,
        'involvement_rate': involvement_rate,
    }

    return {'user_stats': user_stats}

def users_stats_v1(token):
    '''
    the functions return information about existing channels, dms and messages and a utilization rate

    Arguments:
        token - auth user who wants to get the info

    Exceptions:
        AccessError - invalid token

    Return:
        Dictionary of shape {
         channels_exist: [{num_channels_exist, time_stamp}], 
         dms_exist: [{num_dms_exist, time_stamp}], 
         messages_exist: [{num_messages_exist, time_stamp}], 
         utilization_rate 
        }
    '''
    if check_if_token_exists(token) == False:
        raise AccessError(description="Error occured, invalid token'")

    num_channels_exist = count_number_channels_exist()
    num_dms_exist = count_number_dms_exist()
    num_messages_exist = count_number_messages_exist()

    users_join_at_least_one = count_users_joined()
    num_users = count_number_users()

    utilization_rate = users_join_at_least_one/num_users

    workspace_stats = {
        'channels_exist': num_channels_exist,
        'dms_exist': num_dms_exist,
        'messages_exist': num_messages_exist,
        'utilization_rate': utilization_rate,
    }

    return {'workspace_stats': workspace_stats}


    # ============= USER PROFILE UPLOAD PHOTO ==============
def user_profile_uploadphoto_v1(token, img_url, x_start, y_start, x_end, y_end):

    # Check if token is invalid
    if not check_if_token_exists(token):
        raise AccessError(description="ERROR: Token is invalid")

    # Check if url is valid
    #### commented this to debug
    # if not 'http://' in img_url:
        # raise InputError(description= 'ERROR: Image url is invalid')


    # Check image is a jpg file / assuming no white space at the end of str
    # can jpg be uppercase? -> to jasmine
    print(f"\n<<<<<<{img_url}>>>>>\n")

    if not img_url.endswith('.jpg') and not img_url.endswith('.JPG'):
        print(img_url.endswith('.jpg')) 
        raise InputError(description= 'ERROR: Uploaded image is not a jpg file')

    # I'm assuming we already have an dir to store profile photos (because we have a default img)
    auth_user_id = decode_token(token)
    users = data_store.get()['users']
    user_handle = [user['handle_str'] for user in users if user['u_id'] == auth_user_id][0]
    
    # Download and save image to src/profile_images
    ## uuid.uuid4() might need this to debug potetnial problem
    file_path = 'src/profile_images/{}_{}.jpg'.format(user_handle, uuid.uuid4())
    print(f"\n<<<<<<{os.getcwd()}>>>>>\n")
    # Check if x range or y range is impossible 
    if x_end <= x_start or y_end <= y_start:
        raise InputError(description="x_end is less than or equal to x_start or y_end is less than or equal to y_start")

    try:
        urllib.request.urlretrieve(img_url, file_path)
    except InputError:
            print(description="img_url returns an HTTP status other than 200")
    
    


    # Check x and y values are within image 
    image = Image.open(file_path)
    width, height = image.size
    print(f"\n ----- {image.size} ----\n")
    if x_end > width or y_end > height or x_start < 0 or y_start < 0:
        raise InputError(description= 'ERROR: Selection is outside original image size')

    # Save cropped image 
    cropped_image = image.crop((x_start, y_start, x_end, y_end))
    cropped_file_path = 'src/profile_images/cropped/{}__{}.jpg'.format(user_handle, uuid.uuid4())
    cropped_image.save(cropped_file_path)

    # Store url in user dictionary
    user_idx = get_user_idx(users, auth_user_id)
    users[user_idx]['profile_img_url'] = url + cropped_file_path

    return {}
