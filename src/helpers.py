'''
Module Description: This is a helper functions module

'''


########################### Import Paths #########################
import re
import jwt
import uuid
import pickle
import json
import requests
import hashlib
from src.data_store import data_store
from src.error import AccessError
import re

############ Used By Every Feature except auth_register ##########

def check_u_id_exists(users, u_id):
    for user in users:
        if u_id == user["u_id"]:
            return True
    return False


def check_if_token_exists(token):
    '''
    This is a helper function that takes in
    a token string and returns a boolean value

    if the token is found in the sessions list
    it will return True. Otherwise, it will return
    False.
    '''

    users = data_store.get()['users']
    for user in users:
        if token in user['sessions']:
            return True
    return False



def decode_token(token):
    '''
    This is a helper function that takes in a token string.
    If the string has a jwt acceptable format, it will decode
    it and return a u_id. 

    Otherwise, it will raise an AccessError exception
    '''

    secret = "rjry3rJYwYIDHvVU0wJQuh6cFujCDfWS4Qa81w9HHGjEa0xs7N"    
    try:
        payload = jwt.decode(token, secret, algorithms=["HS256"])

    except (jwt.InvalidTokenError, jwt.DecodeError) as invalid_token:
        raise AccessError(description="Invalid Token!") from invalid_token

    return payload['u_id']

###################### Used By Auth and User features ############

def generate_session_token(u_id):
    '''
    This function uses generates a session token string
    using the u_id of the user and the secret string.

    Every session token generated will be guaranteed by
    adding uuid.uuid4() to the payload

    The token generation will be taken care of by a jwt method
    and the encrypted token will be returned as a string.

    This function will be called when a user is registered 
    and everytime the user logs in.
    '''
    secret = "rjry3rJYwYIDHvVU0wJQuh6cFujCDfWS4Qa81w9HHGjEa0xs7N"

    payload = {
        'unique_session_id' : str(uuid.uuid4()),
        'u_id' : u_id 
    }

    encripted_token = jwt.encode(payload, secret, algorithm="HS256")
    return encripted_token


def hash(password):
    '''
    This function uses the hashlib module to hash a given
    password string. It returns the hashed string.
    '''
    return hashlib.sha256(str(password).encode()).hexdigest()


def generate_handle(users_list, name_first, name_last):
    '''
    This function generates a unique alphanumeric handle for a new user.
    More details can be found in the details spec.

    It returns a string containing the handle generated

    '''
    naive_handle = ''.join([name_first, name_last])
    naive_handle = ''.join(ch for ch in naive_handle if ch.isalnum())
    naive_handle = naive_handle.lower()[:20]

    # starting at -1 since dupilicate handle strings will
    # start with 0 suffix
    handle_matches = -1
    for user in users_list:
        if user['handle_str'][:len(naive_handle)] == naive_handle:
            handle_matches += 1

    if handle_matches >= 0:
        handle_with_suffix = [naive_handle, str(handle_matches)]
        handle = ''.join(handle_with_suffix)
    else:
        # no matches and no need for numerical suffix
        handle = naive_handle

    return handle


def is_valid_name(name):
    '''
    This function checks if the name parameter is in between 1 and 50 characters
    (inclusive)
    It is assumed the name object will always be of type string.
    '''

    if len(name) >= 1 and len(name) <= 50:
        return True
    return False


def is_valid_email(email):
    '''
    This funciton utilised the regex module to check
    if the validty of an email string by checking if it matches a given regex.
    See regex below

    It returns True if it passes the check (if it is valid)
    Otherwise it returns False
    '''

    # Using regex module
    regex = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$"

    # using fullmatch which will match the entier email regex.
    match = re.fullmatch(regex, email)
    if match is not None:
        return True
    return False


def is_email_already_registered(users_list, email):
    '''
    Given a users list of dictionaries and an email string, this function
    checks if the email given belongs to an existing user.
    It returns True if it finds a match. Otherwise, it returns False

    '''

    for user in users_list:
        if user['email'] == email:
            return True
    return False


def return_exist_status(users, u_id):
    '''
    Checks the exist_status of a user and returns it
    '''
    users = data_store.get()["users"]
    for user in users:
        if user["u_id"] == u_id:
            return user["exist_status"]
    return None

