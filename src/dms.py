from src.data_store import data_store
from src.error import InputError, AccessError
from src.helpers import decode_token
from src.helpers import check_if_token_exists
from src.helper import get_user_idx

def dm_remove_v1(token,dm_id):

    dms = data_store.get()['dms']
    users = data_store.get()['users']

    # Check token is valid and u_id exists
    token_valid = False
    user_exists = False
    if not check_if_token_exists(token):
        raise AccessError(description="Invalid token")
    else:
        u_id = int(decode_token(token))
        token_valid is True

    u_ids = [user['u_ids'] for user in users]
    if u_id in u_ids:
        user_exists is True
    else: 
        raise InputError("ERROR: User id does not exist")

    # Check dm_id is valid and exists
    dm_id_valid = False
    dm_ids = [dm['dm_id'] for dm in dms]
    if dm_id in dm_ids:
        dm_id_valid is True
    else:
        raise InputError("ERROR: Dm id does not exist")

    # Check token is from owner of dm_id and is still in the dm
    user_is_owner = False
    idx = find_dm_index(dm_id)
    owners = dms[idx]['owner_members']['u_id']
    if u_id in owners:
        user_is_owner is True
    else:
        raise AccessError ("ERROR: User is not the owner of this Dm")

    user_in_dm = False
    users_dms_list = dm_list_v1(token)
    if dm_id in users_dms_list:
        user_in_dm is True
    else:
        raise AccessError ("ERROR: User is not in Dm")
    
    # If all conditions followed, delete dm from dms list in data struct
    if token_valid and user_exists and dm_id_valid and user_is_owner and user_in_dm:
        del dms[idx]

    return{}


def dm_list_v1(token):

    # initialise datastore and dicts
    data = data_store.get()
    dms_list = data['dms']
    dms_dict = {'dms' : []}
    
    # if token doesnt exist return AccessError
    if not check_if_token_exists(token):
        raise AccessError(description="Invalid token")
    
    u_id = int(decode_token(token))

    # loop through data_store and if u_id is in dm
    # add dms and names to dict
    for dm in dms_list:
        for member in dm['all_members']:
            if u_id == member['u_id']:
                dm_id = dm['dm_id']
                name = dm['name']
                dms_dict['dms'].append({'dm_id' : dm_id, 'name' : name})

    return dms_dict

def find_dm_index(dm_id):
    data = data_store.get()

    i = 0
    for dm in data["dms"]:
        if dm["dm_id"] == dm_id:
            return i
        else:
            i += 1
    return None


def is_in_dm(auth_user_id, right_dm):
    for member in right_dm["all_members"]:
        if auth_user_id == member["u_id"]:
            return True

    return False

def dm_details_v1(token, dm_id):
    # initialise datastore and dicts
    data = data_store.get()

    # if token doesnt exist return AccessError
    if not check_if_token_exists(token):
        raise AccessError(description="Invalid token")
    
    u_id = int(decode_token(token))
    
    right_dm_index = find_dm_index(dm_id)

    # error
    if right_dm_index is None:
        raise InputError("dm_id does not refer to a valid dm")

    right_dm = data["dms"][right_dm_index]

    if not is_in_dm(u_id, right_dm):
        raise AccessError("dm_id is valid and the authorised user is not a member of the dm")

    return {
        'name': right_dm["name"],
        'owner_members': right_dm['owner_members'],
        'all_members': right_dm['all_members'],
    } 

def generate_dm_handle(u_ids, users):
    handles = []
    for u_id in u_ids:
        idx = get_user_idx(users, u_id) 
        handles.append(users[idx]["handle_str"])
    return handles

def dm_create_v1(token, u_ids):
    if not check_if_token_exists(token):
        raise AccessError(description="Invalid Token!")

    owner_uid = decode_token(token)
    data = data_store.get() 
    users = data["users"]
    
    handles = generate_dm_handle(u_ids, users)
    handles = sorted(handles)
    name = ", ".join(handles)
    
    host_info = data["users"][owner_uid]
    host_info_list = [{
        'u_id': host_info["u_id"],
    }]
    all_members_list = host_info_list
    owner_members_list = host_info_list.copy()
    
    dm_id = len(data['dms'])
    data['dms'].append({
        "dm_id" : dm_id,
        "name" : name,
        'owner_member': owner_members_list,
        'all_members': all_members_list,
        'messages': []
    })
    
    data_store.set(data)

    return {
        'dm_id': dm_id
    }
