
from src.data_store import data_store
from src.error import InputError
import re

#from data_store import data_store
#from error import InputError


# Further function documentation will be added later.
def auth_login_v1(email, password):
    users_list = data_store.get()['users']
    # Email does not exist in database
    if is_email_already_registered(users_list, email) is False:
        raise InputError("The email you entered does not belong to a user")

    # Check Password is correct
    if is_password_correct(users_list, email, password) is False:
        raise InputError("The password you entered is not correct")

    for user_index, user in enumerate(users_list):
        if (user['email'] == email):
            break

    uid = user_index + 1
    return {'auth_user_id': uid}


## Second part of the feature
# Registering a new user. Further details will be added later
def auth_register_v1(email, password, name_first, name_last):
    users_list = data_store.get()['users']

    # Check if email is already in the database
    # Emails ARE assumed to be case sensitive
    if is_email_already_registered(users_list, email) is True:
        raise InputError(
            "The email you entered is already used "
            "by a by a registered user.")

    if is_valid_email(email) is False:
        raise InputError("The email you entered is invalid.")

    # Validate password
    if is_valid_password(password) is False:
        raise InputError(
            "The password you entered is invalid.\n"
            "Your password must have at least 6 ASCII characters.")

    # Validate first_name
    if is_valid_name(name_first) is False:
        raise InputError(
            "The first name you entered is invalid.\n"
            "Your first name must be consist of ASCII only "
            "characters and between 1 and 50 characters inclusive.")
    
    # Validate last_name
    if is_valid_name(name_last) is False:
        raise InputError(
            "The first name you entered is invalid.\n"
            "Your first name must be consist of ASCII only"
            "characters and between 1 and 50 characters inclusive.")
    
    # Generate Handle
    handle = generate_handle(users_list, name_first, name_last)
    
    # Populating the 'users' list with a new user's dictionary
    uid = len(users_list) + 1
    curr_user = {}
    users_list.append(curr_user)
    curr_user = users_list[uid - 1]
    curr_user['uid'] = uid
    curr_user['email'] = email
    curr_user['password'] = password
    curr_user['name_first'] = name_first
    curr_user['name_last'] = name_last
    curr_user['handle'] = handle

    return { 'auth_user_id': uid }

# ============================= HELPER FUNCTIONS ========================

# Checking if email inputted belong to an existing user
def is_email_already_registered(users_list, email):
    for user in users_list:
        if user['email'] == email:
            return True
    return False

# Checking whether email contains invalid characters
# see regex below
def is_valid_email(email):
    # Using regex module
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    if (re.fullmatch(regex, email)):
        return True
    else:
        return False


# Checking password string has less than 6 characters
def is_valid_password(password):
    if len(password) < 6:
        return False
    else:
        return True

# Checking if name is in between 1 and 50 characters inc
def is_valid_name(name):
    if len(name) >= 1 and len(name) <= 50:
        return True
    else:
        return False


# Generating a unique alphanumeric handle for a new user.
# More details can be found in the details spec.
def generate_handle(users_list, name_first, name_last):
    naive_handle = ''.join([name_first, name_last])
    naive_handle = ''.join(ch for ch in naive_handle if ch.isalnum())
    naive_handle = naive_handle.lower()[:20]

    handle_matches = -1
    for user in users_list:
        if user['handle'][:len(naive_handle)] == naive_handle:
            handle_matches += 1

    if handle_matches >= 0:
        handle_with_suffix = [naive_handle, str(handle_matches)]
        handle = ''.join(handle_with_suffix)
    else:
        handle = naive_handle

    return handle

# Can access database globally, but chose to pass it
# as an argument
def is_password_correct(users_list, email, password):
    for user_index, user in enumerate(users_list):
        if user['email'] == email:
            if users_list[user_index]['password'] == password:
                return True
            else:
                return False
    return False



if __name__ == "__main__":
    pass
