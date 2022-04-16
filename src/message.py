from base64 import decode
from time import time
from src.dms import find_dm_index, is_in_dm
from src.data_store import data_store
from src.helpers import check_if_token_exists, decode_token, is_global_owner,find_message_from_message_id, find_channeldm_from_message
from src.error import AccessError, InputError

def message_senddm_v1(token, dm_id, message):
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
    print(right_dm)

    if not is_in_dm(auth_user_id, right_dm):
        raise AccessError(description="dm_id is valid and the authorised user is not a member of the dm")
    if not 'messages' in right_dm:
        right_dm["messages"] = []

    data['unique_message_id'] += 1
    
    right_dm['messages'].append(
        {
            'message_id': data['unique_message_id'],
            'u_id': auth_user_id,
            'message': message,
            'time_sent': int(time()),
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
    assert "channels" in data
    # assert "token" in data

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
        'time_sent': int(time())
        }

    for channel in data['channels']:
        if channel_id == channel['channel_id']:
            if 'messages' in channel:
                channel["messages"].append(messages_dict)
            else:
                channel["messages"] = [messages_dict]

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
    # assert "token" in data

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

# ========================================== MESSAGE SHARE =================================================
def message_share_v1(token,og_message_id,message,channel_id,dm_id):

    # Check if token is invalid
    if not check_if_token_exists(token):
        raise AccessError(description="ERROR: Token is invalid")

    # Decode token to u_id
    u_id = decode_token(token)['u_id']

    # Check message is from channel or dm that authorized user belongs to
    og_is_channel = find_channeldm_from_message(og_message_id)['is_channel']
    og_is_dm = find_channeldm_from_message(og_message_id)['is_dm']

    # If in channel, find the relevant channel id and check if token user is part of channel
    channels = data_store.get()['channels']
    if og_is_channel:
        og_channel_id = find_channeldm_from_message(og_message_id)['id']
        og_channel_members = [channel['all_members'] for channel in channels if channel['channel_id'] == og_channel_id][0]
        og_channel_member_ids = [member['u_id'] for member in og_channel_members]
        if not u_id in og_channel_member_ids:
            raise InputError(description = 'ERROR: User does not have access to the message they are sharing')

    # If in dm, find the relevant dm_id 
    dms = data_store.get()['dms']
    if og_is_dm:
        og_dm_id = find_channeldm_from_message(og_message_id)['id']
        og_dm_members = [dm['all_members'] for dm in dms if dm['dm_id'] == og_dm_id][0]
        og_dm_member_ids = [member['u_id'] for member in og_dm_members]
        if not u_id in og_dm_member_ids:
            raise InputError(description = 'ERROR: User does not have access to the message they are sharing')

    # Check at least one out of dm_id and channel_id are -1
    if not dm_id == -1 and not channel_id == -1:
        raise InputError(description= 'ERROR: Neither channel id nor dm id are -1 ')

    # Check message length is less than 1000 characters
    if len(message) > 1000:
        raise InputError(description= 'ERROR: Appended message exceeds 1000 characters')
    
    # Find message from message id 
    message_to_share = find_message_from_message_id(og_message_id)
    # Check message exists 
    if message_to_share is None:
        raise InputError(description = 'ERROR: There is no message related to the given message id')

    # Generate new message
    new_message = "{}\n >>> {}".format(message_to_share,message)

    # Check token user is part of channel or dm they are sharing to
    if dm_id == -1:
        channel_members = [channel['all_members'] for channel in channels if channel['channel_id'] == channel_id][0]
        channel_members_ids = [member['u_ids'] for member in channel_members]
        if not u_id in channel_members_ids:
            raise AccessError(description= 'ERROR: Authorized user is not part of the channel they are sharing to')
        # Send new message
        shared_message_id = message_send_v1(token,channel_id,new_message)

    if channel_id == -1:
        dm_members = [dm['all_members'] for dm in dms if dm['dm_id'] == dm_id]
        dm_members_ids = [member['u_ids'] for member in dm_members]
        if not u_id in dm_members_ids:
            raise AccessError(description= 'ERROR: Authorized user is not part of DM they are sharing to')
        # Send new message
        shared_message_id = message_senddm_v1(token, dm_id,new_message)

    return {'shared_message_id': shared_message_id}