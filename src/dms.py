from src.data_store import data_store
from src.error import InputError, AccessError
from src.helpers import decode_token
from src.helpers import check_if_token_exists
from src.helper import get_user_idx
from src.helpers import generate_dm_handle
from src.helpers import find_dm_index
from src.helpers import is_in_dm
from src.helpers import check_u_id_exists
from src.helpers import check_duplicate_u_ids
from typing import List, Dict, Any, Optional
from time import time

def dm_list_v1(token: str) -> Dict:
    '''
    Returns a list of of dictionaries in {dms}, 
    where the list is made up of dictionairies 
    containing types {dm_id, name} if it corresponds 
    to the given user id. The list returned
    are DMs the user is a member of. 
    The user_id is found by decoding the token.

    Arguments:
        <token> (str) 

    Exceptions:
        AccessError -   Occurs when invalid token input

    Return Value:
        Returns {dms} which contains a list of dictionaries 
        {dm_id, name} where name is str
        and dm_id is int
    '''

    # initialise datastore and dicts
    data = data_store.get()
    dms_list = data['dms']
    dms_dict: Dict = {'dms' : []}
    
    # if token doesnt exist return AccessError
    if not check_if_token_exists(token):
        raise AccessError(description="Invalid token")
    
    u_id = int(decode_token(token))

    # loop through data_store and if u_id is in dm
    # add dms and names to dict
    for dm in dms_list:
        for members in dm['all_members']:
            if u_id == members['u_id']:
                dm_id = dm['dm_id']
                name = dm['name']
                dms_dict['dms'].append({'dm_id' : dm_id, 'name' : name})

    return dms_dict


def dm_details_v1(token: str, dm_id: int) -> Dict:
    '''
    Given { token, dm_id } ,
    the DM is found if it exists and { name, members } is returned.
    name is the handle generated by dm_create_v1 
    and members generates the following details,
    -   email
    -   handle_str
    -   name_first
    -   name_last
    -   u_id

    Arguments:
        <token> (str) - is generated by auth_register_v1 
        when a user is first registered
        <dm_id> (int) - is generated by dm_create_v1 when a DM is made

    Exceptions:
        AccessError -   Occurs when invalid token or when dm_id 
        is valid however the authorised user is not a member of the DM
        InputError  -   Occurs when dm_id does not refer to a valid DM 

    Return Value:
        Returns {name, members} which includes the basic details of 
        the DM where name is str and
        members is a list of dictionaries
    '''

    data = data_store.get()
    dm_id = int(dm_id)
    users = data["users"]
    dms = data["dms"]

    if not check_if_token_exists(token):
        raise AccessError(description="Invalid token")
    
    auth_user_id = int(decode_token(token))

    right_dm_index = find_dm_index(dms, dm_id)

    if right_dm_index is None:
        raise InputError(description="dm_id does not refer to a valid dm")

    right_dm = data["dms"][right_dm_index]

    if not is_in_dm(auth_user_id, right_dm):
        raise AccessError(description="dm_id is valid and the authorised user is not a member of the dm")

    right_dm_all_members = [
        {
            'u_id': users[member['u_id']]['u_id'],
            'email': users[member['u_id']]['email'],
            'name_first': users[member['u_id']]['name_first'],
            'name_last': users[member['u_id']]['name_last'],
            'handle_str': users[member['u_id']]['handle_str'],
        }
    for member in right_dm['all_members']]

    return {
        'name': right_dm["name"],
        'members': right_dm_all_members,
    }

def dm_create_v1(token: str, u_ids: List[int]) -> Dict[str, int]:
    '''
    Given token and a list of u_ids, we should generate a direct message for the auth user and u_ids to be invited

    Arguments:
        <token> (str) - is generated by auth_register_v1 
        when a user is first registered
        <u_ids> (list) - this is a list of u_ids which represents the users to be joined the dm

    Exceptions:
        InputError  -   any u_id in u_ids does not refer to a valid user
        InputError  -   there are duplicate 'u_id's in u_ids

    Return Value:
        Returns { dm_id } where dm_id is the unique identifier of the created dm
    '''
    # if token doesnt exist return AccessErr
    if not check_if_token_exists(token):
        raise AccessError(description="Invalid Token!")

    owner_uid = decode_token(token)

 
    if check_duplicate_u_ids(u_ids):
        raise InputError(description="Duplicate u_ids")

    data = data_store.get() 
    users = data["users"]

    for u_id in u_ids:
        if not check_u_id_exists(users, u_id):
            raise InputError(description="Invalid u_id in u_ids")
    
    handles = generate_dm_handle(owner_uid, u_ids, users)
    handles = sorted(handles)
    name = ", ".join(handles)
    
    host_info = data["users"][owner_uid]
    host_info_list = [{
        'u_id': host_info["u_id"],
    }]
    owner_members_list = host_info_list.copy()
    
    members_list = []
    members_list.append({'u_id': host_info["u_id"]})
    for uid in u_ids:
        members = data["users"][uid]
        members_list.append({'u_id': members['u_id']})
    
    dm_id = len(data['dms'])
    time_stamp = int(time())

    data['dms'].append({
        "dm_id" : dm_id,
        "name" : name,
        'time_stamp': time_stamp,
        'owner_members': owner_members_list,
        'all_members': members_list,
        'messages': []
    })
    
    data_store.set(data)

    return {
        'dm_id': dm_id
    }


