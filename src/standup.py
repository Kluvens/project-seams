from src.data_store import data_store
from src.error import InputError, AccessError
from src.helpers import decode_token
from src.helpers import check_if_token_exists
from src.message import message_send_v1
import time
from datetime import datetime, timedelta

def find_channel(channel_id):
    data = data_store.get()
    for channel in data['channels']:
        if int(channel_id) == channel['channel_id']:
            return channel
    return None
def find_user(u_id):
    data = data_store.get()
    for user in data['users']:
        if int(u_id) == user['u_id']:
            return user
    return None

def standup_start_v1(token, channel_id, length):

    length = int(length)
    channel_id = int(channel_id)
    channel = find_channel(channel_id)
    auth_user_id = int(decode_token(token))

    if channel is None:
        raise InputError("Channel doesn't exist!")

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
    channel = find_channel(channel_id)
    if channel is None:
        raise InputError("Channel doesn't exist!")
    if check_if_token_exists(token) == False:
        raise AccessError(description="Error occured, invalid token'")

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
            channel['standup']['is_active'] = False
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

    channel_id = int(channel_id)
    channel = find_channel(channel_id)
    if channel is None:
        raise InputError("Channel doesn't exist!")
    auth_user_id = int(decode_token(token))
    standup_message = channel["standup"]['message']
    user = find_user(auth_user_id)

    standup_message += user['name_first']+": "+message+"\n"

    channel["standup"]['message'] = standup_message
    return {}