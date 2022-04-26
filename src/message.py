from time import time
import threading
from src.dms import find_dm_index, is_in_dm
from src.data_store import data_store
from src.helpers import check_if_token_exists, decode_token, is_global_owner
from src.error import AccessError, InputError
from src.helper import is_in_channel_owner, is_in_dm_owner
from src.helper import find_channel_index, find_dm_index
from src.helper import is_in_channel
from src.helpers import find_handle_in_message
from src.helpers import find_channeldm_from_message  
from src.helpers import find_message_sender 
from src.helpers import find_message_from_message_id

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
    dm_exist = False
    for dm in data['dms']:
        if dm['dm_id'] == dm_id:
            dm_exist = True
    if not dm_exist:
        raise InputError(description="Error occurred, channel_id is not in database")
    
    # Check user is a member in channel_id
    auth_user_id = int(decode_token(token))

    authorised_user = False
    for dm in data['dms']:
        for member in dm['all_members']:
            if member['u_id'] == auth_user_id:
                authorised_user = True
    if not authorised_user:
        raise AccessError(description="Error occurred, authorised user is not a member of channel_id")

    # ====================================================== NOTIFICATIONS INSERTION ===============================================================
    # Get information needed, put into notification dictionary
    sender_handle = [user['handle_str'] for user in users if user['token'] == token][0]
    dms = data_store.get()['dms']
    dm_name = [dm['dm_name'] for dm in dms if dm['dm_id'] == dm_id][0]
    message_preview = message[0:19] 
    notification_message = '{} tagged you in {}: {}'.format(sender_handle,dm_name,message_preview)
    notification = {
        'channel_id': '-1',
        'dm_id': dm_id,
        'notification_message': notification_message,
    }

    # Get handles of tagged users using helper function
    handles = find_handle_in_message(message)

    # Append notification to list of notifications specific to user
    users = data_store.get()['users']
    for handle in handles:
        user_listof_notifications = [user['notifications'] for user in users if user['handle_str'] == handle][0]
        user_listof_notifications.append(notification)
    # ================================================================================================================================================

    # Ensuring message_id will be unique
    data['unique_message_id'] += 1
    
    messages_dict = {
        'message_id': data['unique_message_id'],
        'u_id': auth_user_id,
        'message': message,
        'time_sent': int(time()),
        'is_pinned': False,
        'reacts' : []
        }

    for dm in data['dms']:
        if dm_id == dm['dm_id']:
            if 'messages' in dm:
                dm["messages"].append(messages_dict)
            else:
                dm["messages"] = [messages_dict]
    return {
        'message_id': data['unique_message_id'],
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
        'reacts' : []
        }

    # ============================================ NOTIFICATIONS INSERTION ===============================================================
    # Get information needed, put into notification dictionary
    channels = data_store.get()['channels']
    sender_handle = [user['handle_str'] for user in users if user['token'] == token][0]
    channel_name = [channel['channel_name'] for channel in channels if channel['channel_id'] == channel_id][0]
    message_preview = message[0:19] 
    notification_message = '{} tagged you in {}: {}'.format(sender_handle,channel_name,message_preview)
    notification = {
        'channel_id': channel_id,
        'dm_id': '-1',
        'notification_message': notification_message,
    }

    # Get handles of tagged users using helper function
    handles = find_handle_in_message(message)

    # Append notification to list of notifications specific to user
    users = data_store.get()['users']
    for handle in handles:
        user_listof_notifications = [user['notifications'] for user in users if user['handle_str'] == handle][0]
        user_listof_notifications.append(notification)
    # ======================================================================================================================================

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
        raise AccessError(description="Error occured, invalid token")

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

    # If not in channel messages, check dm messages
    if not message_exist:
        for dm in data['dms']:
            for message in dm['messages']:
                # Confirms message_id is valid
                if message_id == message['message_id']:
                    message_exist = True
                    # Checking if member is authorised to delete message
                    for owner in dm['owner_member']:
                        if auth_user_id == owner['u_id']:
                            authorised_user = True
                            dm['messages'].remove(message)
                        elif auth_user_id == message['u_id']:
                            authorised_user = True
                            dm['messages'].remove(message)

    if not message_exist:
        raise InputError(
            description="Error occurred, message_id is not in database")

    if not authorised_user:
        raise AccessError(
            description="Error occured, user does not have access to delete this message_id")

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
    # Checking if message string is less than 1 character long so we can call
    # message_remove_v1
    if len(message) < 1:
        return message_remove_v1(token, message_id)

    # Checking if message string is more than 1000 characters long
    elif len(message) > 1000:
        raise InputError(
            description="Error occurred, message is more than 1000 characters")

    data = data_store.get()
    assert "channels" in data
    assert "dms" in data

    # Check if token is valid using helper
    if check_if_token_exists(token) == False:
        raise AccessError(description="Error occured, invalid token")

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

    # If not in channel messages, check dm messages
    if not message_exist:
        for dm in data['dms']:
            for message_dict in dm['messages']:
                if message_dict['message_id'] == message_id:
                    message_exist = True
                    # Checking if member is authorised to edit message
                    for owner in dm['owner_member']:
                        if auth_user_id == owner['u_id']:
                            authorised_user = True
                            message_dict['message'] = new_message
                        elif auth_user_id == message_dict["u_id"]:
                            authorised_user = True
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