###################### Used By Multiple Feature Functions #########

def check_handlestr_unique(users, handle_str):
    for user in users:
        if handle_str == user["handle_str"]:
            return False
    return True


def get_user_idx(users, u_id):
    for idx, user in enumerate(users):
        if u_id == user["u_id"]:
            return idx
    # does not exist
    return None

def find_dm_index(dms, dm_id):    
    for idx, dm in enumerate(dms):
        if dm['dm_id'] == dm_id:
            return idx
    return None

def is_in_dm(u_id, right_dm):
    for member in right_dm["all_members"]:
        if u_id == member["u_id"]:
            return True

    return False

def find_channel(channel_id):
    data = data_store.get()
    for channel in data['channels']:
        if int(channel_id) == channel['channel_id']:
            return channel
    return None

def find_user(u_id):
    data = data_store.get()
    for user in data['users']:
        if int(u_id) == user['u_id']:
            return user
    return None

def check_duplicate_u_ids(u_ids):
    i = 0
    while (i < len(u_ids)):
        j = i + 1
        while(j < len(u_ids)):
            if u_ids[i] == u_ids[j]:
                return True
            j += 1
        i += 1
    return False




def generate_dm_handle(owner_uid, u_ids, users):
    handles = []
    idx = get_user_idx(users, owner_uid) 
    handles.append(users[idx]["handle_str"])
    for u_id in u_ids:
        idx = get_user_idx(users, u_id) 
        handles.append(users[idx]["handle_str"])
    return handles


def is_global_owner(u_id):
    users = data_store.get()['users']
    for user in users:
        if user['u_id'] == u_id:
            if user['permissions'] == 1:
                return True
            else:
                return False
    return False

def write_savefile():
    """
    Saves data into pickle file, to ensure when server is restarted, data is not erased
    """
    with open('src/savefile.p', 'wb') as FILE:
        pickle.dump(data_store, FILE)

# ========================================= FOR MESSAGE SHARE/NOTIFICATIONS GET/UPLOAD PHOTO ===========================================

def find_message_from_message_id(message_id):
    message = None

    # Channel 
    channels = data_store.get()['channels']
    for channel in channels:
        messages = channel['messages']
        message = [message['message'] for message in messages if message['message_id'] == message_id][0]
        
    # DM
    dms = data_store.get()['dms']
    for dm in dms:
        messages = dm['messages']
        message = [message['message'] for message in messages if message['message_id'] == message_id][0]
        
    return {
        'message': message
    }

def find_channeldm_from_message(message_id):
    id = None

    # Channel 
    channels = data_store.get()['channels']
    for channel in channels:
        messages = channel['messages']
        message_ids = [message['message_id'] for message in messages]
        if message_ids.count(message_id) > 0:
            id = channel['channel_id']
            is_channel = True
            is_dm = False
    
    # DM
    dms = data_store.get()['dms']
    for dm in dms:
        messages = dm['messages']
        message_ids = [message['message_id'] for message in messages]
        if message_ids.count(message_id) > 0:
            id = dm['dm_id']
            is_channel = False
            is_dm = True
        
    return {
        'is_channel': is_channel,
        'is_dm': is_dm,
        'id': id,
    }

def find_message_sender(message_id,channel_id,dm_id):
    
    # Channels 
    if dm_id == -1:
        channels = data_store.get()['channels']
        channel = [channel for channel in channels if channel['channel_id '] == channel_id][0]
        message_list = channel['messages']
        sender_id = [message['u_id'] for message in message_list if message['message_id'] == message_id][0]

    # DMS
    if channel_id == -1:
        dms = data_store.get()['dms']
        dm = [dm for dm in dms if dm['dm_id'] == dm_id][0]
        message_list = dm['messages']
        sender_id = [message['u_id'] for message in message_list if message['message_id'] == message_id][0]      

    return sender_id 

def find_handle_in_message(message):
    words = message.split() 
    at_words = [word.split('@') for word in words if '@' in word]
    users = data_store.get()['users']
    existing_handles = [user['handle_str'] for user in users]
    handles = []
    for at_word in at_words:
        contains_handle = any(existing_handle in at_word for existing_handle in existing_handles)
        if contains_handle:
            handle = re.split('\W+',at_word)[0]
            handles.append(handle)
    return handles

