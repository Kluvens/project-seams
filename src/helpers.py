import jwt
import uuid
import json
import requests
import hashlib
from src.data_store import data_store
from src.error import AccessError

def check_if_token_exists(token):
    '''
    This is a helper function that takes in
    a token string and returns a boolean value

    if the token is found in the sessions list
    it will return True. Otherwise, it will return
    False.
    '''

    # The data access related code will need to 
    # be changed when we implement data persistance.
    users = data_store.get()['users']
    for user in users:
        if user['sessions'] == {}:
            return False
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

    except (jwt.InvalidTokenError, jwt.DecodeError):
        raise AccessError(description="Invalid Token!")

    return payload['u_id']



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