# def create_react_key(channels, channel_id):
#     for channel in channels:
#         if channel['channel_id'] == channel_id:
#             if channel['reacts'] not in channel:
#                 channel['reacts'] = []
########################## send later ############################


################ HELPER --> move to helpers if approved ##########

def validate_message_dm(message: str) -> bool:
    if not (0 <= len(message) <= 1000):
        return False
    return True

def send_scheduled_message(message_dict, channel_idx):
    target_channel = data_store.get()["channels"][channel_idx]
    target_channel["messages"].append(message_dict)
    
    send_later_list = target_channel["send_later"]
    for message_dict_idx, message in enumerate(send_later_list):
        if message["u_id"] == message_dict["u_id"]:
            send_later_list.pop(message_dict_idx)
    
    # alert when thread terminates
    print("Hakaaiiii")

def send_scheduled_message_dm(message_dict, dm_idx):
    target_channel = data_store.get()["dms"][dm_idx]
    target_channel["messages"].append(message_dict)
    
    send_later_list = target_channel["send_later"]
    for message_dict_idx, message in enumerate(send_later_list):
        if message["u_id"] == message_dict["u_id"]:
            send_later_list.pop(message_dict_idx)
    
    # alert when thread terminates
    print("Hakaaiiii")
###################### Function Implementation ###################


def message_sendlater_v1(token, channel_id, message, time_sent):
    '''
    message_sendlater_v1

    Sends a message from the authorised user to the channel specified by channel_id at a time in the future, given by time_sent.

    Arguments
    token (string) - This is the token of a user.
    channel_id (integer) - This is the channel id of the channel that the authorised user 
    would like to send the messages to.
    message (string) - The message string which will be sent to the channel message
    time_sent (integer) - This is the time when the message will be sent

    Exceptions:
    InputError - An input error is raised when the channel_id does not refer to a valid channel that the authorised user has joined 
    or the length of message is more than 1000 characters or less than 1 character. Also if the time_sent is a time in the past.

    AccessError - An access error is raised when the authorised user is either not a global owner or an owner member of the channel or the sender of the message.

    Return Value:
    This function returns message_id (integer), which is a completely unique ID.

    '''
    ### Double check order of exceptions

    if not check_if_token_exists(token):
        raise AccessError(description="Invalid Token!")
     
    # We can write a better helper function
    channels = data_store.get()["channels"]
    channel_idx = find_channel_index(channels, channel_id)
    if  channel_idx is None:
        raise InputError(description="Error occured, Invalid channel_id")

    target_channel = channels[channel_idx]
    u_id = decode_token(token)

    if not is_in_channel(u_id, target_channel):
        raise InputError(
            description="Error occured, User is not a member of channel they're trying to post to.")

    if not validate_message_dm(message):
        raise InputError(
            description="Error occured, Message length should be between 1 and 1000 characters.")


    waiting_time = time_sent - int(time())
    if waiting_time < 0:
        raise InputError(description="Error occured, The time entered has already passed!")


    # Create a send_later key if it does not exist
    if "send_later" not in target_channel:
        target_channel["send_later"] = []
    
    # Generating message dict and appending it to send_later list
    message_id =  data_store.get()['unique_message_id']
    message_dict =  {
            'message_id': message_id,
            'u_id': u_id,
            'message': message,
            'time_sent': time_sent
        }

    target_channel["send_later"].append(message_dict)

    sleeping_thread = threading.Timer(
        waiting_time, send_scheduled_message, args=(message_dict, channel_idx))
    sleeping_thread.start()


    return {"message_id" : message_id} 


