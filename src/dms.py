# u_ids contains the user(s) that this DM is directed to, 
# and will not include the creator. The creator is the owner of the DM. 
# name should be automatically generated based on the users that are in this DM. 
# The name should be an alphabetically-sorted,
#  comma-and-space-separated list of user handles, e.g. 'ahandle1, bhandle2, chandle3'.

from src.helpers import decode_token
from src.helpers import check_if_token_exists
from src.error import AccessError, InputError
from src.data_store import data_store
from src.auth import auth_register_v1
from src.helpers import get_user_idx

def generate_dm_handle(u_ids, users):
    handles = []
    for u_id in u_ids:
        idx = get_user_idx(users, u_id) 
        handles.append(users[idx]["handle_str"])
    return handles

def dm_create_v1(token, u_ids):
    if not check_if_token_exists(token):
        raise AccessError(description="Invalid Token!")

    # Assuming token is valid
    owner_uid = decode_token(token)
    data = data_store.get()
    users = data["users"]

    u_ids.append(owner_uid)
    handles = generate_dm_handle(u_ids, users)
    handles = sorted(handles)
    name = "".join(handles)

    dm_id = len(data['dms'])
    data['dms'].append({"dm_id" : dm_id, "owner" : owner_uid, "name" : name})

    return {"dm_id" : dm_id}

if __name__ == "__main__":
    u0 = auth_register_v1("k@gl.com", "dgdsgasd", "SGdf", "Gsdf")
    u1 = auth_register_v1("k1@gl.com", "dgdsgasd", "SGdgff", "Ghgnsdf")
    u2 = auth_register_v1("k2@gl.com", "dgdsgasd", "SGddvsf", "Gsndf")

    dm_create_v1(u0["token"], [u1["auth_user_id"], u2["auth_user_id"]])
    data = data_store.get()
    print(data["dms"])
