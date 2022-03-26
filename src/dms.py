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
        for messages in dm['messages']:
            if u_id == messages['u_id']:
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
    for member in right_dm["messages"]:
        if auth_user_id == member["u_id"]:
            return True

    return False

def dm_details_v1(token, dm_id):
    # initialise datastore and dicts
    data = data_store.get()
    dms = data['dms']

    # if token doesnt exist return AccessError
    if not check_if_token_exists(token):
        raise AccessError(description="Invalid token")
    
    u_id = int(decode_token(token))
    
    right_dm_index = get_dm_idx(dms, dm_id)

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

def dm_create(token, u_ids):
    if not check_if_token_exists(token):
        raise AccessError(description="Invalid Token!")

    # Assuming token is valid
    owner_uid = decode_token(token)
    data = data_store.get()
    users = data["users"]
    handles = generate_dm_handle(u_ids, users)
    handles = sorted(handles)
    name = ", ".join(handles)

    dm_id = len(data['dms'])
    data['dms'].append({"dm_id" : dm_id, "owner" : owner_uid, "name" : name})

    return dm_id
