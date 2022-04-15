from time import time
from src.dms import find_dm_index, is_in_dm
from src.data_store import data_store
from src.helpers import check_if_token_exists, decode_token, is_global_owner
from src.error import AccessError, InputError
from src.helper import is_in_channel_owner, is_in_dm_owner

def message_senddm_v1(token, dm_id, message):
    '''
    send a message in dm with unique message_id

    Arguments:
        token - the auth user who wants to send a message in the dm
        dm_id - the dm the auth user wants to send message
        message - the detailed content of the message

    Exceptions:
        InputError - dm_id does not refer to a valid DM
        InputError - length of message is less than 1 or over 1000 characters
        AccessError - dm_id is valid and the authorised user is not a member of the DM

    Return:
        { message_id } - the unique identifier of the message created
    '''
    data = data_store.get()
    dms = data['dms']

    # if token doesnt exist return AccessError
    if not check_if_token_exists(token):
        raise AccessError(description="Invalid token")
    auth_user_id = int(decode_token(token))

    right_dm_index = find_dm_index(dms, dm_id)

    # error
    if right_dm_index is None:
        raise InputError(description="dm_id does not refer to a valid dm")

    if len(message) < 1 or len(message) > 1000:
        raise InputError(description="length of message is less than 1 or over 1000 characters")
    
    right_dm = dms[right_dm_index]

    # check if is in dm
    if not is_in_dm(auth_user_id, right_dm):
        raise AccessError(description="dm_id is valid and the authorised user is not a member of the dm")
    if not 'messages' in right_dm:
        right_dm["messages"] = []

    data['unique_message_id'] += 1
    
    # all checks passed, append to the messages
    right_dm['messages'].append(
        {
            'message_id': data['unique_message_id'],
            'u_id': auth_user_id,
            'message': message,
            'time_sent': int(time()),
            'is_pinned': False,
        }
    )

    return {
        'message_id': data['unique_message_id']
    }

def message_send_v1(token, channel_id, message):
    '''
    message_send_v1

    Sends a message from the authorised user to the channel specified by channel_id.

    Arguments
    token (string) - This is the token of a user.
    channel_id (integer) - This is the channel id of the channel that the authorised user 
    would like to see the messages of.
    message (string) - The message string which will be sent to the channel message

    Exceptions:
    InputError - An input error is raised when the channel id is not valid
    or the length of message is less than 1 or more than 1000 characters.

    AccessError - An access error is raised when the authorised user is not an owner
    or an existing member of the channel

    Return Value:
    This function returns message_id (integer), which is a completely unique ID.
    '''
    # Checking if message string is less than 1 character long
    if len(message) < 1:
        raise InputError(description="Error occurred, no message was received")

    # Checking if message string is more than 1000 characters long
    elif len(message) > 1000:
        raise InputError(description="Error occurred, message is more than 1000 characters")

    data = data_store.get()

    # Check if token is valid using helper
    if check_if_token_exists(token) == False:
        raise AccessError(description="Error occured, invalid token'")

    # Check whether channel_id exist in the database
    channel_exist = False
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            channel_exist = True
    if not channel_exist:
        raise InputError(description="Error occurred, channel_id is not in database")
    
    # Check user is a member in channel_id
    auth_user_id = int(decode_token(token))

    authorised_user = False
    for channel in data['channels']:
        for member in channel['all_members']:
            if member['u_id'] == auth_user_id:
                authorised_user = True
    if not authorised_user:
        raise AccessError(description="Error occurred, authorised user is not a member of channel_id")

    # Ensuring message_id will be unique
    data['unique_message_id'] += 1
    
    messages_dict = {
        'message_id': data['unique_message_id'],
        'u_id': auth_user_id,
        'message': message,
        'time_sent': int(time()),
        'is_pinned': False,
        }

    for channel in data['channels']:
        if channel_id == channel['channel_id']:
            if 'messages' in channel:
                channel["messages"].append(messages_dict)

    return {
        'message_id': data['unique_message_id'],
    }

