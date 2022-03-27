from src.data_store import data_store
from src.error import AccessError, InputError
from src.helpers import check_if_token_exists, decode_token

def dm_messages_v1(token, dm_id, start):
    '''
    dm_messages_v1

    This function outputs upto 50 messages in dm_id between index start and start + 50.

    Arguments
    token (string) - This is the token of a user.
    dm_id (integer) - This is the dm id of the DM that the authorised user 
    would like to see the messages of.
    start (integer) - The start index of the messages array which will be returned.

    Exceptions:
    InputError - An input error is raised when the dm_id is not valid or either the start is greater 
    than the total number of messages in the DM
    AccessError - An access error is raised when the authorised user is not an owner
    or an existing member of the DM

    Return Value:
    This function returns the messages array from the DM, the start index and the end index.
    '''
    data = data_store.get()
    dm_id = int(dm_id)
    start = int(start)
    # Check if token is valid using helper
    if not check_if_token_exists(token):
        raise AccessError("Error occured, invalid token'")

    # Check whether dm_id exist in the database

    dm_exist = False
    for dm in data['dms']:
        if dm['dm_id'] == dm_id:
            dm_exist = True
    if not dm_exist:
        raise InputError("Error occurred dm_id is not in database")
    
    # Check user is a member in dm_id
    auth_user_id = int(decode_token(token))

    authorised_user = False
    for dm in data['dms']:
        for member in dm['all_members']:
            if member['u_id'] == auth_user_id:
                authorised_user = True
    if not authorised_user:
        raise AccessError("Error occurred authorised user is not a member of channel_id")

    # Retrieves all messages and also number of messages
    num_messages = 0
    for dm in data['dms']:
        if dm['dm_id'] == dm_id:
            if 'messages' in data['dms'][dm_id]:
                found_messages = dm['messages']
                num_messages = len(found_messages)
            else:
                data['dms'][dm_id]['messages'] = []
    
    if start > num_messages:
        raise InputError("Error occurred, start value is greater than the number of messages")

    # When there is no messages
    if num_messages == 0 and start == 0:
        return {
            'messages': [], 
            'start': start, 
            'end': -1
        }

    # Iterating through list to collect messages
    end = start + 50
    message_array = []
    
    for num in range(51):
        index = start + num
        if index >= num_messages or index >= end:
            break

        message_array.append({
            'message_id': found_messages[index].get('message_id'),
            'u_id': found_messages[index].get('u_id'),
            'message': found_messages[index].get('message'),
            'time_sent': found_messages[index].get('time_sent'),
        })

    if num < 50:
        end = -1

    return {
        'messages': message_array,
        'start': start,
        'end': end,
    }
