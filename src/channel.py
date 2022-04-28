from src.data_store import data_store
from src.error import AccessError, InputError
from src.helpers import decode_token
from src.helpers import check_if_token_exists
from src.helper import find_channel_index, is_in_channel
from src.helper import  count_number_owner, is_in_channel_owner
from src.helper import global_owner_check, get_user_idx
from src.helpers import decode_token, check_if_token_exists
from src.helper import channel_details_members_return


def channel_invite_v2(token, channel_id, u_id):
    '''
    This function allows an authorized user to invite another 
    user into a given channel.

    Arguments:
    - token (string) - This is the authentication token of the 
    authorized user. 
    This means they are a member themselves, and/or are an owner.
    - channel_id (integer) - This is the channel id of the channel 
    that the authorized user would like to invite the other user to.
     - u_id (integer) - This is the user id of the user to be
    invited to the given channel.

    Exceptions:
    InputError - An input error is raised when the channel id or 
    either user is invalid or if the user already exists in the channel
    AccessError - An access error is raised when the authorizing user 
    is not a global owner or an existing member of the channel

    Common error:
    AccessError - When an invalid token is passed into the function

    Return Value:
    This function does not return anything
    '''

    # Access user and channel lists 
    store = data_store.get()
    channels = store['channels']
    users = store['users']

    channel_id = int(channel_id)
    u_id = int(u_id)

    # Check if token exists
    token_exists = check_if_token_exists(token)

    # Convert token to u_id
    if token_exists:
        u_id2 = decode_token(token)
    else:
        raise AccessError (description="ERROR: Token does not exist")
      
    # Check u_id is valid, channel is valid, auth_user is a channel member and u_id is not already a member of channel
    channel_to_join = None
    u_id_valid = False
    auth_user_authorized = False
    u_id_member = False

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
                if member['u_id'] == u_id2:
                    auth_user_authorized = True 
                if member['u_id'] == u_id:
                    u_id_member = True

    # Input errors 
    if not u_id_valid:
        raise InputError (
            description="ERROR: The user you are trying to add does not exist.")

    if channel_to_join == None:
        raise InputError (
            description="ERROR: This channel does not exist.")

    if u_id_member == True:
        raise InputError (
            description="ERROR: The user you are trying to add already exists in the channel")

    # Access errors
    if auth_user_authorized == False:
        raise AccessError (
            description="ERROR: You are not authorized to invite users to this channel.")

    # If all conditions are met, append user to members list for given channel
    if u_id_valid and channel_to_join != None and not u_id_member and auth_user_authorized and token_exists:
        member_list = channel_to_join['all_members']
        new_member = {'u_id': u_id}
        member_list.append(new_member)

    return {}

def channel_details_v2(token, channel_id):
    '''
    This function is given by token which refers to a 
    user and channel id, returning name, 
    whether the channel is public, a list of owner members 
    and a list of all members.

    Arguments:
    token(string) - The token refers to the authorised user 
    who is a member of the channel
    channel_id(integer) - this is the identifier of the channel

    Exceptions:
    InputError - when the channel_id does not refer to a valid channel
    AccessError - channel_id is valid but the authorised user
    is not a member of the channel
    AccessError - When the token does not refer to a valid user

    Return Value:
    the function will return a dictionary containing
    the name of the channel,
    whether the channel is public, the list of all
    owner members and a list of all members 
    of the channel.

    '''

    data = data_store.get()

    channel_id = int(channel_id)

    users = data["users"]
    channels = data["channels"]

    if not check_if_token_exists(token):
        raise AccessError(description="Invalid token")
    
    auth_user_id = int(decode_token(token))

    right_channel_index = find_channel_index(channels, channel_id)

    # error
    if right_channel_index is None:
        raise InputError(description="channel_id does not refer to a valid channel")

    right_channel = data["channels"][right_channel_index]

    if not is_in_channel(auth_user_id, right_channel):
        raise AccessError(description="channel_id is valid and the authorised user is not a member of the channel")

    # get the list of all owner members in a channel
    right_channel_owner_members = [channel_details_members_return(users, member) for member in right_channel['owner_members']]

    # get the list of all members in a channel
    right_channel_all_members = [channel_details_members_return(users, member) for member in right_channel['all_members']]

    return {
        'name': right_channel["name"],
        'is_public': right_channel["is_public"],
        'owner_members': right_channel_owner_members,
        'all_members': right_channel_all_members,
    }


