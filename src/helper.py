from src.auth import auth_register_v2, auth_login_v2
from src.data_store import data_store


def find_channel_index(channels, channel_id):    
    for idx, channel in enumerate(channels):
        if channel['channel_id'] == channel_id:
            return idx
    return None

def is_in_channel(u_id, right_channel):
    for member in right_channel["all_members"]:
        if u_id == member["u_id"]:
            return True

    return False


def count_number_owner(right_channel):
    total = 0
    for member in right_channel['owner_members']:
        if member is not None:
            total += 1
    
    return total


def is_in_channel_owner(u_id, right_channel):
    for member in right_channel["owner_members"]:
        if u_id == member["u_id"]:
            return True

    return False 

def is_in_dm_owner(u_id, right_dm):
    for member in right_dm['owner_members']:
        if u_id == member['u_id']:
            return True

    return False


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


def get_user_idx(users, u_id):
    for idx, user in enumerate(users):
        if u_id == user["u_id"]:
            return idx
    # does not exist
    return None

def count_number_channels_joined(auth_user_id):
    data = data_store.get()
    sum = 0

    for channel in data['channels']:
        for member in channel['all_members']:
            if member['u_id'] == auth_user_id:
                sum += 1
                break

    return sum

def count_number_dms_joined(auth_user_id):
    data = data_store.get()
    sum = 0

    for dm in data['dms']:
        for member in dm['all_members']:
            if member['u_id'] == auth_user_id:
                sum += 1
                break

    return sum

def count_number_messages_sent(auth_user_id):
    data = data_store.get()
    sum = 0

    for channel in data['channels']:
        for message in channel['messages']:
            if message['u_id'] == auth_user_id:
                sum += 1
                break

    for dm in data['dms']:
        for message in dm['messages']:
            if message['u_id'] == auth_user_id:
                sum += 1
                break

    return sum

def count_number_channels_exist():
    data = data_store.get()
    sum = len(data['channels'])

    return sum

def count_number_dms_exist():
    data = data_store.get()
    sum = len(data['dms'])

    return sum

def count_number_messages_exist():
    data = data_store.get()
    sum = 0

    for channel in data['channels']:
        sum += len(channel['messages'])

    for dm in data['dms']:
        sum += len(dm['messages'])

    return sum

def count_users_joined():
    data = data_store.get()
    sum = 0

    for user in data['users']:
        joinned = False
        for channel in data['channels']:
            for member in channel['all_members']:
                if member['u_id'] == user['u_id']:
                    joinned = True
                    
        for dm in data['dms']:
            for member in dm['all_members']:
                if member['u_id'] == user['u_id']:
                    joinned = True

        if joinned:
            sum += 1

    return sum

def count_number_users():
    data = data_store.get()
    sum = len(data['users'])

    return sum
