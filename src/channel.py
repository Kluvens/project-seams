from src.data_store import data_store
from src.error import AccessError, InputError


def channel_invite_v1(auth_user_id, channel_id, u_id):
    return {
    }

# ==================================================== JUSTINS CODE ==========================================


def find_channel_index(channel_id):
    data = data_store.get()

    i = 0
    for channel in data["channels"]:
        if channel["channel_id"] == channel_id:
            return i
        else:
            i += 1
    return None

def is_in_channel(auth_user_id, right_channel):
    for channel in right_channel["all_members"]:
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
    }

# ================================ JUSTINS CODE ==================================

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

    # Access channel and user lists
    store = data_store.get()
    channels = store['channels']
    users = store['users']
    
    #Check if channel exists, is public, is global owner, is already a member 
    channel_access = False 
    user_in_channel = False
    channel_to_join = None

    # Check channel exists
    channel_list = [channel for channel in channels if channel['channel_id'] == channel_id]
        
    # If channel exists, save correct channel
    if channel_list != []:
        channel_to_join = channel_list[0]
        # Check if user exists in channel already
        users = channel_to_join['all_members']
        u_id_list = [user['u_id'] for user in users]
        if auth_user_id in u_id_list:
            user_in_channel = True
        # Check if the channel is public 
        if channel_to_join['is_public']:
            channel_access = True 

    # Check if user is a global owner 
    if auth_user_id == 0:
        channel_access = True   

    # Access error 
    if not channel_access:
        raise AccessError ("ERROR: You do not have access to this private channel")
    
    # Input error 
    if channel_list == []:
        raise InputError ("ERROR: Channel does not exist")

    if user_in_channel:
        raise InputError ("ERROR: You have already joined this channel")         
        
    # Append member if all conditions met
    if channel_to_join != None and channel_access == True and user_in_channel == False:
        member_list = channel_to_join['all_members']
        new_member = {
            'u_id':auth_user_id,
            }
        member_list.append(new_member)
    return {}