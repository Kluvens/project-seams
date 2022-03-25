import jwt
import uuid
import json
import requests
import hashlib
from src.data_store import data_store

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

# add error handelling in case of invalid token
def decode_token(token):
    secret = "rjry3rJYwYIDHvVU0wJQuh6cFujCDfWS4Qa81w9HHGjEa0xs7N"
    payload = jwt.decode(token, secret, algorithms=["HS256"])
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

def find_channel_index(channels, channel_id):    
    for idx, channel in enumerate(channels):
        if channel['channel_id'] == channel_id:
            return idx
    return None


def find_user_index(u_id):
    data = data_store.get()

    i = 0
    for user in data['users']:
        if user['u_id'] == u_id:
            return i
        else:
            i += 1
    return None

def is_in_channel(u_id, right_channel):
    for member in right_channel["all_members"]:
        if u_id == member["u_id"]:
            return True

    return False

def is_in_channel_owner(u_id, right_channel):
    for member in right_channel["owner_members"]:
        if u_id == member["u_id"]:
            return True

    return False 

def count_number_owner(right_channel):
    total = 0
    for member in right_channel['owner_members']:
        if member is not None:
            total += 1
    
    return total

def get_user_id(email, password, name_first, name_last):
    user = auth_register_v2(email, password, name_first, name_last)

    u_id = user["auth_user_id"]
    return u_id
