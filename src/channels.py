from src.data_store import data_store
from src.error import InputError, AccessError
from src.helpers import decode_token
from src.helpers import check_if_token_exists
from time import time

def channels_list_v2(token):

    '''
    Returns a list of of dictionaries in {channels}, 
    where the list is made up of dictionairies 
    containing types {channel_id, name} if it 
    corresponds to the given user id. The channels 
    returned include private and public channels. 

    Arguments:
        <token> (str)

    Exceptions:
        AccessError  - Occurs when invalid token is passed

    Return Value:
        Returns {channels} which contains a 
        list of dictionaries {channel_id, name} when
        (token) is input
    '''

    # initialise datastore and dicts
    data = data_store.get()
    channels_list = data['channels']
    channels_dict = {'channels' : []}
    
    # if token doesnt exist return AccessError
    if not check_if_token_exists(token):
        raise AccessError(description="Invalid token")
    
    u_id = int(decode_token(token))

    # loop through data_store and if u_id is in channel
    # add channels and names to dict
    for channel in channels_list:
        for member in channel['all_members']:
            if u_id == member['u_id']:
                channel_id = channel['channel_id']
                name = channel['name']
                channels_dict['channels'].append({'channel_id' : channel_id, 'name' : name})

    return channels_dict

def channels_listall_v2(token):
    '''
    Returns a list of of dictionaries in {channels}, 
    where the list is made up of dictionairies 
    containing types {channel_id, name} regardless if it 
    corresponds to the given user id. The channels 
    returned include private and public channels. 

    Arguments:
        <token> (str)

    Exceptions:
        AccessError  - Occurs when invalid token is passed

    Return Value:
        Returns {channels} which contains a 
        list of dictionaries {channel_id, name} when
        (token) is input
    '''

    # initialise datastore and dict
    data = data_store.get()
    channels_list = data['channels']
    channels_dict = {'channels' : []}
    
    # if token doesnt exist return AccessError
    if not check_if_token_exists(token):
        raise AccessError(description="Invalid token")
    
    # loop through and grab all channel and name variables
    for channel in channels_list:
        channel_id = channel['channel_id']
        name = channel['name']
        channels_dict['channels'].append({'channel_id' : channel_id, 'name' : name})

    data_store.set(data)

    return channels_dict


def channels_create_v2(token, name, is_public):
    '''
    This function allows an authorized user to create a channel

    Arguments:
    token(string) - This is the token of authorised usre to create a channel
    This means that the authrised user is the owner member and a member of the channel crated.
    name(string) - this is the name of the channel
    is_public(boolean) - This is whether the channel is public to others

    Exceptions:
    InputError: An input error is raised when the channel name is less than 1 character or 
    the channel name is more than 20 characters
    AccessError: When the token does not refer to a valid user

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
        }
    ]
    all_members_list = host_info_list
    owner_members_list = host_info_list.copy()
    channel_id = len(data["channels"])

    # error
    if len(name) < 1 or len(name) > 20:
        raise InputError(description="length of name is less than 1 or more than 20 characters")

    time_stamp = int(time())

    data["channels"].append(
        {
            'channel_id': channel_id,
            'name': name,
            'is_public': is_public,
            'time_stamp': time_stamp,
            'messages': [],
            'owner_members': owner_members_list,
            'all_members': all_members_list,
        }
    )

    data_store.set(data)

    return {
        'channel_id': channel_id,
    }