def message_sendlaterdm_v1(token, dm_id, message, time_sent):
    '''
    message_sendlaterdm_v1

    Sends a message from the authorised user to the channel specified by dm_id at a time in the future, given by time_sent.

    Arguments
    token (string) - This is the token of a user.
    dm_id (integer) - This is the dm id of the dm that the authorised user 
    would like to send the messages to.
    message (string) - The message string which will be sent to the channel message
    time_sent (integer) - This is the time when the message will be sent

    Exceptions:
    InputError - An input error is raised when the dm_id does not refer to a valid dm that the authorised user has joined 
    or the length of message is more than 1000 characters or less than 1 character. Also if the time_sent is a time in the past.

    AccessError - An access error is raised when the authorised user is either not a global owner or an owner member of the dm or the sender of the message.

    Return Value:
    This function returns message_id (integer), which is a completely unique ID.

    '''
    if not check_if_token_exists(token):
        raise AccessError(description="Error occured, Invalid Token!")
     
    # We can write a better helper function
    dms = data_store.get()["dms"]
    dm_idx = find_dm_index(dms, dm_id)
    if dm_idx is None:
        raise InputError(description="Error occured, Invalid dm_id")

    target_dm = dms[dm_idx]
    u_id = decode_token(token)

    if not is_in_channel(u_id, target_dm):
        raise InputError(
            description="Error occured, User is not a member of dm they're trying to post to.")

    if not validate_message_dm(message):
        raise InputError(
            description="Error occured, Message length should be between 1 and 1000 characters.")


    waiting_time = time_sent - int(time())
    if waiting_time < 0:
        raise InputError(description="Error occured, The time entered has already passed!")


    # Create a send_later key if it does not exist
    if "send_later" not in target_dm:
        target_dm["send_later"] = []
    
    # Generating message dict and appending it to send_later list
    message_id =  data_store.get()['unique_message_id']
    message_dict =  {
            'message_id': message_id,
            'u_id': u_id,
            'message': message,
            'time_sent': time_sent
        }

    target_dm["send_later"].append(message_dict)

    sleeping_thread = threading.Timer(
        waiting_time, send_scheduled_message_dm, args=(message_dict, dm_idx))
    sleeping_thread.start()

    return {"message_id" : message_id}
############################### REACT ############################

########################## Helpers ##############################
 
def get_dm_channel_idx(channels, dms, message_id):

    for idx, channel in enumerate(channels):
        messages = channel["messages"]
        for msg_idx, message in enumerate(messages):
            if message_id == message["message_id"]:
                return {"idx" : idx, "msg_idx" : msg_idx,
                    "dm" : False, "channel": True}
    
    # if not channel_idx:
    for idx, dm in enumerate(dms):
        messages = dm["messages"]
        for msg_idx, message in enumerate(messages):
            if message_id == message["message_id"]:
                return {"idx" : idx, "msg_idx" : msg_idx,
                    "dm" : True, "channel": False}

    return {"idx" : None}


############################ Implementation #############################


