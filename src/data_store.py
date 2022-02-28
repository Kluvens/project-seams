# This module will imported by other functions 
# and an instnace of the class defined below
# will be used to store user/channel data 

# Blueprint of standard data strucutre:
'''
data = {
    'users': [
        {
            'uid': 1,
            'email': "email.com1",
            'name_first': "name_first",
            'name_last': "name_last",
            'password': "password",
        },
        {
            'uid': 2,
            'email': "email.com2",
            'name_first': "name_first",
            'name_last': "name_last",
            'password': "password",
        },
    ],
    'channels': [
        {
            'cid': 1,
            'name' : 'channel1',
            'is_public': True,
            'owner_members': [
                {
                    'uid': 1,
                    'email': 'example@gmail.com',
                    'name_first': 'Hayden',
                    'name_last': 'Jacobs',
                    'handle_str': 'haydenjacobs',
                }
            ],
            'all_members': [
                {
                    'uid': 1,
                    'email': 'example@gmail.com',
                    'name_first': 'Hayden',
                    'name_last': 'Jacobs',
                    'handle_str': 'haydenjacobs',
                }
            ],
        },
        {
            'cid': 2,
            'name' : 'channel2',
            'is_public': True,
            'owner_members': [
                {
                    'uid': 1,
                    'email': 'example@gmail.com',
                    'name_first': 'Hayden',
                    'name_last': 'Jacobs',
                    'handle_str': 'haydenjacobs',
                }
            ],
            'all_members': [
                {
                    'uid': 1,
                    'email': 'example@gmail.com',
                    'name_first': 'Hayden',
                    'name_last': 'Jacobs',
                    'handle_str': 'haydenjacobs',
                }
            ],
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
