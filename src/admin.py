from src.data_store import data_store
from src.error import InputError, AccessError
from src.helpers import decode_token, check_if_token_exists
from src.helper import global_owner_check, get_user_idx, count_number_global_owner

def admin_user_remove_v1(token, u_id):
    data = data_store.get()

    # if token doesnt exist return AccessError
    if not check_if_token_exists(token):
        raise AccessError(description="Invalid token")
    auth_user_id = int(decode_token(token))

    if not global_owner_check(auth_user_id):
        raise AccessError("the authorised user is not a global owner")

    user_index = get_user_idx(data['users'], u_id)
    if user_index == None:
        raise InputError("u_id does not refer to a valid user")

    if count_number_global_owner(data['users']) == 1:
        raise InputError("u_id refers to a user who is the only global owner")

    data['users'][user_index]["name_first"] = 'Removed'
    data['users'][user_index]["name_last"] = 'user'
    data['users'][user_index]['email'] = None
    data['users'][user_index]['password'] = None
    data['users'][user_index]['handle_str'] = None
    data['users'][user_index]['permissions'] = None

    for channel in data['channels']:
        for message in channel['messages']:
            if message['u_id'] == u_id:
                message['message'] = 'Removed user'
        for memeber in channel['all_members']:
            if member['u_id'] == u_id:
                member['u_id'] = None
        for o_memeber in channel['owner_members']:
            if o_member['u_id'] == u_id:
                o_member['u_id'] = None

    data_store.set(data)

def admin_userpermission_change_v1(token, u_id, permission_id):
    OWNER = 1
    MEMBER = 2
    data = data_store.get()
    u_id = int(u_id)
    permission_id = int(permission_id)

    # if token doesnt exist return AccessError
    if not check_if_token_exists(token):
        raise AccessError(description="Invalid token")
    auth_user_id = int(decode_token(token))
    
    user_index = get_user_idx(data['users'], u_id)
    if user_index == None:
        raise InputError("u_id does not refer to a valid user")

    if permission_id not in [1, 2]:
        raise InputError("permission_id is invalid")

    if data['users'][user_index]['permissions'] == permission_id:
        raise InputError("the user already has the permissions level of permission_id")

    if not global_owner_check(auth_user_id):
        raise AccessError("the authorised user is not a global owner")

    if count_number_global_owner(data['users']) == 1 and permission_id == MEMBER and auth_user_id == u_id:
        raise InputError("u_id refers to a user who is the only global owner and they are being demoted to a user")

    data['users'][user_index]['permissions'] = permission_id

    data_store.set(data)
