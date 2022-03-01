from data_store import data_store
import error


def channel_invite_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_details_v1(auth_user_id, channel_id):
    return {
        'name': 'Hayden',
        'owner_members': [
            {
                'u_id': 1,
                'email': 'example@gmail.com',
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
                'handle_str': 'haydenjacobs',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'email': 'example@gmail.com',
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
                'handle_str': 'haydenjacobs',
            }
        ],
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

    # Access channel and user lists
    store = data_store.get()
    channels = store['channels']
    users = store['users']
    # Get user data from user list for given auth_user_id
    user_data_append = users[auth_user_id]
    
    
    #Check if channel exists, is public, is global owner, is already a member 
    channel_access = False 
    user_in_channel = False
    channel_to_join = None

    for channel in channels:

        # Check if channel exists and save correct channel
        if channel['cid'] == channel_id:
            channel_to_join = channel

            # If channel exists, check if it is public 
            if channel['is_public'] == True:
                channel_access = True 
        
            # If channel exists, check if user is already in channel 
            users = channel['users']
            for user in users:
                if user['uid'] == auth_user_id:
                    user_in_channel = True
                break
            break 

    # Check if user is a global owner 
    if auth_user_id == 0:
        channel_access = True   

    # Access error 
    if channel_access == False:
        raise error.AccessError ("ERROR: You do not have access to this private channel")
    
    # Input error 
    if channel_to_join == None:
        raise error.InputError ("ERROR: Channel does not exist")

    if user_in_channel == True:
        raise error.InputError ("ERROR: You have already joined this channel")         
        
    # Append member if all conditions met
    if channel_to_join != None and channel_access == True and user_in_channel == False:
        member_list = channel_to_join['all_members']
        member_list.append(user_data_append)

    
    
    return {}
