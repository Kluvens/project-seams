from src.data_store import data_store
from src.error import AccessError
from src.other import clear_v1
from src.auth import auth_register_v1

# from data_store import data_store
# from error import AccessError
# from other import clear_v1
# from auth import auth_register_v1

def channels_list_v1(auth_user_id):

    # if auth_user_id doesnt exist return AccessError
    try:
        auth_user_id + 1 - 1
    except:
        raise AccessError

    data = data_store.get()

    channels = data['channels']
    channel_id_list = []
    name_list = []

    for x in range(len(channels)):
        for y in range(len(channels[x]['all_members'])):
            if channels[x]['all_members'][y]['u_id'] == auth_user_id:
                channel_idv = (channels[x]['channel_id'])
                channel_id_list.append(channel_idv)
                namev = (channels[x]['name'])
                name_list.append(namev)

    """
    print(channel_id_list)
    print(name_list)

    dic = {}
    for channel_id in channel_id_list:
        for name in name_list:
            dic[channel_id] = name
            name_list.remove(name)
            break

    print(dic)
    """

    data_store.set(data)

    return {
        'channels': [
            {
                'channel_id': [channel_id_list],
                'name': [name_list],
            }
        ],
    }


def channels_listall_v1(auth_user_id):
    return {
        'channels': [
            {
                'channel_id': 1,
                'name': 'My Channel',
            }
        ],
    }

def channels_create_v1(auth_user_id, name, is_public):
    data = data_store.get()

    host_info = data["users"][auth_user_id]

    channel_id = len(data["channels"])

    if len(name) < 1 or len(name) > 20:
        raise InputError("length of name is less than 1 or more than 20 characters")

    data["channels"].append(
        {
            'channel_id': channel_id,
            'name': name,
            'is_public': is_public,
            'owner_members': [{
                'u_id': host_info["u_id"],
                'email': host_info["email"],
                'name_first': host_info["name_first"],
                'name_last': host_info["name_last"],
            }],
            'all_members': [{
                'u_id': host_info["u_id"],
                'email': host_info["email"],
                'name_first': host_info["name_first"],
                'name_last': host_info["name_last"],
            }],
        }
    )

    data_store.set(data)

    return {
        'channel_id': channel_id,
    }


if __name__ == "__main__":
    clear_v1()
    # create user
    u_id1 = auth_register_v1("james@gmail.com", "abcdefg123", "James", "Cai")
    u_id2 = auth_register_v1("james2@gmail.com", "abcdefg123", "Jam", "Cao")
    # create channels
    x = channels_create_v1(u_id1['auth_user_id'], "ch1", True)
    y = channels_create_v1(u_id1['auth_user_id'], "ch2", False)
    listv1 = channels_list_v1(u_id1['auth_user_id'])

    assert listv1['channels'][u_id1['auth_user_id']] == {'channel_id': [[0, 1]], 'name': [['ch1', 'ch2']]}