from src.data_store import data_store

def channel_invite_v1(auth_user_id, channel_id, u_id):
    return {
    }

def find_channel_index(channel_id):
    data = data_store.get()

    i = 0
    for channel in data[channels]:
        if channel["c_id"] == channel_id:
            return i
        else:
            i += 1
    return None

def is_in_channel(auth_user_id, right_channel):
    for channel in len(right_channel["all_members"]):
        if auth_user_id == channel["u_id"]:
            return True

    return False

def channel_details_v1(auth_user_id, channel_id):
    data = data_store.get()
    users = data["users"]

    right_channel_index = find_channel_index(channel_id)

    # error
    if right_channel_index == None:
        raise InputError("channel_id does not refer to a valid channel")

    right_channel = data["channels"][right_channel_index]

    if not is_in_channel(auth_user_id, right_channel):
        raise AccessError("channel_id is valid and the authorised user is not a member of the channel")

    return {
        'name': right_channel["name"],
        'is_public': right_channel["is_public"],
        'owner_members': right_channel['owner_members'],
        'all_members': right_channel['all_members'],
        # 'owner_members': [
        #     {
        #         'u_id': 1,
        #         'email': 'example@gmail.com',
        #         'name_first': 'Hayden',
        #         'name_last': 'Jacobs',
        #         'handle_str': 'haydenjacobs',
        #     }
        # ],
        # 'all_members': [
        #     {
        #         'u_id': 1,
        #         'email': 'example@gmail.com',
        #         'name_first': 'Hayden',
        #         'name_last': 'Jacobs',
        #         'handle_str': 'haydenjacobs',
        #     }
        # ],
    }

def channel_messages_v1(auth_user_id, channel_id, start):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        'start': 0,
        'end': 50,
    }

def channel_join_v1(auth_user_id, channel_id):
    return {
    }
