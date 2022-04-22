'''
FILE DESCRIPTION :
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
                "handle_str" : user["handle_str"]
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
                "handle_str" : user["handle_str"]
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
        raise AccessError(description="Invalid Token!!")

    
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

# =============================== NOTIFICATIONS GET ====================================

'''
Test message: 'Hi@A@Z, what are @B@C and @D doing? 
words = ['Hi@A@Z','what','are', '@B@C', 'and', '@D]', 'doing?']
at_words = ['Hi','A','Z','B','C','D']
existing_handles = []
'''


def notifications_get_v1(token):
    if not check_if_token_exists(token):
        raise AccessError(description="Invalid Token")

    users = data_store.get()['users']

    all_user_notifications = [user['notifications'] for user in users if user['token'] == token][0]
    num_of_notifications = len(all_user_notifications)

    if num_of_notifications < 20:
        notifications = all_user_notifications.reverse()
    else:
        notifications = all_user_notifications.reverse()[0:19]

    return {'notiifcations' : notifications}
