# Import 
import pytest
from channel import channel_join_v1 
from error import InputError, AccessError
from auth import auth_register_v1
from other import clear_v1
from channels import channels_create_v1
from data_store import data_store

# channel join tests
def test_channel_join_InputError(): 

    clear_v1()

    # Create Global Owner
    user1 = auth_register_v1('user1@test.com', '0000001', 'Amelie', 'Amelies')

    # Create Global member
    user2 = auth_register_v1('user2@test.com', '0000002', 'Ben', 'Bens')

    # Global Owner creates public channel
    channel_id_public = channels_create_v1(user1['auth_user_id'], 'public test channel', True) 

    # Join invalid channel
    with pytest.raises(InputError) as error:
        channel_join_v1(user1['auth_user_id'],'this is not a channel')
    assert error.type == InputError

    # Join channel that user has already joined
    channel_join_v1(user2['auth_user_id'],channel_id_public['channel_id'])

    with pytest.raises(InputError) as error:
        channel_join_v1(user2['auth_user_id'],channel_id_public['channel_id'])
    assert error.type == InputError

def test_channel_join_AccessError():

    clear_v1()

    # Create Global Owner
    user1 = auth_register_v1('user1@test.com', '0000001', 'Amelie', 'Amelies')

    # Create Global member
    user2 = auth_register_v1('user2@test.com', '0000002', 'Ben', 'Bens')

    # Global Owner creates private channel
    channel_id_private = channels_create_v1(user1['auth_user_id'], 'private test channel', False) 

    with pytest.raises(AccessError) as error:
        channel_join_v1(user2['auth_user_id'],channel_id_private['channel_id'])
    assert error.type == AccessError

def test_channel_join_Success():
    clear_v1()

    # Create Global Owner
    user1 = auth_register_v1('user1@test.com', '0000001', 'Amelie', 'Amelies')

    # Create Global member
    user2 = auth_register_v1('user2@test.com', '0000002', 'Ben', 'Bens')

    # Global Owner creates public channel
    channel_id_public = channels_create_v1(user1['auth_user_id'], 'public test channel', True) 

    # Global Member creates private channel
    channel_id_private = channels_create_v1(user2['auth_user_id'], 'private test channel', False) 

    # Global owner joins private channel
    channel_join_v1(user1['auth_user_id'],channel_id_private['channel_id'])
    
    # Check global owner has joined private channel successfully 
    store = data_store.get()
    channels = store['channels']

    for channel in channels:
        if channel['channel_id'] == channel_id_private['channel_id']:
            users = channel['users']
            user_exists = False
            for user in users:
                if user['auth_user_id'] == user1["auth_user_id"]:
                    user_exists = True
                    break
            assert user_exists == True 
            break

    # Global member joins public channel 
    channel_join_v1(user2['auth_user_id'],channel_id_public['channel_id'])

    for channel in channels:
        if channel['channel_id'] == channel_id_public['channel_id']:
            users = channel['users']
            user_exists = False
            for user in users:
                if user['auth_user_id'] == user2["auth_user_id"]:
                    user_exists = True
                    break
            assert user_exists == True 
            break



    
        






