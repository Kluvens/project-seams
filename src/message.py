from time import time
from src.dms import get_dm_idx

def message_senddm_v1(token, dm_id, message):
    data = data_store.get()

    # if token doesnt exist return AccessError
    if not check_if_token_exists(token):
        raise AccessError(description="Invalid token")
    auth_user_id = int(decode_token(token))

    right_dm_index = get_dm_idx(dms, dm_id)

    # error
    if right_dm_index is None:
        raise InputError("dm_id does not refer to a valid dm")

    if len(message) < 1 or len(message) > 1000:
        raise InputError("length of message is less than 1 or over 1000 characters")

    dms = data['dms']
    right_dm = dms[right_dm_index]

    if not is_in_dm(auth_user_id, right_dm):
        raise AccessError("dm_id is valid and the authorised user is not a member of the dm")

    num_messages = len(right_dm['messages'])

    data['unique_message_id'] += 1
    
    right_dm.append(
        {
            'message_id': num_messages,
            'u_id': u_id,
            'message': message,
            'time_sent': int(time()),
        }
    )

    return {
        'message_id': data['unique_message_id']
    }