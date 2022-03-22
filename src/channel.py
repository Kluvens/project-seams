from src.data_store import data_store
from src.error import AccessError, InputError

def channel_invite_v2(token, channel_id, u_id):

    ''' 
    channel_invite.py

    This function allows an authorized user to invite another user into a given channel.

    Arguments:
    auth_user_id (integer) - This is the user id of the user authorized to invite other users. 
    This means they are a member themselves, and/or are an owner.
    channel_id (integer) - This is the channel id of the channel that the authorized user 
    would like to invite the other user to.
    u_id (integer) - This is the user id of the user to be invited to the given channel.

    Exceptions:
    InputError - An input error is raised when the channel id or either user is invalid or 
    if the user already exists in the channel
    AccessError - An access error is raised when the authorizing user is not a global owner 
    or an existing member of the channel

    Return Value:
    This function does not return anything
    '''


    # Access user and channel lists 
    store = data_store.get()
    channels = store['channels']
    users = store['users']

    # Check u_id is valid, channel is valid, auth_user is a channel member and u_id is not 
    # already a member of channel
    channel_to_join = None
    u_id_valid = False
    auth_user_authorized = False
    u_id_member = False

    # Convert token to auth_user_id TO DO
    auth_user_id = token

    # Check for valid u_id
    u_id_list = [user['u_id']for user in users]
    if u_id in u_id_list:
        u_id_valid = True
    
    # Check for valid channel
    for channel in channels:
        if channel['channel_id'] == channel_id:
            channel_to_join = channel

            # If channel is valid, check if auth_user and u_id are in it
            channel_members = channel['all_members']
            for member in channel_members:
                if member['u_id'] == auth_user_id:
                    auth_user_authorized = True 
                if member['u_id'] == u_id:
                    u_id_member = True

    # Input errors 
    if not u_id_valid:
        raise InputError ("ERROR: The user you are trying to add does not exist.")

    if channel_to_join == None:
        raise InputError ("ERROR: This channel does not exist.")

    if u_id_member == True:
        raise InputError ("ERROR: The user you are trying to add already exists in the channel")

    # Access errors
    if auth_user_authorized == False:
        raise AccessError ("ERROR: You are not authorized to invite users to this channel.")

    # If all conditions are met, append user to members list for given channel
    if u_id_valid == True and channel_to_join != None and u_id_member == False and auth_user_authorized == True:
        member_list = channel_to_join['all_members']
        new_member = {'u_id': u_id}
        member_list.append(new_member)

    return {}

def find_channel_index(channel_id):
    data = data_store.get()

    i = 0
    for channel in data["channels"]:
        if channel["channel_id"] == channel_id:
            return i
        else:
            i += 1
    return None


def is_in_channel(auth_user_id, right_channel):
    for member in right_channel["all_members"]:
        if auth_user_id == member["u_id"]:
            return True

    return False

def channel_details_v2(auth_user_id, channel_id):
    '''
    This function is given by authorised user id and channel id, returning name, 
    whether the channel is public, a list of owner members and a list of all members.

    Arguments:
    auth_user_id(integer) - This is the user id of the user authorized to create the channel.
    channel_id(integer) - this is the identifier of the channel

    Exceptions:
    InputError - when the channel_id does not refer to a valid channel
    AccessError - channel_id is valid but the authorised user is not a member of the channel

    Return Value:
    the function will return a dictionary containing the name of the channel,
    whether the channel is public, the list of all owner members and a list of all members 
    of the channel

    '''

    data = data_store.get()
    # users = data["users"]

    right_channel_index = find_channel_index(channel_id)

    # error
    if right_channel_index is None:
        raise InputError("channel_id does not refer to a valid channel")

    right_channel = data["channels"][right_channel_index]

    if not is_in_channel(auth_user_id, right_channel):
        raise AccessError("channel_id is valid and the authorised user is not a member of the channel")

    return {
        'name': right_channel["name"],
        'is_public': right_channel["is_public"],
        'owner_members': right_channel['owner_members'],
        'all_members': right_channel['all_members'],
    }


def channel_messages_v2(auth_user_id, channel_id, start):
    '''
    channel_messages_v1

    This function outputs upto 50 messages between index start and start + 50.

    Arguments
    auth_user_id (integer) - This is the user id of an authorised user who is either an owner 
    or member of the channel.
    channel_id (integer) - This is the channel id of the channel that the authorised user 
    would like to see the messages of.
    start (integer) - The start index of the messages array which will be returned.

    Exceptions:
    InputError - An input error is raised when the channel id or either the start is greater 
    than the total number of messages in the channel
    AccessError - An access error is raised when the authorised user is not a global owner or an 
    existing member of the channel

    Return Value:
    This function returns the messages array from the channel, the start index and the end index.
    
    '''
    data = data_store.get()
    assert "channels" in data

    # Check whether channel_id exist in the database
    channel_exist = False
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            channel_exist = True
    if not channel_exist:
        raise InputError("Error occurred channel_id is not in database")
    
    # Check user is a member in channel_id
    authorised_user = False
    for channel in data['channels']:
        for member in channel['all_members']:
            if member['u_id'] == auth_user_id:
                authorised_user = True
    if not authorised_user:
        raise AccessError("Error occurred authorised user is not a member of channel_id")

    # Retrieves all messages and also number of messages
    num_messages = 0
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            if 'messages' in data['channels'][channel_id]:
                found_messages = channel['messages']
                num_messages = len(found_messages)
            else:
                data['channels'][channel_id]['messages'] = []
    
    if start > num_messages:
        raise InputError("Error occurred start value is greater than the number of messages")

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

def channel_join_v2(auth_user_id, channel_id):
    '''
    channel_join.py

    This function allows given user to join a given channel.

    Arguments:
    auth_user_id (integer) - This is the user id of the user that would like to join the channel.
    channel_id (integer) - This is the channel id of the channel that the user would like to join.

    Exceptions:
    InputError - An input error is raised when the channel id is invalid 
    (i.e. the channel doesn't exist) or if the user already exists in the channel
    AccessError - An access error is raised when a non authorized user tries to join a private 
    channel (ie. not a global owner and not already in the channel)

    Return Value:
    This function does not return anything
    '''

    # Access channel and user lists
    store = data_store.get()
    channels = store['channels']
    users = store['users']
    
    #Check if channel exists, is public, is global owner, is already a member 
    channel_access = False 
    user_in_channel = False
    channel_to_join = None

    # Check channel exists
    channel_list = [channel for channel in channels if channel['channel_id'] == channel_id]
        
    # If channel exists, save correct channel
    if channel_list != []:
        channel_to_join = channel_list[0]
        # Check if user exists in channel already
        users1 = channel_to_join['all_members']
        u_id_list = [user['u_id'] for user in users1]
        if auth_user_id in u_id_list:
            user_in_channel = True
        # Check if the channel is public 
        if channel_to_join['is_public']:
            channel_access = True 

    # Check if user is a global owner 
    if auth_user_id == 0:
        channel_access = True   

    # Input error 
    if channel_list == []:
        raise InputError ("ERROR: Channel does not exist")

    if user_in_channel:
        raise InputError ("ERROR: You have already joined this channel")         

    # Access error 
    if not channel_access:
        raise AccessError ("ERROR: You do not have access to this private channel")
        
    # Append member if all conditions met
    if channel_to_join != None and channel_access == True and user_in_channel == False:
        member_list = channel_to_join['all_members']
        new_member = {'u_id':auth_user_id}
        member_list.append(new_member)
    return {}