def channel_messages_v2(token, channel_id, start):
    '''
    channel_messages_v2

    This function outputs upto 50 messages in channel_id between index start and start + 50.

    Arguments
    token (string) - This is the token of a user.
    channel_id (integer) - This is the channel id of the channel that the authorised user 
    would like to see the messages of.
    start (integer) - The start index of the messages array which will be returned.

    Exceptions:
    InputError - An input error is raised when the channel id is not valid or either the start is greater 
    than the total number of messages in the channel
    AccessError - An access error is raised when the authorised user is not an owner
    or an existing member of the channel

    Return Value:
    This function returns the messages array from the channel, the start index and the end index.
    '''
    channel_id = int(channel_id)
    start = int(start)
    data = data_store.get()
    assert "channels" in data
    # assert "token" in data

    # Check if token is valid using helper
    if check_if_token_exists(token) == False:
        raise AccessError("Error occured, invalid token'")

    # Check whether channel_id exist in the database
    channel_exist = False
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            channel_exist = True
    if not channel_exist:
        raise InputError("Error occurred channel_id is not in database")
    
    # Check user is a member in channel_id
    auth_user_id = int(decode_token(token))

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
            # else:
            #     data['channels'][channel_id]['messages'] = []
    
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
            'reacts': found_messages[index].get('reacts'),
            'is_pinned': found_messages[index].get('is_pinned'),
        })
        
        last_message = message_array[-1]
        if last_message['reacts']:
            if auth_user_id in last_message['reacts'][0]["u_ids"]:
                last_message['reacts'][0]["is_this_user_reacted"] = True
            else:
                last_message['reacts'][0]["is_this_user_reacted"] = False
    
    if num < 50:
        end = -1
    message_array.reverse()
    return {
        'messages': message_array,
        'start': start,
        'end': end,
    }

