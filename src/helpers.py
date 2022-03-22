import jwt
import uuid
import json
import requests
import hashlib

def check_if_token_exists(token: str) -> bool:
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
        if user['token'] in sessions:
            return True
    return False


def decode_token(token: str) -> dict:
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
