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
    'users': [
        {
            'u_id': 0,
            'email': "email.com1",
            'name_first': "name_first",
            'name_last': "name_last",
            'password': "password",
            'permission': 
        },
        {
            'u_id': 1,
            'email': "email.com2",
            'name_first': "name_first",
            'name_last': "name_last",
            'password': "password",
            'permission'
        },
    ],
    'channels': [
        {
            'channel_id': 0,
            'name' : 'channel0',
            'is_public': True,
            'messages': [
                {
                    'message_id': 0,
                    'u_id': 0,
                    'message': 'Hello world',
                    'time_sent': 1582426789,
                },
            ],
            'owner_members': [
                {
                    'u_id': 0,
                    'email': 'example@gmail.com',
                    'name_first': 'Hayden',
                    'name_last': 'Jacobs',
                    'handle_str': 'haydenjacobs',
                }
            ],
            'all_members': [
                {
                    'u_id': 0,
                    'email': 'example@gmail.com',
                    'name_first': 'Hayden',
                    'name_last': 'Jacobs',
                    'handle_str': 'haydenjacobs',
                }
            ],
        },
        {
            'channel_id': 1,
            'name' : 'channel1',
            'is_public': True,
            'owner_members': [
                {
                    'u_id': 0,
                    'email': 'example@gmail.com',
                    'name_first': 'Hayden',
                    'name_last': 'Jacobs',
                    'handle_str': 'haydenjacobs',
                }
            ],
            'all_members': [
                {
                    'u_id': 0,
                    'email': 'example@gmail.com',
                    'name_first': 'Hayden',
                    'name_last': 'Jacobs',
                    'handle_str': 'haydenjacobs',
                }
            ],
            'messages': [
                {
                    'message_id': 0,
                    'u_id': 0,
                    'message': 'Bye world',
                    'time_sent': 1582426790,
                },
            ],
        },
    ],
}
'''