from src.data_store import data_store
from src.error import InputError, AccessError

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

    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }


def channels_create_v1(auth_user_id, channel_name, is_public):
    data = data_store.get()
    
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

    channel_id = len(data["channels"])

    # error
    if len(channel_name) < 1 or len(channel_name) > 20:
        raise InputError("length of name is less than 1 or more than 20 characters")

    data["channels"].append(
        {
            'channel_id': channel_id,
            'name': channel_name,
            'is_public': is_public,
            'owner_members': host_info_list,
            'all_members': host_info_list,
        }
    )

    data_store.set(data)

    return {
        'channel_id': channel_id,
    }
