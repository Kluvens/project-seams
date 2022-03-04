from src.data_store import data_store

def channels_list_v1(auth_user_id):
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
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

def channels_create_v1(auth_user_id, channel_name, is_public):
    data = data_store.get()
    print(data)
    print(auth_user_id)
    print(channel_name)
    
    host_info = data["users"][auth_user_id]
    # print(host_info)
    channel_id = len(data["channels"])

    # error
    if len(channel_name) < 1 or len(channel_name) > 20:
        raise InputError("length of name is less than 1 or more than 20 characters")

    data["channels"].append(
        {
            'channel_id': channel_id,
            'name': cahnnel_name,
            'is_public': is_public,
            'owner_members': [
                {
                    'u_id': host_info["u_id"],
                    'email': host_info["email"],
                    'name_first': host_info["name_first"],
                    'name_last': host_info["name_last"],
                    'handle_str': host_info["handle_str"],
                }
            ],
            'all_members': [
                {
                    'u_id': host_info["u_id"],
                    'email': host_info["email"],
                    'name_first': host_info["name_first"],
                    'name_last': host_info["name_last"],
                    'handle_str': host_info["handle_str"],
                }
            ],
        }
    )

    data_store.set(data)

    return {
        'channel_id': channel_id,
    }

channels_create_v1(1, "Tony_channel", True)
