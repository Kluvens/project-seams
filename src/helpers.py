def check_if_token_exists(str: token) -> bool
    '''
    This is a helper function that takes in
    a token string and returns a boolean value

    if the token is found in the sessions list
    it will return True. Otherwise, it will return
    False.
    '''

    # The data access related code will need to 
    # be changed when we implement data persistance.
    data = data_store.get()
    sessions = data['sessions']
    users = data['users']
    if sessions = {}:
        # user is not logged from any device
        return False

    for user in users:
        if user['token'] in sessions:
            return True
    return False


