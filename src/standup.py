from src.data_store import data_store
from src.error import InputError, AccessError
from src.helpers import decode_token
from src.helpers import check_if_token_exists, find_channel, find_user
from src.message import message_send_v1
import time
from datetime import datetime, timedelta

def standup_start_v1(token, channel_id, length):
    '''
    For a given channel, start the standup period whereby for the next 
    "length" seconds if someone calls "standup/send" with a message, 
    it is buffered during the X second window then at the end of the 
    X second window a message will be added to the message queue in the 
    channel from the user who started the standup.

    Arguments:
        <token> (str) 
        <channel_id> (int)
        <length> (int)

    Exceptions:
        AccessError -   Occurs when invalid token input
        AccessError -   channel_id is valid and the authorised user 
                        is not a member of the channel
        InputError  -   channel_id does not refer to a valid channel
        InputError  -   length is a negative integer
        InputError  -   an active standup is currently running in the 
                        channel

    Return Value:
        Returns {time_finish} where time_finish is the unix time of
        when the standup ends
    '''
    length = int(length)
    channel_id = int(channel_id)
    auth_user_id = int(decode_token(token))
    channel = find_channel(channel_id)

    if channel is None:
        raise InputError("channel_id does not refer to a valid channel")
    if length < 0:
        raise InputError("length is a negative integer")
    if 'standup' in channel and channel['standup']['is_active'] == True:
        raise InputError("an active standup is currently running in the channel")
    all_members_uids = [user['u_id'] for user in channel['all_members']]
    if not auth_user_id in all_members_uids:
        raise AccessError("channel_id is valid and the authorised user is not a member of the channel") 
    if not check_if_token_exists(token):
        raise AccessError(description="Invalid token")

    time_finish = datetime.now() + timedelta(seconds=length)
    unix_time_finish = int(time_finish.timestamp())
    standup_dict = {
        'is_active': True,
        'time_finish': unix_time_finish,
        'u_id': auth_user_id,
        'message': '',
    }

    channel["standup"] = standup_dict

    return {
        'time_finish': unix_time_finish
    }

def standup_active_v1(token, channel_id):
    '''
    For a given channel, return whether a standup is active in it, 
    and what time the standup finishes. If no standup is active, 
    then time_finish returns None.

    Arguments:
        <token> (str) 
        <channel_id> (int)

    Exceptions:
        AccessError -   Occurs when invalid token input
        AccessError -   channel_id is valid and the authorised user 
                        is not a member of the channel
        InputError  -   channel_id does not refer to a valid channel

    Return Value:
        Returns {is_active, time_finish} where time_finish is 
        the unix time of when the standup ends and is_active
        is a boolean value of whether the standup is active
    '''
    channel_id = int(channel_id)
    auth_user_id = int(decode_token(token))
    channel = find_channel(channel_id)

    if channel is None:
        raise InputError("channel_id does not refer to a valid channel")
    all_members_uids = [user['u_id'] for user in channel['all_members']]
    if not auth_user_id in all_members_uids:
        raise AccessError("channel_id is valid and the authorised user is not a member of the channel") 
    if not check_if_token_exists(token):
        raise AccessError(description="Invalid token")

    if 'standup' in channel:
        # if current time > finish time
        if int(time.time()) > int(channel['standup']['time_finish']):
            # when standup_active is called the first time after standup finishes
            if channel['standup']['is_active'] == True:
                channel['standup']['is_active'] = False
                # if message is empty
                if channel['standup']['message'] == '':
                    return {
                        'is_active': False,
                        'time_finish': None,
                    }
                # if message is not empty
                message_send_v1(token, channel_id, channel['standup']['message'])
                return {
                    'is_active': False,
                    'time_finish': None,
                }
            # when standup_active has been called more than once after standup has finished
            channel['standup']['is_active'] = False
            return {
                'is_active': False,
                'time_finish': None,
            }
        # if current time < finish time
        return {
            'is_active': True,
            'time_finish': int(channel['standup']['time_finish']),
        }
    # if standup not in channel
    return {
        'is_active': False,
        'time_finish': None,
    }

def standup_send_v1(token, channel_id, message):
    '''
    Sending a message to get buffered in the standup queue, 
    assuming a standup is currently active.

    Arguments:
        <token> (str) 
        <channel_id> (int)
        <message> (str)

    Exceptions:
        AccessError -   Occurs when invalid token input
        AccessError -   channel_id is valid and the authorised user 
                        is not a member of the channel
        InputError  -   channel_id does not refer to a valid channel
        InputError  -   length of message is over 1000 characters
        InputError  -   an active standup is not currently running 
                        in the channel
    Return Value:
        Returns {}
    '''
    auth_user_id = int(decode_token(token))
    channel_id = int(channel_id)
    channel = find_channel(channel_id)

    if channel is None:
        raise InputError("channel_id does not refer to a valid channel")
    if len(message) > 1000:
        raise InputError(description="length of message is over 1000 characters")
    if 'standup' not in channel or channel['standup']['is_active'] == False:
        raise InputError("an active standup is not currently running in the channel")
    all_members_uids = [user['u_id'] for user in channel['all_members']]
    if not auth_user_id in all_members_uids:
        raise AccessError("channel_id is valid and the authorised user is not a member of the channel") 
    if not check_if_token_exists(token):
        raise AccessError(description="Invalid token")

    standup_message = channel["standup"]['message']
    user = find_user(auth_user_id)

    standup_message += user['name_first']+": "+message+"\n"

    channel["standup"]['message'] = standup_message
    return {}