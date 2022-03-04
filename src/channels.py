from src.data_store import data_store
from src.error import AccessError
from src.other import clear_v1
from src.auth import auth_register_v1

def channels_list_v1(auth_user_id):
    pass

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

