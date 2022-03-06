from src.data_store import data_store
from src.error import AccessError, InputError


def channel_invite_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_details_v1(auth_user_id, channel_id):

    return {
        'name',
        'is_public',
        'owner_members',
        'all_members',
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

'''
channel_join.py

This function allows given user to join a given channel.

Arguments:
auth_user_id (integer) - This is the user id of the user that would like to join the channel.
channel_id (integer) - This is the channel id of the channel that the user would like to join.

Exceptions:
InputError - An input error is raised when the channel id is invalid (i.e. the channel doesn't exist) or if the user already exists in the channel
AccessError - An access error is raised when a non authorized user tries to join a private channel (ie. not a global owner and not already in the channel)

Return Value:
This function does not return anything
'''
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

    # Input error 
    if channel_list == []:
        raise InputError ("ERROR: Channel does not exist")

    if user_in_channel:
        raise InputError ("ERROR: You have already joined this channel")         

    # Access error 
    if not channel_access:
        raise AccessError ("ERROR: You do not have access to this private channel")
        
    # Append member if all conditions met
    if channel_to_join != None and channel_access == True and user_in_channel == False:
        member_list = channel_to_join['all_members']
        new_member = {
            'u_id':auth_user_id,
            'email': users[auth_user_id]["email"],
            'name_first': users[auth_user_id]["name_first"],
            'name_last': users[auth_user_id]["name_last"],
            'handle_str': users[auth_user_id]["handle_str"]
            }
        member_list.append(new_member)
    return {}