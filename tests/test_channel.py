from dataclasses import dataclass
import pytest

from src.channel import channel_details_v1, channel_join_v1, channel_invite_v1
from src.error import InputError, AccessError
from src.auth import auth_register_v1
from src.other import clear_v1
from src.channels import channels_create_v1, channels_listall_v1, channels_list_v1

# Channel invite tests
def test_channel_invite_InputError():
    clear_v1()

    # Create Global Owner
    user1 = auth_register_v1('user1@test.com', '0000001', 'Amelie', 'Amelies')
    # Create Global member
    user2 = auth_register_v1('user2@test.com', '0000002', 'Ben', 'Bens')
    # Global Owner creates public channel
    channel_id_public = channels_create_v1(user1['auth_user_id'], 'public test channel', True) 
    # Global Owner creates private channel
    channels_create_v1(user1['auth_user_id'], 'private test channel', False) 

    # Input invalid channel
    # channel_invite_v1(user1['auth_user_id'],'420',user2['auth_user_id'])

    with pytest.raises(InputError) as error:
        channel_invite_v1(user1['auth_user_id'],'420',user2['auth_user_id'])
    assert error.type == InputError

    # Input invalid u_id user
    # channel_invite_v1(user1['auth_user_id'],channel_id_public['channel_id'], '96')

    with pytest.raises(InputError) as error:
        channel_invite_v1(user1['auth_user_id'],channel_id_public['channel_id'], '96')
    assert error.type == InputError

    # Invite user to channel they have already joined 
    # channel_invite_v1(user1['auth_user_id'], channel_id_public['channel_id'],user1['auth_user_id'])

    with pytest.raises(InputError) as error:
        channel_invite_v1(user1['auth_user_id'],channel_id_public['channel_id'],user1['auth_user_id'])
    assert error.type == InputError

def test_channel_invite_AccessError():
    clear_v1()

    # Create Global Owner
    user1 = auth_register_v1('user1@test.com', '0000001', 'Amelie', 'Amelies')
    # Create Global member 1
    user2 = auth_register_v1('user2@test.com', '0000002', 'Ben', 'Bens')
    # Create Global member 2
    user3 = auth_register_v1('user3@test.com', '0000003', 'Charlie', 'Charlies')
    # Global owner creates private channel
    channel_id_private = channels_create_v1(user1['auth_user_id'], 'private test channel', False) 

    # Global member 1 tries to give global memebr 2 an invite
    # channel_invite_v1(user2['auth_user_id'], channel_id_private['channel_id'],user3['auth_user_id'])

    with pytest.raises(AccessError) as error:
        channel_invite_v1(user2['auth_user_id'],channel_id_private['channel_id'],user3['auth_user_id'])
    assert error.type == AccessError

def test_channel_invite_success():
    clear_v1()

    # Create Global Owner
    user1 = auth_register_v1('user1@test.com', '0000001', 'Amelie', 'Amelies')
    # Create Global member 1
    user2 = auth_register_v1('user2@test.com', '0000002', 'Ben', 'Bens')
    # Global ownder creates private channel
    channel_id_private = channels_create_v1(user1['auth_user_id'], 'private test channel', False)

    # Invite Global member 1 to private channel
    channel_invite_v1(user1['auth_user_id'],channel_id_private['channel_id'],user2['auth_user_id'])

    # Check user had been added to channel
    user_in_channel = False
    channel_info = channel_details_v1(user1['auth_user_id'],channel_id_private['channel_id'])
    channel_members = channel_info['all_members']
    for member in channel_members:
        if member['u_id'] == user2['auth_user_id']:
            user_in_channel = True
            break

    assert user_in_channel == True
     

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

    # join channel
    channel_join_v1(user2['auth_user_id'],channel_id_public['channel_id'])
    # Join channel that user has already joined
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
        channel_join_v1(user2['auth_user_id'], channel_id_private['channel_id'])
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
    members_list_private = channel_details_v1(user1['auth_user_id'],channel_id_private['channel_id'])["all_members"]

    user_exists1 = False 
    for member in members_list_private:
        if member['u_id'] == user1['auth_user_id']:
            user_exists1 = True
            break

    assert user_exists1 == True 

    # Global member joins public channel 
    channel_join_v1(user2['auth_user_id'],channel_id_public['channel_id'])

    # Check Global member has joined public channel sucessfully 
    members_list_public = channel_details_v1(user2['auth_user_id'],channel_id_public['channel_id'])['all_members']

    user_exists2 = False
    for member in members_list_public:
        if member['u_id'] == user2['auth_user_id']:
            user_exists2 = True
            break

    assert user_exists2 is True 
