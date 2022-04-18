# This module will imported by other functions 
# and an instnace of the class defined below
# will be used to store data 

# Blueprint of standard data strucutre:

initial_object = {
    'users' : [],
    'reset_codes' : [],
    'removed_users' : [],
    'channels' : [],
    'dms': [],
    'unique_message_id': 0,
}

## YOU ARE ALLOWED TO CHANGE THE BELOW IF YOU WISH
class Datastore:
    def __init__(self):
        self.__store = initial_object

    def get(self):
        return self.__store

    def set(self, store):
        if not isinstance(store, dict):
            raise TypeError('store must be of type dictionary')
        self.__store = store

print('Loading Datastore...')

global data_store
data_store = Datastore()

'''
data = {
    'users': [],
    'channels': [];
    'dms': [],
    'removed_users' : [],
    'unique_message_id': int,
}

'users': [
    {
        'u_id': int,
        'email': str,
        'name_first': str,
        'name_last': str,
        'handle_str': str,
        'password': str,
        'permisson': int,
    }
]

'channels': [
    {
        'channel_id': int,
        'name': str,
        'is_public': boolean,
        'time_stamp': int unix,
        'owner_members': [
            {
                'u_id': int,
            }
        ]
        'all_members': [
            {
                'u_id': int,
            }
        ]
        'messages': [
            'message_id': int,
            'u_id': int,
            'message': str,
            'time_sent': int unix,
            'is_pinned': boolean,
        ]
    }
]

'dms': [
    {
        'dm_id': int,
        'name': str,
        'time_stamp': int unix,
        'owner_members': [
            {
                'u_id': int,
            }
        ]
        'all_members': [
            {
                'u_id': int,
            }
        ]
        'messages': [
            'message_id': int,
            'u_id': int,
            'message': str,
            'time_sent': int unix,
            'is_pinned': boolean,
        ]
    }
]
'''
