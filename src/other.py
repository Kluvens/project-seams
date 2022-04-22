from src.data_store import data_store
from time import time

def clear_v1():
    '''
    clear_v1

    This clears the data structure.
    In particular its the users and channels dictionary.

    '''
    store = data_store.get()
    store['users'] = []
    store['removed_users'] = []
    store['channels'] = []
    store['dms'] = []
    store['unique_message_id'] = 0
    store['time_setup'] = int(time())
    data_store.set(store)
