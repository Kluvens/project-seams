from src.data_store import data_store

def clear_v1():
    '''
    clear_v1

    This clears the data structure.
    In particular its the users and channels dictionary.

    '''
    store = data_store.get()
    store['users'] = []
    store['channels'] = []
    data_store.set(store)