def channel_join_v2(token, channel_id):
    '''

    This function allows given user to join a given channel.

    Arguments:
    - token(string) - This is the authentication token of 
    the authorized user
    - channel_id (integer) - This is the channel id of the 
    - channel that the user would like to join.

    Exceptions:
    - InputError - An input error is raised when the channel id is 
    invalid (i.e. the channel doesn't exist) or if the user 
    already exists in the channel

    - AccessError - An access error is raised when a non
    authotries to join a private 
    channel (ie. not a global owner and not alreadrized user y in the 
    channel)

    Common error:
    AccessError - When an invalid token is passed into the function

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
    user_exists = False

    # Check token exists 
    token_exists = check_if_token_exists(token)

    # Convert token to u_id
    if not token_exists:
        raise AccessError(description="Invalid token")
    
    u_id = int(decode_token(token))

    # Check user exists 
    true_user = [user['u_id'] for user in users]
    if u_id in true_user:
        user_exists = True

    # Check channel exists
    channel_list = [channel for channel in channels if channel['channel_id'] == channel_id]
        
    # If channel exists, save correct channel
    if channel_list != []:
        channel_to_join = channel_list[0]
        # Check if user exists in channel already
        users1 = channel_to_join['all_members']
        u_id_list = [user['u_id'] for user in users1]
        if u_id in u_id_list:
            user_in_channel = True
        # Check if the channel is public 
        if channel_to_join['is_public']:
            channel_access = True  

    # Input error 
    if channel_list == []:
        raise InputError ("ERROR: Channel does not exist")

    if user_in_channel:
        raise InputError ("ERROR: You have already joined this channel")       

    if not user_exists:
        raise InputError ("ERROR: User does not exist")  

    # Access error 
    if not channel_access and not global_owner_check(u_id):
        raise AccessError ("ERROR: You do not have access to this private channel")
        
    # Append member if all conditions met
    if channel_to_join != None and (channel_access or global_owner_check(u_id)) and not user_in_channel and token_exists and user_exists:
        member_list = channel_to_join['all_members']
        new_member = {'u_id':u_id}
        member_list.append(new_member)

    data_store.set(store)
    return {}


def channel_addowner_v1(token, channel_id, u_id):
    '''
    This function is given by authorised user, channel id and user id, 
    make the user to become one of the owner members in the given channel

    Arguments:
    - token(string) - This is a token for a user, with the token we can decode and get the 
    authorised user id
    - channel_id(integer) - this is the identifier of the channel
    - u_id(integer) - this is the identifier of the person to be assigned 
    as the owner of the channel

    Exceptions:
    InputError - channel_id does not refer to a valid channel
    InputError - u_id does not refer to a valid user
    InputError - u_id refers to a user who is not a member of the channel
    InputError - u_id refers to a user who is already an owner of the channel
    AccessError - channel_id is valid and the authorised user does 
    not have owner permissions in the channel
    AccessError - when the token given does not refer to a valid user

    Return Value:
    the function will not return values

    '''

    data = data = data_store.get()
    channels = data['channels']
    users = data['users']

    if not check_if_token_exists(token):
        raise AccessError(description="Invalid token")
    auth_user_id = int(decode_token(token))

    channel_id = int(channel_id)
    u_id = int(u_id)

    right_channel_index = find_channel_index(channels, channel_id)
    # error
    if right_channel_index is None:
        raise InputError(description="channel_id does not refer to a valid channel")
    right_channel = channels[right_channel_index]

    if not is_in_channel(auth_user_id, right_channel):
        raise AccessError(description="auth user not in channel")
    
    if not global_owner_check(auth_user_id) and not is_in_channel_owner(auth_user_id, right_channel):
        raise AccessError(description="channel_id is valid and the authorised user does not have owner permissions in the channel")  

    right_user_index = get_user_idx(users, auth_user_id)
    # error
    if right_user_index is None:
        raise InputError(description="u_id does not refer to a valid user")

    if not is_in_channel(u_id, right_channel):
        raise InputError(description="u_id refers to a user who is not a member of the channel")

    if is_in_channel_owner(u_id, right_channel):
        raise InputError(description="u_id refers to a user who is already an owner of the channel")

    right_channel["owner_members"].append(
        {
            'u_id': u_id,
        }
    )

    data_store.set(data)

    return {}


def channel_removeowner_v1(token, channel_id, u_id):
    '''
    This function is given by authorised user, channel id and user id, 
    make the user to become one of the owner members in the given channel

    Arguments:
    token(string) - This is a token for a user, 
    with the token we can decode and get the authorised user id
    channel_id(integer) - this is the identifier of the channel
    u_id(integer) - this is the identifier of the person to be 
    removed as the owner of the channel

    Exceptions:
    InputError - channel_id does not refer to a valid channel
    InputError - u_id does not refer to a valid user
    InputError - u_id refers to a user who is not an owner of the channel
    InputError - u_id refers to a user who is currently the 
    only owner of the channel
    AccessError - channel_id is valid and the authorised
    user does not have owner permissions in the channel
    AccessError - when the token given does not refer to a valid user

    Return Value:
    the function will not return values

    '''
    data = data = data_store.get()
    channels = data['channels']
    users = data['users']

    if not check_if_token_exists(token):
        raise AccessError(description="Invalid token")
    auth_user_id = int(decode_token(token))

    channel_id = int(channel_id)
    u_id = int(u_id)

    right_channel_index = find_channel_index(channels, channel_id)
    # error
    if right_channel_index is None:
        raise InputError(description="channel_id does not refer to a valid channel")
    right_channel = channels[right_channel_index]

    if not is_in_channel(auth_user_id, right_channel):
        raise AccessError(description="auth user not in channel")

    right_user_index = get_user_idx(users, u_id)
    # error
    if right_user_index is None:
        raise InputError(description="u_id does not refer to a valid user")

    if not is_in_channel_owner(u_id, right_channel):
        raise InputError(description="u_id refers to a user who is not an owner of the channel")

    if count_number_owner(right_channel) == 1:
        raise InputError(description="u_id refers to a user who is currently the only owner of the channel")

    if not global_owner_check(auth_user_id) and not is_in_channel_owner(auth_user_id, right_channel):
        raise AccessError(description="channel_id is valid and the authorised user does not have owner permissions in the channel")  

    right_channel["owner_members"].remove(
        {
            'u_id': u_id,
        }
    )

    data_store.set(data)

    return {}

def channel_leave_v1(token, channel_id):
    '''
    channel_leave_v1.py

    This function allows a member that is part of a channel, to leave that channel.

    Arguments: 
    Token (string) - This is the authentication token of the authorized user, who must be a member of the channel.
    channel_id (integer) - This is the channel id of the channel that the authorized user would like to leave.

    Exceptions:
    InputError - An input error is raised when the channel id does not refer to a valid channel
    AccessError - An access error is raised when the given user is not a member of the channel 

    Common error:
    AccessError - When an invalid token is passed into the function

    Return Value:
    This function does not return anything
    '''
    channels = data_store.get()['channels']
    users = data_store.get()['users']
    channel_id = int(channel_id)

    # Check token is valid and u_id exists

    if not check_if_token_exists(token):
        raise AccessError(description="Invalid token")
    else:
        u_id = int(decode_token(token))

    u_ids = [user['u_id'] for user in users]
    if not u_id in u_ids:
        raise InputError("ERROR: User id does not exist") 

    # Check channel_id is valid 
    channel_ids = [channel['channel_id'] for channel in channels]
    if not channel_id in channel_ids:
        raise InputError("ERROR: Channel id does not exist")

    # Check authorized user is part of channel
    # find correct channel
    channel_index = find_channel_index(channels, channel_id)
    correct_channel = channels[channel_index]
    all_members_uids = [user['u_id'] for user in correct_channel['all_members']]
    if not u_id in all_members_uids:
        raise AccessError ("ERROR: User is not in channel")

    for member in channels[channel_index]['all_members']:
        if member['u_id'] == u_id:
            channels[channel_index]['all_members'].remove({'u_id': u_id})

    for member in channels[channel_index]['owner_members']:
        if member['u_id'] == u_id:
            channels[channel_index]['owner_members'].remove({'u_id': u_id})

    return {}
