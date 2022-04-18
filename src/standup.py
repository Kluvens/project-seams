from src.data_store import data_store
from src.error import InputError, AccessError
from src.helpers import decode_token
from src.helpers import check_if_token_exists, find_channel, find_user
from src.message import message_send_v1
import time
from datetime import datetime, timedelta

def standup_start_v1(token, channel_id, length):

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
        raise AccessError ("channel_id is valid and the authorised user is not a member of the channel") 

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

    channel_id = int(channel_id)
    auth_user_id = int(decode_token(token))
    channel = find_channel(channel_id)

    if channel is None:
        raise InputError("channel_id does not refer to a valid channel")
    all_members_uids = [user['u_id'] for user in channel['all_members']]
    if not auth_user_id in all_members_uids:
        raise AccessError ("channel_id is valid and the authorised user is not a member of the channel") 

    if 'standup' in channel:
        if int(time.time()) > int(channel['standup']['time_finish']):
            if channel['standup']['is_active'] == True:
                channel['standup']['is_active'] = False
                if channel['standup']['message'] == '':
                    return {
                        'is_active': False,
                        'time_finish': None,
                    }
                message_send_v1(token, channel_id, channel['standup']['message'])
                return {
                    'is_active': False,
                    'time_finish': None,
                }
        return {
            'is_active': True,
            'time_finish': int(channel['standup']['time_finish']),
        }
    return {
        'is_active': False,
        'time_finish': None,
    }

def standup_send_v1(token, channel_id, message):

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
        raise AccessError ("channel_id is valid and the authorised user is not a member of the channel") 

    standup_message = channel["standup"]['message']
    user = find_user(auth_user_id)

    standup_message += user['name_first']+": "+message+"\n"

    channel["standup"]['message'] = standup_message
    return {}