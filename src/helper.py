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
    result = []
    sum = 0

    for channel in data['channels']:
        for member in channel['all_members']:
            if member['u_id'] == auth_user_id:
                result.append({
                    "num_channels_joined": sum,
                    "time_stamp": channel['time_stamp'],
                })
                sum += 1

    return result

def count_number_dms_joined(auth_user_id):
    data = data_store.get()
    result = []
    sum = 0

    for dm in data['dms']:
        for member in dm['all_members']:
            if member['u_id'] == auth_user_id:
                result.append({
                    "num_dms_joined": sum,
                    "time_stamp": dm['time_stamp'],
                })
                sum += 1

    return result

def count_number_messages_sent(auth_user_id):
    data = data_store.get()
    temp_result = []
    result = []
    sum = 0

    for channel in data['channels']:
        for message in channel['messages']:
            if message['u_id'] == auth_user_id:
                temp_result.append(message)

    for dm in data['dms']:
        for message in dm['messages']:
            if message['u_id'] == auth_user_id:
                temp_result.append(message)

    temp_result.sort(key=lambda x: x.get('time_sent'))

    if temp_result != None:
        for message in temp_result:
            result.append({
                "num_messages_sent": sum,
                "time_stamp": message['time_sent']
            })
            sum += 1

    return result

def count_number_channels_exist():
    data = data_store.get()
    result = []
    sum = 0

    for channel in data['channels']:
        result.append({
            'num_channels_exist': sum,
            'time_stamp': channel['time_stamp'],
        })
        sum += 1

    return result

def count_number_dms_exist():
    data = data_store.get()
    result = []
    sum = 0

    for dm in data['dms']:
        result.append({
            'num_dms_exist': sum,
            'time_stamp': dm['time_stamp'],
        })
        sum += 1

    return result

def count_number_messages_exist():
    data = data_store.get()
    temp_result = []
    result = []
    sum = 0

    for channel in data['channels']:
        for message in channel['messages']:
            temp_result.append(message)

    for dm in data['dms']:
        for message in dm['messages']:
            temp_result.append(message)

    temp_result.sort(key=lambda x: x.get('time_sent'))

    if temp_result != None:
        for message in temp_result:
            result.append({
                "num_messages_exist": sum,
                "time_stamp": message['time_sent']
            })
            sum += 1

    return result

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

def channel_details_members_return(users, member):
    return {
        'u_id': users[member['u_id']]['u_id'],
        'email': users[member['u_id']]['email'],
        'name_first': users[member['u_id']]['name_first'],
        'name_last': users[member['u_id']]['name_last'],
        'handle_str': users[member['u_id']]['handle_str'],
    }

def admin_remove_user_info(u_id, data_store):
    for room in data_store:
        # delete relevant messages
        if "messages" in room:
            for message in room['messages']:
                if message['u_id'] == u_id:
                    message['message'] = 'Removed user'
        # delete from all members
        for member in room['all_members']:
            if member['u_id'] == u_id:
                room["all_members"].remove({'u_id': u_id})
        # delete from owner members
        for o_member in room['owner_members']:
            if o_member['u_id'] == u_id:
                room["owner_members"].remove({'u_id': u_id})
