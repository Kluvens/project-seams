from src.auth import auth_register_v2, auth_login_v2
from src.data_store import data_store

def find_channel_index(channels, channel_id):    
    for idx, channel in enumerate(channels):
        if channel['channel_id'] == channel_id:
            return idx
    return None


def get_user_idx(users, u_id):
    for idx, user in enumerate(users):
        if u_id == user["u_id"]:
            return idx
    # does not exist
    return None

def get_dm_idx(dms, dm_id):
    for idx, dm in enumerate(dms):
        if dm_id == dm['dm_id']:
            return idx
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

def is_in_dm(auth_user_id, dm):
    for member in dm['all_members']:
        if auth_user_id == member['u_id']:
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
    user = auth_login_v2(email, password)

    u_id = user["auth_user_id"]
    return u_id

def global_owner_check(auth_user_id):
    OWNER = 1

    data = data_store.get()
    for user in data['users']:
        if user['u_id'] == auth_user_id:
            if user['permissions'] == OWNER:
                return True
            else:
                return False
    
    return False

def count_number_global_owner(users):
    sum = 0
    OWNER = 1

    for user in users:
        if user['permissions'] == OWNER:
            sum += 1

    return sum