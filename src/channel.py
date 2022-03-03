from src.data_store import data
from src.error import InputError, AccessError

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

    # Check whether channel_id exist in the database
    channel_exist = 0
    for channel in data['channels']:
        if channel['id'] == channel_id:
            channel_exist = 1
    if channel_exist == 0:
        raise InputError(description = "Error occurred channel_id is not in database")
    
    u_id = auth_user_id['auth_user_id']
    
    # Check user is a member in channel_id
    authorised_user = 0
    for channel in data['channels']:
        for member in channel['all_members']:
            if member['u_id'] == u_id:
                authorised_user = 1
    if authorised_user == 0:
        raise AccessError(description = "Error occurred authorised user is not a member of channel_id")

    # Retrieves all messages and also number of messages
    for channel in data['channels']:
        if channel['id'] == channel_id:
            messages = list(channel['messages'])
            num_messages = len(messages)
    
    # When there is no messages
    if num_messages == 0 and start == 0:
        return {
            'messages': [], 
            'start': start, 
            'end': -1
        }
    
    if start >= num_messages:
        raise InputError(description = "Error occurred start value is greater than the number of messages")

    # Iterating through list to collect messages
    end = start + 50
    message_array = []
    
    for num in range(51):
        index = start + num
        if index >= num_messages or index >= end:
            break

        message_array.append({
            'message_id': messages[index].get('message_id'),
            'u_id': messages[index].get('u_id'),
            'message': messages[index].get('message'),
            'time_created': messages[index].get('time_created'),
        })
    
    if num < 50:
        end = -1

    return {
        'messages': message_array,
        'start': start,
        'end': end,
    }

def channel_join_v1(auth_user_id, channel_id):
    return {
    }
