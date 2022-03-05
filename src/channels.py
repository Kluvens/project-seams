from src.data_store import data_store
from src.error import AccessError
from src.other import clear_v1
from src.auth import auth_register_v1

def channels_list_v1(auth_user_id):
    return {
        'channels': [
            {
                'channel_id': 1,
                'name': 'My Channel',
            }
        ],
    }

def channels_listall_v1(auth_user_id):

    # if auth_user_id doesnt exist return AccessError
    try:
        auth_user_id + 1 - 1
    except:
        raise AccessError

    data = data_store.get()
    channels_list = data['channels']
    channels_dict = {'channels' : []}
    
    # loop through and grab all channel and name variables
    for channel in channels_list:
        channel_id = channel['channel_id']
        name = channel['name']
        channels_dict['channels'].append({'channel_id' : channel_id, 'name' : name})

    data_store.set(data)

    return channels_dict

def channels_create_v1(auth_user_id, name, is_public):
    return {
        'channel_id': 1,
    }


