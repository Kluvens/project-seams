
from src.data_store import data_store
from src.error import InputError

#from data_store import data_store
#from error import InputError

'''
def auth_login_v1(email, password):
    users_list = data_store.get()['users']
    for user_position, user in enumerate(users_list):
        if (user['email'] == email):
            return user_position
    uid = user_position + 1 
    return {'auth_user_id': uid}
'''

def auth_register_v1(email, password, name_first, name_last):
    users_list = data_store.get()['users']

    if is_email_already_registered(users_list, email) == True:
        raise InputError("The email you entered is already used by a"
            "by a registered user.")

    if is_valid_email(email) == False:
        raise InputError("The email you entered is invalid.")

    # Validate password
    if is_valid_password(password) == False:
        raise InputError(
                "The password you entered is invalid.\n"
                "Your password must have at least 6 ASCII characters.")

    # validate first_name
    if is_valid_name(name_first) == False:
        raise InputError(
            "The first name you entered is invalid.\n"
            "Your first name must be consist of ASCII only"
            "characters and between 1 and 50 characters inclusive.")
    
    # validate last_name
    if is_valid_name(name_last) == False:
        raise InputError(
            "The first name you entered is invalid.\n"
            "Your first name must be consist of ASCII only"
            "characters and between 1 and 50 characters inclusive.")

    
    # Generate Handle
    handle = generate_handle(users_list, name_first, name_last)
    
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

def is_email_already_registered(users_list, email):
    for user in users_list:
        if user['email'] == email:
            return True
    return False

def is_valid_email(email):
    # Use regex module
    pass

def is_valid_password(password):
    if len(password) < 6:
        return True

def is_valid_name(name):
    if len(name) >= 1 and len(name) <= 50:
        return True
    else:
        return False

# still need to get rid of non alpha numeric characters 
# and lowercase the whole thing
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

if __name__ == "__main__":
    pass