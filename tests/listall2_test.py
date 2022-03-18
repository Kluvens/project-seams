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

# test if listall func displays all channels including public and private
def test_listall_public_and_private():
    clear_v1()

    # create user
    u_id = register_user1()

    token_1 = u_id1['token']

    # create channels
    ch1 = create_public_channel1(token_1)
    ch2 = create_private_channel2(token_1)

    listall = channels_listall_v2(token_1)

    # assert listall returns filled dict
    assert listall['channels'] == [{'channel_id': ch1["channel_id"], 'name': 'ch1'},
                                {'channel_id': ch2["channel_id"], 'name': 'ch2'}]

def test_listall_public_only():
    clear_v1()

    # create user
    u_id = register_user1()

    token_1 = u_id1['token']

    # create channels
    ch1 = create_public_channel1(token_1)
    ch2 = create_public_channel2(token_1)

    listall = channels_listall_v2(token_1)

    # assert listall returns filled dict
    assert listall['channels'] == [{'channel_id': ch1["channel_id"], 'name': 'ch1'},
                                {'channel_id': ch2["channel_id"], 'name': 'ch2'}]

def test_listall_private_only():
    clear_v1()

    # create user
    u_id = register_user1()

    token_1 = u_id1['token']

    # create channels
    ch1 = create_private_channel1(token_1)
    ch2 = create_private_channel2(token_1)

    listall = channels_listall_v2(token_1)

    # assert listall returns filled dict
    assert listall['channels'] == [{'channel_id': ch1["channel_id"], 'name': 'ch1'},
                                {'channel_id': ch2["channel_id"], 'name': 'ch2'}]

# test listall func when no channels exist
def test_listall_no_channels():
    clear_v1()

    # create user
    u_id = register_user1()

    token_1 = u_id1['token']

    listall = channels_listall_v2(token_1)

    # assert listall returns empty dict
    assert listall == {'channels': []}

# test listall when multiple channels and users
def test_multiple_users_and_channels():
    clear_v1()

    # create user
    u_id1 = register_user1()
    u_id2 = register_user2()

    token_1 = u_id1['token']
    token_2 = u_id2['token']

    # create channels
    ch1 = create_private_channel1(token_1)
    ch2 = create_private_channel2(token_1)
    ch3 = create_public_channel3(token_2)

    listall = channels_listall_v2(token_1)

    # assert listall returns filled dict
    assert listall['channels'] == [{'channel_id': ch1["channel_id"], 'name': 'ch1'},
                                {'channel_id': ch2["channel_id"], 'name': 'ch2'},
                                {'channel_id': ch3["channel_id"], 'name': 'ch3'}]
