from src.data_store import data_store
from src.error import InputError, AccessError
from src.helpers import decode_token
from src.helpers import check_if_token_exists


def channels_list_v1(auth_user_id):

    '''
    Returns a list of of dictionaries in {channels}, where the list is made up of dictionairies 
    containing types {channel_id, name} if it corresponds to the given user id. The channels 
    returned include private and public channels. 

    Arguments:
        <auth_user_id> (int) -  is the user_id generated by auth_register_v1 when a user is first
                                registered
        
    Exceptions:
        AccessError  - Occurs when invalid auth_user_id

    Return Value:
        Returns {channels} which contains a list of dictionaries {channel_id, name} when
        (auth_user_id) is input
    '''

    # initialise datastore and dicts
    data = data_store.get()
    channels_list = data['channels']
    channels_dict = {'channels' : []}
    
    # if auth_user_id doesnt exist return AccessError
    if type(auth_user_id) != int:
        raise AccessError("ERROR: Invalid auth_user_id type")

    users_list = data['users']
    match = 0
    for user in users_list:
        if auth_user_id == user['u_id']:
            match += 1
    if match == 0:
        raise AccessError("ERROR: Invalid auth_user_id")

    # loop through data_store and if u_id is in channel
    # add channels and names to dict
    for channel in channels_list:
        for member in channel['all_members']:
            if auth_user_id == member['u_id']:
                channel_id = channel['channel_id']
                name = channel['name']
                channels_dict['channels'].append({'channel_id' : channel_id, 'name' : name})

    return channels_dict

def channels_listall_v1(auth_user_id):

    '''
    Returns a list of of dictionaries in {channels}, where the list is made up of dictionairies 
    containing types {channel_id, name} regardless if it corresponds to the given user id. The 
    channels returned include private and public channels. 

    Arguments:
        <auth_user_id> (int) -  is the user_id generated by auth_register_v1 when a user 
                                is first registered
        
    Exceptions:
        AccessError  - Occurs when invalid auth_user_id

    Return Value:
        Returns {channels} which contains a list of dictionaries {channel_id, name} when
        (auth_user_id) is input
    '''
    # initialise datastore and dict
    data = data_store.get()
    channels_list = data['channels']
    channels_dict = {'channels' : []}
    
    # if auth_user_id doesnt exist return AccessError
    if type(auth_user_id) != int:
        raise AccessError("ERROR: Invalid auth_user_id type")

    users_list = data['users']
    match = 0
    for user in users_list:
        if auth_user_id == user['u_id']:
            match += 1
    if match == 0:
        raise AccessError("ERROR: Invalid auth_user_id")
    
    # loop through and grab all channel and name variables
    for channel in channels_list:
        channel_id = channel['channel_id']
        name = channel['name']
        channels_dict['channels'].append({'channel_id' : channel_id, 'name' : name})

    data_store.set(data)

    return channels_dict



def channels_create_v1(token, channel_name, is_public):
    '''
    This function allows an authorized user to create a channel

    Arguments:
    auth_user_id(integer) - This is the user id of the user authorized to create the channel. 
    This means that the authrised user is the owner member and a member of the channel crated.
    
    name - this is the name of the channel
    
    is_public - This is whether the channel is public to others

    Exceptions:
    InputError: An input error is raised when the channel name is less than 1 character or 
    the channel name is more than 20 characters

    Return Value:
    The function will return a dictionary that contains the channel_id of this channel
    '''

    data = data_store.get()
    if not check_if_token_exists(token):
        raise AccessError(description="Invalid token")
    
    auth_user_id = int(decode_token(token))
    host_info = data["users"][auth_user_id]

    host_info_list = [
        {
            'u_id': host_info["u_id"],
            'email': host_info["email"],
            'name_first': host_info["name_first"],
            'name_last': host_info["name_last"],
            'handle_str': host_info["handle_str"],
        }
    ]
    all_members_list = host_info_list
    owner_members_list = host_info_list.copy()
    channel_id = len(data["channels"])

    # error
    if len(channel_name) < 1 or len(channel_name) > 20:
        raise InputError("length of name is less than 1 or more than 20 characters")

    data["channels"].append(
        {
            'channel_id': channel_id,
            'name': channel_name,
            'is_public': is_public,
            'owner_members': owner_members_list,
            'all_members': all_members_list,
        }
    )

    data_store.set(data)

    return {
        'channel_id': channel_id,
    }
