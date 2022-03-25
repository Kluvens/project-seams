'''
This module contains the implementation for the auth feature function

'''
import uuid
import hashlib
import jwt
import re
from src.data_store import data_store
from src.error import AccessError
from src.error import InputError
from src.helpers import check_if_token_exists
from src.helpers import decode_token

def auth_login_v2(email, password):
    '''
    This function takes in an email and password strings
    and returns the a u_id dictionary containing the u_id value
    that corresponds to those inputs

    Arguments:
        email, type: string.
        - Description: <A string representing an email>

        password, type: string
        - Description: <A string representing a password>

    Exceptions:
        InputError:
            1) occures when the email does not exist in the database
            2) password entered is incorrect

    Return Value:
        Returns:
        returns a dictionry containing a key called 'auth_user_id'
        and its value is the user_id the corresponds the user who logged in
    '''

    data = data_store.get()
    users_list = data['users']

    # Email does not exist in database
    if not is_email_already_registered(users_list, email):
        raise InputError("The email you entered does not belong to a user.")

    # Check Password is correct
    hashed_pw = hash(password)
    if not is_password_correct(users_list, email, hashed_pw):
        raise InputError("The password you entered is not correct.")


    u_id = get_corresponding_user_id(users_list, email)
    token = str(generate_session_token(u_id))
    users_list[u_id]['sessions'].append(token)
    return {'token' : token, 'auth_user_id': u_id}



def auth_register_v2(email, password, name_first, name_last):
    '''
    Arguments:
        This function takes an user related info (4 parameters)
        and registers a user. It also generates a unique handle
        for the new user and adds all the user info to a data store
        It returns an user_id dictionary to the caller.

        email, type: string.
        - Description: <A string representing the email of the user that
        will be registered>

        password, type: string
        - Description: <A string representing a password>

        name_first, type: string

        name_last, type: string

        - Description: <Both name_first and name_last refer to the
        the name of the user that is to be registered and added to the database.
        These argumnets will be utilised in generating a unique handle
        for the new user>

    Exceptions:
        InputError:
            1) occures when the email already belongs to an existing user
            2) occurs when the password has less than 6 characters
            3) occurs when the email does not pass the validity
            test against a defined regular expression
            4) occurs when the first name has less than 1 character
            or more than 50 characters
            5) occurs when the first name has less than 1 character
            or more than 50 characters

    Return Value:
        Returns:
        returns a dictionry containing a key called 'auth_user_id'
        and its value is the user_id of the user that has just been registered
    '''


    data = data_store.get()
    users_list = data["users"]

    # Check if email is already in the database
    # Emails ARE assumed to be case sensitive
    if is_email_already_registered(users_list, email):
        raise InputError(description=
            "The email you entered is already used "
            "by a registered user.")

    if not is_valid_email(email):
        raise InputError(description="The email you entered is invalid.")

    # Validate password
    if not is_valid_password(password):
        raise InputError(description=
            "The password you entered is invalid.\n"
            "Your password must have at least 6 ASCII characters.")

    # Validate first_name
    if not is_valid_name(name_first):
        raise InputError(
            "The first name you entered is invalid.\n"
            "Your first name must consist of ASCII only "
            "characters and be between 1 and 50 characters inclusive.")

    # Validate last_name
    if not is_valid_name(name_last):
        raise InputError(
            "The first name you entered is invalid.\n"
            "Your first name must consist of ASCII only "
            "characters and be between 1 and 50 characters inclusive.")

    # Generate Handle
    handle = generate_handle(users_list, name_first, name_last)

    # The u_id for a new user will be defined
    # as the number of currently registered users
    u_id = len(users_list)
    curr_user = {}
    users_list.append(curr_user)

    # Generate a session token
    # When a user is registered, they will be 
    # logged in and a new session token will
    # be created for them.
    token = generate_session_token(u_id)

    # Populate object in datastore with user data
    curr_user = users_list[u_id]
    curr_user['u_id'] = u_id
    curr_user['email'] = email
    curr_user['password'] = hash(password)
    curr_user['name_first'] = name_first
    curr_user['name_last'] = name_last
    curr_user['sessions'] = [str(token)]
    curr_user['handle_str'] = handle

    # Dealing with first layer of permissions
    OWNER = 1
    MEMBER = 2
    if u_id == 0:
        curr_user['permissions'] = OWNER
    else:
        curr_user['permissions'] = MEMBER


    data_store.set(data)
  
    return { "token" : token, "auth_user_id" : u_id }


def auth_logout_v1(token):
    '''
        This function takes in a token string. If the
        token is invalid, it raises an access error.
        Otherwise, it logs out the user session that
        corresponds to the token and returns an empty dict
    '''
    if not check_if_token_exists(token):
        raise AccessError(description="Invalid Token!")

    users_list = data_store.get()["users"]
    u_id = decode_token(token)
    if token in users_list[u_id]["sessions"]:
        users_list[u_id]["sessions"].remove(token)

    return {}

# ============================= HELPER FUNCTIONS ========================

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


def is_valid_password(password):
    '''
    This function checks if the password string contains less than
    6 characters by checking its length.
    If it does, it returns false to signal the password is invalid.
    Otherwise, True is returned

    '''
    if len(password) < 6:
        return False
    return True


def is_valid_name(name):
    '''
    This function checks if the name parameter is in between 1 and 50 characters
    (inclusive)
    It is assumed the name object will always be of type string.
    '''

    if len(name) >= 1 and len(name) <= 50:
        return True
    return False


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


def is_password_correct(users_list, email, password):
    '''
    This function checks if password is correct for a given email
    in a users list.

    It returns True if the password is correct. Otherwise False is returned
    '''

    for user_index, user in enumerate(users_list):
        if user['email'] == email:
            if users_list[user_index]['password'] == password:
                return True
    return False

def get_corresponding_user_id(users_list, email):
    '''
    Given a valid email for a registered user, and a users list
    This function returns the corresponding u_id
    '''

    for user_index, user in enumerate(users_list):
        if user['email'] == email:
            return user_index
    return None




def hash(password):
    '''
    This function uses the hashlib module to hash a given
    password string. It returns the hashed string.
    '''
    return hashlib.sha256(str(password).encode()).hexdigest()


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