def message_react_v1(token, message_id, react_id):
    '''
    message_react_v1

    Given a message_id, add a react_id to the particular section of the message.

    Arguments
    token (string) - This is the token of a user.
    message_id (integer) - This is the unique ID to identify which message will be reacted upon.
    react_id (integer) - The react_id will be the reaction that will appear in the frontend.

    Exceptions:
    InputError - An input error is raised when the message_id does not refer to a valid message within a channel/DM that the authorised user has joined
    or react_id is not valid, only react_id == 1 only exist for now (thumbs up), or there is already a react_id already present in the message.

    AccessError - An access error is raised when the authorised user is either not a global owner or an owner member of the channel or the sender of the message_id.

    Return Value:
    This function returns an empty dictionary.
    '''
    if not check_if_token_exists(token):
        raise AccessError(description="Error occured, Invalid Token!")
    u_id = decode_token(token)

    if react_id != 1:
        raise InputError(description="Error occured, Invalid react_id")

    channels = data_store.get()["channels"]
    dms = data_store.get()["dms"]
    result = get_dm_channel_idx(channels, dms, message_id)
    idx = result["idx"]
    if idx is None:
        raise InputError(description="Error occured, Invalid message id!")

    if result["dm"]:
        messages = dms[idx]["messages"]
    else:
        messages = channels[idx]["messages"]

    target_message = messages[result["msg_idx"]]
    if "reacts" in target_message and target_message["reacts"]:
        u_ids = target_message["reacts"][0]["u_ids"]
        if u_id in u_ids:
            raise InputError(description="Error occured, User already reacted to this message")
        else:
            u_ids.append(u_id)
            # target_message["reacts"][0]["is_this_user_reacted"] = True

    else:
        target_message['reacts'] = [
            {
                'react_id' : react_id,
                'u_ids' : [u_id]
            }
        ]
    print(data_store.get())

    # ================================================== NOTIFICATIONS INSERTION ==============================================================
    # Find if message is in channel or in dm
    is_channel = find_channeldm_from_message(message_id)['is_channel']
    is_dm = find_channeldm_from_message(message_id)['is_dm']

    # If in channel, find the relevant channel id and channel_name
    if is_channel:
        channel_id = find_channeldm_from_message(message_id)['id']
        dm_id = -1
        channeldm_name = [channel['channel_name'] for channel in channels if channel['channel_id'] == channel_id][0]

    # If in dm, find the relevant dm_id and dm_name    
    if is_dm:
        dm_id = find_channeldm_from_message(message_id)['id']
        channel_id = -1
        channeldm_name = [dm['dm_name'] for dm in dms if dm['dm_id'] == dm_id][0]

    # Find the person who originally sent the message that is being reacted to, i.e. the person to notify
    user_to_notify = find_message_sender(message_id,channel_id,dm_id)
    # Find handle of the user reacting to the message
    users = data_store.get()['users']
    u_id = decode_token(token)
    reactor_handle = [user['handle_str'] for user in users if user['u_id'] == u_id][0]
    # Generate notification message
    notification_message = '{} reacted to your message in {}'.format(reactor_handle,channeldm_name)
    notification = {
        'channel_id': channel_id,
        'dm_id': dm_id,
        'notification_message': notification_message,
    }

    # Append notification to list of notifications under the the person who originally sent the message
    user_listof_notifications = [user['notifications'] for user in users if user['u_id'] == user_to_notify][0]
    user_listof_notifications.append(notification)

    # ===============================================================================================================================

    return {}





def message_unreact_v1(token, message_id, react_id):
    '''
    message_unreact_v1

    Given a message_id, remove a react_id to the particular section of the message.

    Arguments
    token (string) - This is the token of a user.
    message_id (integer) - This is the unique ID to identify which message will be reacted upon.
    react_id (integer) - The react_id will be the reaction that will appear in the frontend.

    Exceptions:
    InputError - An input error is raised when the message_id does not refer to a valid message within a channel/DM that the authorised user has joined
    or react_id is not valid, only react_id == 1 only exist for now (thumbs up), or there is already a react_id already present in the message.

    AccessError - An access error is raised when the authorised user is either not a global owner or an owner member of the channel or the sender of the message_id.

    Return Value:
    This function returns an empty dictionary.
    '''
    if not check_if_token_exists(token):
        raise AccessError(description="Invalid Token!")
    u_id = decode_token(token)

    if react_id != 1:
        raise InputError(description="Invalid react_id")

    channels = data_store.get()["channels"]
    dms = data_store.get()["dms"]
    result = get_dm_channel_idx(channels, dms, message_id)
    idx = result["idx"]
    if idx is None:
        raise InputError(description="Invalid message id!")

    if result["dm"]:
        messages = data_store.get()["dms"][idx]["messages"]
    else:
        messages = channels[idx]["messages"]

    target_message = messages[result["msg_idx"]]
    if "reacts" in target_message and target_message["reacts"]:
        u_ids = target_message["reacts"][0]["u_ids"]
        print(f"###############  {u_ids}  ###################")
        if u_id in u_ids:
            u_ids.remove(u_id)
        #else:
        #    raise InputError(description="Error occured, User has not reacted to this message")

    print(data_store.get())
    return {}

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
