from src.auth import auth_register_v2, auth_login_v2
from src.data_store import data_store

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
    user = auth_login_v2(email, password)

    u_id = user["auth_user_id"]
    return u_id
