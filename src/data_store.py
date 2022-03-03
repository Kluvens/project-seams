'''
data_store.py

This contains a definition for a Datastore class which you should use to store your data.
You don't need to understand how it works at this point, just how to use it :)

The data_store variable is global, meaning that so long as you import it into any
python file in src, you can access its contents.

Example usage:

    from data_store import data_store

    store = data_store.get()
    print(store) # Prints { 'names': ['Nick', 'Emily', 'Hayden', 'Rob'] }

    names = store['names']

    names.remove('Rob')
    names.append('Jake')
    names.sort()

    print(store) # Prints { 'names': ['Emily', 'Hayden', 'Jake', 'Nick'] }
    data_store.set(store)
'''

## YOU SHOULD MODIFY THIS OBJECT BELOW
initial_object = {
    'users': [],
    'channels' : []
}
## YOU SHOULD MODIFY THIS OBJECT ABOVE

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
            'messages': [
                {
                    'message_id': 1,
                    'u_id': 1,
                    'message': 'Hello world',
                    'time_created': 1582426789,
                },
            ],
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
