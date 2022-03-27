from src.data_store import data_store
from src.error import InputError, AccessError
from src.helpers import decode_token
from src.helpers import check_if_token_exists
from src.helper import get_user_idx

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
        for members in dm['all_members']:
            if u_id == members['u_id']:
                dm_id = dm['dm_id']
                name = dm['name']
                dms_dict['dms'].append({'dm_id' : dm_id, 'name' : name})

    return dms_dict

def find_dm_index(dms, dm_id):    
    for idx, dm in enumerate(dms):
        if dm['dm_id'] == dm_id:
            return idx
    return None

def is_in_dm(u_id, right_dm):
    for member in right_dm["all_members"]:
        if u_id == member["u_id"]:
            return True

    return False

def dm_details_v1(token, dm_id):
    
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

def generate_dm_handle(owner_uid, u_ids, users):
    handles = []
    idx = get_user_idx(users, owner_uid) 
    handles.append(users[idx]["handle_str"])
    for u_id in u_ids:
        idx = get_user_idx(users, u_id) 
        handles.append(users[idx]["handle_str"])
    return handles

def dm_create_v1(token, u_ids):
    
    # if token doesnt exist return AccessErr
    if not check_if_token_exists(token):
        raise InputError(description="Invalid Token!")

    owner_uid = decode_token(token)
    data = data_store.get() 
    users = data["users"]
    
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
    data['dms'].append({
        "dm_id" : dm_id,
        "name" : name,
        'owner_member': owner_members_list,
        'all_members': members_list,
        'messages': []
    })
    
    data_store.set(data)

    return {
        'dm_id': dm_id
    }

def dm_leave_v1(token, dm_id):

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

    u_ids = [user['u_id'] for user in users]
    if u_id in u_ids:
        user_exists is True
    else: 
        raise InputError(description="ERROR: User id does not exist")

    # Check dm_id is valid and exists
    dm_id_valid = False
    dm_ids = [dm['dm_id'] for dm in dms]
    if dm_id in dm_ids:
        dm_id_valid is True
    else:
        raise InputError(description="ERROR: Dm id does not exist")

    # Check token is from owner of dm_id and is still in the dm
    user_is_owner = False
    idx = find_dm_index(dms, dm_id)
    owners = dms[idx]['all_members'][0]['u_id']
    if u_id == owners:
        user_is_owner is True
    else:
        raise AccessError (description="ERROR: User is not the owner of this Dm")

    user_in_dm = False
    users_dms_list = dm_list_v1(token).get('dms')
    final_dms_list = [member['dm_id'] for member in users_dms_list]

    if dm_id in final_dms_list:
        user_in_dm is True
    else:
        raise AccessError (description="ERROR: User is not in Dm")
    
    # If all conditions followed, delete dm from dms list in data struct
    if token_valid and user_exists and dm_id_valid and user_is_owner and user_in_dm:
        del dms[idx]

    return{}

