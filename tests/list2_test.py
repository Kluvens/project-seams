import pytest

from src.channels import channels_list_v2, channels_listall_v2, channels_create_v2
from src.other import clear_v1
from src.error import AccessError
from src.auth import auth_register_v2

@pytest.fixture
def register_user1():
    return auth_register_v2('e1@gmail.com', 'abcdefg123', 'James', 'Cai')

@pytest.fixture
def register_user2():
    return auth_register_v2('e2@gmail.com', 'abcdefg123', 'Jam', 'Cao')

@pytest.fixture
def create_public_channel1(token):
    return channels_create_v2(token, "ch1", True)

@pytest.fixture
def create_public_channel2(token):
    return channels_create_v2(token, "ch2", True)

@pytest.fixture
def create_public_channel3(token):
    return channels_create_v2(token, "ch3", True)

@pytest.fixture
def create_private_channel1(token):
    return channels_create_v2(token, "ch1", False)

@pytest.fixture
def create_private_channel2(token):
    return channels_create_v2(token, "ch2", False)

@pytest.fixture
def create_private_channel3(token):
    return channels_create_v2(token, "ch3", False)

# =============================TESTING CORRECTNESS============================

# test if list func doesn't return dict when inputting user_id with
# non-existant channel public and private
def test_no_channels_joined_private():
    clear_v1()

    # create two users
    u_id1 = register_user1()
    u_id2 = register_user2()

    token_1 = u_id1['token']
    token_2 = u_id2['token']

    # create private channel for user 1
    create_private_channel1(token_1)

    # return channels for user 2 (non-existant)
    listv2 = channels_list_v2(token_2)
    
    assert listv2 == {'channels': []}

def test_no_channels_joined_public():
    clear_v1()

    # create two users
    u_id1 = register_user1()
    u_id2 = register_user2()

    token_1 = u_id1['token']
    token_2 = u_id2['token']

    # create public channel for user 1
    create_public_channel1(token_1)

    # return channels for user 2 (non-existant)
    listv2 = channels_list_v2(token_2)
    
    assert listv2 == {'channels': []}

# test func output when user has joined all channels public and private
def test_user_join_all_channels_private():
    clear_v1()

    # create user
    u_id1 = register_user1()
    register_user2()

    token_1 = u_id1['token']

    # create channels
    ch1 = create_private_channel1(token_1)
    ch2 = create_private_channel2(token_1)

    listv2 = channels_list_v2(token_1)

    # assert user 1 is part of all channels
    assert listv2['channels'] == [{'channel_id': ch1['channel_id'], 'name': 'ch1'},
                                {'channel_id': ch2['channel_id'], 'name': 'ch2'}]

def test_user_join_all_channels_public():
    clear_v1()

    # create user
    u_id1 = register_user1()
    register_user2()

    token_1 = u_id1['token']

    # create channels
    ch1 = create_public_channel1(token_1)
    ch2 = create_public_channel2(token_1)

    listv2 = channels_list_v2(token_1)

    # assert user 1 is part of all channels
    assert listv2['channels'] == [{'channel_id': ch1['channel_id'], 'name': 'ch1'}, 
                                {'channel_id': ch2['channel_id'], 'name': 'ch2'}]

# test func output when user has joined some channels public and private
def test_user_join_some_channels_private():
    clear_v1()

    # create users
    u_id1 = register_user1()
    u_id2 = register_user2()

    token_1 = u_id1['token']
    token_2 = u_id2['token']

    # create channels with u_id1 as owner of ch1 and ch2 and not a member
    # of ch3
    ch1 = create_private_channel1(token_1)
    ch2 = create_private_channel2(token_1)
    create_private_channel3(token_2)

    listv2 = channels_list_v2(token_1)

    # assert user 1 is part of ch1 and ch2
    assert listv2['channels'] == [{'channel_id': ch1['channel_id'], 'name': 'ch1'}, 
                                {'channel_id': ch2['channel_id'], 'name': 'ch2'}]

def test_user_join_some_channels_public():
    clear_v1()

    # create users
    u_id1 = register_user1()
    u_id2 = register_user2()

    token_1 = u_id1['token']
    token_2 = u_id2['token']

    # create channels with u_id1 as owner of ch1 and ch2 and not a member
    # of ch3
    ch1 = create_public_channel1(token_1)
    ch2 = create_public_channel2(token_1)
    create_public_channel3(token_2)

    listv2 = channels_list_v2(token_1)

    # assert user 1 is part of ch1 and ch2
    assert listv2['channels'] == [{'channel_id': ch1['channel_id'], 'name': 'ch1'}, 
                                {'channel_id': ch2['channel_id'], 'name': 'ch2'}]