def dm_leave_v1(token: str, dm_id: int) -> Dict:
    '''
    This function allows the user to leave a DM.

    Arguments: 
    - token (string) - This is the authentication token of the authorized user,
    who must be a member of the DM.
    - dm_id (integer) - This is the dm id of the DM that the authorized 
    user would like to leave.

    Exceptions:
    InputError - An input error is raised when the dm_id does not 
    refer to a valid DM.

    AccessError - An access error is raised when the authorized user 
    is no longer in the DM.

    Exception for all functions:
    AccessError - When an invalid token is passed into the function.

    Return Value:
    This function does not return anything.
    '''

    dms = data_store.get()['dms']
    users = data_store.get()['users']
    dm_id = int(dm_id)

    # Check token is valid and u_id exists
    if not check_if_token_exists(token):
        raise AccessError(description="Invalid token")
    else:
        u_id = int(decode_token(token))

    u_ids = [user['u_id'] for user in users]
    if u_id not in u_ids:
        raise InputError(description="ERROR: User id does not exist") 

    # Check dm_id is valid 
    dm_ids = [dm['dm_id'] for dm in dms]
    if dm_id not in dm_ids:
        raise InputError(description="ERROR: DM id does not exist")

    # find correct channel
    dm_index = find_dm_index(dms, dm_id)
    correct_dm = dms[dm_index]
    all_members_uids = [user['u_id'] for user in correct_dm['all_members']]
    if u_id not in all_members_uids:
        raise AccessError (description="ERROR: User is not in DM")

    for member in dms[dm_index]['all_members']:
        if member['u_id'] == u_id:
            dms[dm_index]['all_members'].remove({'u_id': u_id})

    return{}

def dm_remove_v1(token: str, dm_id: int) -> Dict:
    '''
    This function allows for the owner of the DM to remove the DM, 
    such that all members of the DM are no longer in the DM.

    Arguments: 
     - token (string) - This is the authentication token of the 
    authorized user, who must be a member of the DM and the owner of it.
    - dm_id (integer) - This is the dm id of the DM that the authorized 
    user would like to remove.

    Exceptions:
    InputError - An input error is raised when the dm_id does 
    not refer to a valid DM.
    AccessError - An access error is raised when the authorized 
    user is not the owner of the DM or the authorized user is no longer in the DM

    Common error:
    AccessError - When an invalid token is passed into the function.

    Return Value:
    This function does not return anything.
    '''

    dms = data_store.get()['dms']
    users = data_store.get()['users']

    # Check token is valid and u_id exists
    token_valid = False
    user_exists = False
    if not check_if_token_exists(token):
        raise AccessError(description="Invalid token")
    else:
        u_id = int(decode_token(token))
        token_valid = True

    u_ids = [user['u_id'] for user in users]
    if u_id in u_ids:
        user_exists = True
    else: 
        raise InputError(description="ERROR: User id does not exist")

    # Check dm_id is valid and exists
    dm_id_valid = False
    dm_ids = [dm['dm_id'] for dm in dms]
    if dm_id in dm_ids:
        dm_id_valid = True
    else:
        raise InputError(description="ERROR: Dm id does not exist")

    # Check token is from owner of dm_id and is still in the dm
    user_is_owner = False
    idx = find_dm_index(dms, dm_id)
    all_members = dms[idx]['all_members']
    owner_u_id = get_owner_idx(all_members, u_id)

    if u_id == all_members[owner_u_id]['u_id']:
        user_is_owner = True
    else:
        raise AccessError (
            description="ERROR: User is not the owner of this Dm")

    user_in_dm = False
    users_dms_return: Dict = dm_list_v1(token)
    users_dms_list: List = users_dms_return['dms']
    final_dms_list: List = [member['dm_id'] for member in users_dms_list]

    if dm_id in final_dms_list:
        user_in_dm = True
    else:
        raise AccessError (description="ERROR: User is not in Dm")
    
    # If all conditions followed, delete dm from dms list in data struct
    if token_valid and user_exists and dm_id_valid and user_is_owner and user_in_dm:
        del dms[idx]

    return {}

############## Helper Funciton ######################
def get_owner_idx(members, u_id):
    return 0
