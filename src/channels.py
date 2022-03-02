from src.data_store import data_store

def channels_list_v1(auth_user_id):

    # if auth_user_id doesnt exist return AccessError

    data = data_store.get()

    channels = data['channels']
    cid_list = []
    name_list = []

    for x in range(len(channels)):
        for y in range(len(channels[x]['all_members'])):
            if channels[x]['all_members'][y]['uid'] == auth_user_id:
                cidv = (channels[x]['cid'])
                cid_list.append(cidv)
                namev = (channels[x]['name'])
                name_list.append(namev)

    """
    print(cid_list)
    print(name_list)
    
    dic = {}
    for cid in cid_list:
        for name in name_list:
            dic[cid] = name
            name_list.remove(name)
            break  
    
    print(dic)
    """

    return {
        'channels': [
        	{
        		'channel_id': [cid_list],
        		'name': [name_list],
        	}
        ],
    }
    
def channels_listall_v1(auth_user_id):

    # if auth_user_id doesnt exist return AccessError

    data = data_store.get()

    channels = data['channels']
    cid_list = []
    name_list = []

    for x in range(len(channels)):
        for y in range(len(channels[x]['all_members'])):
            cidv = (channels[x]['cid'])
            cid_list.append(cidv)
            namev = (channels[x]['name'])
            name_list.append(namev)

    return {
        'channels': [
        	{
        		'channel_id': [cid_list],
        		'name': [name_list],
        	}
        ],
    }

def channels_create_v1(auth_user_id, name, is_public):
    return {
        'channel_id': 1,
    }
