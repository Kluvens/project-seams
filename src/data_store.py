# This module will imported by other functions 
# and an instnace of the class defined below
# will be used to store user/channel data 

# Blueprint of standard data strucutre:
'''
data = {
    'users': [
        {
            'u_id': 0,
            'email': "email1@gmail.com",
            'name_first': "name_first",
            'name_last': "name_last",
            'password': "password",
            'handle_str' : "namefirstnamelast"
        },
        {
            'u_id': 1,
            'email': "email2@gmail.com",
            'name_first': "name_first",
            'name_last': "name_last",
            'password': "password",
            'handle_str' : "namefirstnamelast0"
        },
    ],
        'channels': [
        {
            'channel_id': 0,
            'name' : 'channel0',
            'is_public': True,
            'owner_members': [
                {
                    'u_id': 0,
                }
            ],
            'all_members': [
                {
                    'u_id': 1,
                }
            ],
            'messages': [
                {
                    'message_id': 0,
                    'u_id': 0,
                }
            ]
        },
        {
            'channel_id': 1,
            'name' : 'channel1',
            'is_public': True,
            'owner_members': [
                {
                    'u_id': 0,
                }
            ],
            'all_members': [
                {
                    'u_id': 0,
                }
            ],
            'messages': [
                {
                    'message_id': 0,
                    'u_id': 0,
                }
            ]
        },
    ],
}
'''

initial_object = {
    'users' : [],
    'channels' : [],
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