def message_remove_v1(token, message_id):
    '''
    message_remove_v1

    Given a message_id, the message string is deleted.

    Arguments
    token (string) - This is the token of a user.
    message_id (integer) - This is the unique ID to identify which message will be deleted.

    Exceptions:
    InputError - An input error is raised when the message_id does not refer to a valid message within a channel/DM that the authorised user has joined.

    AccessError - An access error is raised when the authorised user is either not a global owner or an owner member of the channel or the sender of the message.

    Return Value:
    This function returns an empty dictionary.
    '''
    data = data_store.get()
    assert "channels" in data

    # Check if token is valid using helper
    if check_if_token_exists(token) == False:
        raise AccessError(description="Error occured, invalid token'")
    
    auth_user_id = int(decode_token(token))
    
    # Check if user is authorised to delete message and message_id is valid
    authorised_user = is_global_owner(auth_user_id)
    message_exist = False

    for channel in data['channels']:
        for message in channel['messages']:
            # Confirms message_id is valid
            if message_id == message['message_id']:
                message_exist = True
                # Checking if member is authorised to delete message
                for owner in channel['owner_members']:
                    if auth_user_id == owner['u_id']:
                        authorised_user = True
                        channel['messages'].remove(message)
                    elif auth_user_id == message['u_id']:
                        authorised_user = True
                        channel['messages'].remove(message)
                    elif authorised_user:
                        channel['messages'].remove(message)

    if not message_exist:
        raise InputError(description="Error occurred, message_id is not in database")
    
    if not authorised_user:
        raise AccessError(description="Error occured, user does not have access to delete this message_id")
    
    return {}

def message_edit_v1(token, message_id, message):
    '''
    message_edit_v1

    Given a message_id, update its current message string with a new given message. If the new message is an empty string, the message is deleted.

    Arguments
    token (string) - This is the token of a user.
    message_id (integer) - This is the unique ID to identify which message will be edited.
    message (string) - The message string which will be replacing the existing message.

    Exceptions:
    InputError - An input error is raised when the message_id does not refer to a valid message within a channel/DM that the authorised user has joined
    or the length of message is more than 1000 characters.

    AccessError - An access error is raised when the authorised user is either not a global owner or an owner member of the channel or the sender of the message.

    Return Value:
    This function returns an empty dictionary.
    '''
    # Checking if message string is less than 1 character long so we can call message_remove_v1
    if len(message) < 1:
        return message_remove_v1(token, message_id)

    # Checking if message string is more than 1000 characters long
    elif len(message) > 1000:
        raise InputError(description="Error occurred, message is more than 1000 characters")

    data = data_store.get()
    assert "channels" in data
    # assert "token" in data

    # Check if token is valid using helper
    if check_if_token_exists(token) == False:
        raise AccessError(description="Error occured, invalid token'")
    
    auth_user_id = int(decode_token(token))
    
    # Check if user is authorised to edit message and message_id is valid
    authorised_user = is_global_owner(auth_user_id)
    message_exist = False
    new_message = message

    for channel in data['channels']:
        for message_dict in channel['messages']:
            if message_dict['message_id'] == message_id:
                message_exist = True
                # Checking if member is authorised to edit message
                for owner in channel['owner_members']:
                    if auth_user_id == owner['u_id']:
                        authorised_user = True
                        message_dict['message'] = new_message
                    elif auth_user_id == message_dict["u_id"]:
                        authorised_user = True
                        message_dict['message'] = new_message
                    elif authorised_user:
                        message_dict['message'] = new_message

    if not message_exist:
        raise InputError(
            description="Error occurred, message_id is not in database")
    
    if not authorised_user:
        raise AccessError(
            description="Error occured, user does not have access to edit this message_id")
    
    return {}

