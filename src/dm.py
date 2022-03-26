from src.helpers import decode_token
from src.helpers import check_if_token_exists
from src.error import AccessError, InputError
from src.data_store import data_store
from src.auth import auth_register_v1
from src.helper import get_user_idx

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