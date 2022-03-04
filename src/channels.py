from src.data_store import data_store
from src.error import AccessError
from src.other import clear_v1
from src.auth import auth_register_v1

def channels_list_v1(auth_user_id):

    # if auth_user_id doesnt exist return AccessError
    try:
        auth_user_id + 1 - 1
    except:
        raise AccessError

    data = data_store.get()

    channels = data['channels']
    channel_id_list = []
    name_list = []

    for x in range(len(channels)):
        for y in range(len(channels[x]['all_members'])):
            if channels[x]['all_members'][y]['u_id'] == auth_user_id:
                channel_idv = (channels[x]['channel_id'])
                channel_id_list.append(channel_idv)
                namev = (channels[x]['name'])
                name_list.append(namev)

    data_store.set(data)

    return {
        'channels': [
            {
                'channel_id': [channel_id_list],
                'name': [name_list],
            }
        ],
    }


def channels_listall_v1(auth_user_id):
    return {
        'channels': [
            {
                'channel_id': 1,
                'name': 'My Channel',
            }
        ],
    }

def channels_create_v1(auth_user_id, name, is_public):

    return {
        'channel_id': 1,
    }