def message_pin_v1(token, message_id):
    '''
    The function is used to pin a message in channel or dm

    Arguments:
        token - the auth user who wants to pin the message
        message_id - the message may be pinned

    Exceptions:
        InputError - message_id is not a valid message within a channel or DM that the authorised user has joined
        InputError - the message is already pinned
        AccessError - invalid token
        AccessError - message_id refers to a valid message in a joined channel/DM and the authorised user does not have owner permissions in the channel/DM

    Return:
        {}
    '''
    valid_message = False
    message_already_pinned = False
    user_has_permission = False

    if check_if_token_exists(token) == False:
        raise AccessError(description="Error occured, invalid token'")
    
    auth_user_id = int(decode_token(token))

    data = data_store.get()
    channels = data['channels']
    dms = data['dms']

    # pin the message if it is in the channel
    for channel in channels:
        for message in channel['messages']:
            can_change = True
            if message['message_id'] == message_id:
                valid_message = True
                if is_global_owner(auth_user_id) or is_in_channel_owner(auth_user_id, channel):               
                    user_has_permission = True
                else:
                    can_change = False
                if message['is_pinned'] == True:
                    message_already_pinned = True
                    can_change = False
                if can_change:
                    message['is_pinned'] = True

    # pin the message if it is in the dm
    for dm in dms:
        for message in dm['messages']:
            can_change = True
            if message['message_id'] == message_id:
                valid_message = True
                if is_global_owner(auth_user_id) or is_in_dm_owner(auth_user_id, dm):               
                    user_has_permission = True
                else:
                    can_change = False
                if message['is_pinned'] == True:
                    message_already_pinned = True
                    can_change = False
                if can_change:
                    message['is_pinned'] = True

    if not valid_message:
        raise InputError(description="message_id is not a valid message within a channel or DM that the authorised user has joined")

    if not user_has_permission:
        raise AccessError(description="message_id refers to a valid message in a joined channel/DM and the authorised user does not have owner permissions in the channel/DM")

    if message_already_pinned:
        raise InputError(description="the message is already pinned")

    return {}

def message_unpin_v1(token, message_id):
    '''
    the function is used to unpin a message

    Arguments:
        token - the auth user who wants to unpin the message
        message_id - the message to be unpinned

    Exceptions:
        InputError - message_id is not a valid message within a channel or DM that the authorised user has joined
        InputError - the message is not already pinned
        AccessError - invalid token
        AccessError - message_id refers to a valid message in a joined channel/DM and the authorised user does not have owner permissions in the channel/DM

    Return:
        {}
    '''
    valid_message = False
    message_already_unpinned = False
    user_has_permission = False

    if check_if_token_exists(token) == False:
        raise AccessError(description="Error occured, invalid token'")
    
    auth_user_id = int(decode_token(token))

    data = data_store.get()
    channels = data['channels']
    dms = data['dms']

    # unpin the message if in channel
    for channel in channels:
        for message in channel['messages']:
            can_change = True
            if message['message_id'] == message_id:
                valid_message = True
                if is_global_owner(auth_user_id) or is_in_channel_owner(auth_user_id, channel):               
                    user_has_permission = True
                else:
                    can_change = False
                if message['is_pinned'] == False:
                    message_already_unpinned = True
                    can_change = False
                if can_change:
                    message['is_pinned'] = False

    # unpin the message if in dm
    for dm in dms:
        for message in dm['messages']:
            can_change = True
            if message['message_id'] == message_id:
                valid_message = True
                if is_global_owner(auth_user_id) or is_in_dm_owner(auth_user_id, dm):               
                    user_has_permission = True
                else:
                    can_change = False
                if message['is_pinned'] == False:
                    message_already_unpinned = True
                    can_change = False
                if can_change:
                    message['is_pinned'] = False
    
    if not valid_message:
        raise InputError(description="message_id is not a valid message within a channel or DM that the authorised user has joined")
    
    if not user_has_permission:
        raise AccessError(description="message_id refers to a valid message in a joined channel/DM and the authorised user does not have owner permissions in the channel/DM")

    if message_already_unpinned:
        raise InputError(description="the message is not already pinned")

    return {}


    
