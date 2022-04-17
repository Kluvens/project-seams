from src.data_store import data_store
from src.error import InputError, AccessError
from src.helpers import decode_token, check_if_token_exists
from src.helper import global_owner_check, get_user_idx, count_number_global_owner
from src.helper import admin_remove_user_info

def admin_user_remove_v1(token, u_id):
    '''
    the function is used to remove an existing user and his relevant info

    Arguments:
        token - the auth user
        u_id - the user to be removed

    Exceptions:
        InputError - u_id does not refer to a valid user
        InputError - u_id refers to a user who is the only global owner
        AccessError - the authorised user is not a global owner
        AccessError - invalid token

    Return:
        {}
    '''
    data = data_store.get()

    # if token doesnt exist return AccessError
    if not check_if_token_exists(token):
        raise AccessError(description="Invalid token")
    auth_user_id = int(decode_token(token))

    if not global_owner_check(auth_user_id):
        raise AccessError(description="the authorised user is not a global owner")

    user_index = get_user_idx(data['users'], u_id)
    if user_index == None:
        raise InputError(description="u_id does not refer to a valid user")

    if count_number_global_owner(data['users']) == 1 and u_id == auth_user_id:
        raise InputError(description="u_id refers to a user who is the only global owner")

    user_to_be_removed = data["users"][user_index]

    user_to_be_removed["exist_status"] = False

    user_to_be_removed["name_first"] = "Removed"
    user_to_be_removed["name_last"] = "user"
    # Copying their details to the removed users list
    user_data = data["users"][user_index].copy()
    data["removed_users"].append(user_data)

    # We have to add this key to the data object 
    # in data_store

    data['users'][user_index]['email'] = ''
    data['users'][user_index]['password'] = ''
    data['users'][user_index]['handle_str'] = ''
    data['users'][user_index]['permissions'] = 0

    # log them out
    user_to_be_removed["sessions"] = []

    # delete and resettle the information about the removed user
    # delete associated info about channels
    admin_remove_user_info(u_id, data['channels'])

    # delete associated info about dms
    admin_remove_user_info(u_id, data['dms'])
    # for dm in data['dms']:
    #     if "messages" in dm:
    #         for message in dm['messages']:
    #             if message['u_id'] == u_id:
    #                 message['message'] = 'Removed user'
    #     for member in dm['all_members']:
    #         if member['u_id'] == u_id:
    #             dm['all_members'].remove({'u_id': u_id})
    #     for o_member in dm['owner_member']:
    #         if o_member['u_id'] == u_id:
    #             dm['owner_members'].remove({'u_id': u_id})

    data_store.set(data)

    return {}

def admin_userpermission_change_v1(token, u_id, permission_id):
    '''
    the function is used to change the global permission of a user

    Arguments:
        token - the auth user
        u_id - the user that needs to change the permission
        permission_id - the permission to be changed to

    Exceptions:
        InputError - u_id does not refer to a valid user
        InputError - u_id refers to a user who is the only global owner and they are being demoted to a user
        InputError - permission_id is invalid
        InputError - the user already has the permissions level of permission_id
        AccessError - invalid token
        AccessError - the authorised user is not a global owner

    Return:
        {}
    '''
    MEMBER = 2
    data = data_store.get()
    u_id = int(u_id)
    permission_id = int(permission_id)

    # if token doesnt exist return AccessError
    if not check_if_token_exists(token):
        raise AccessError(description="Invalid token")
    auth_user_id = int(decode_token(token))
    
    user_index = get_user_idx(data['users'], u_id)
    # more error checking
    if user_index == None:
        raise InputError(description="u_id does not refer to a valid user")

    if permission_id not in [1, 2]:
        raise InputError(description="permission_id is invalid")

    if data['users'][user_index]['permissions'] == permission_id:
        raise InputError(description="the user already has the permissions level of permission_id")

    if not global_owner_check(auth_user_id):
        raise AccessError(description="the authorised user is not a global owner")

    if count_number_global_owner(data['users']) == 1 and permission_id == MEMBER and auth_user_id == u_id:
        raise InputError(description="u_id refers to a user who is the only global owner and they are being demoted to a user")

    # change the permission
    data['users'][user_index]['permissions'] = permission_id

    data_store.set(data)

    return {}
