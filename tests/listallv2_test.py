import pytest

from src.channels import channels_listall_v2, channels_create_v1
from src.other import clear_v1
from src.error import AccessError
from src.auth import auth_register_v1

# =============================TESTING CORRECTNESS============================

# test if listall func displays all channels including public and private
def test_listall_public_and_private():
    clear_v1()

    # create user
    u_id = auth_register_v1("e1@gmail.com", "abcdefg123", "James", "Cai")

    # create channels
    ch1 = channels_create_v1(u_id['token'], "ch1", True)
    ch2 = channels_create_v1(u_id['token'], "ch2", False)

    listall = channels_listall_v2(u_id['token'])

    # assert listall returns filled dict
    assert listall['channels'] == [{'channel_id': ch1["channel_id"], 'name': 'ch1'},
                                {'channel_id': ch2["channel_id"], 'name': 'ch2'}]

def test_listall_public_only():
    clear_v1()

    # create user
    u_id = auth_register_v1("e1@gmail.com", "abcdefg123", "James", "Cai")

    # create channels
    ch1 = channels_create_v1(u_id['token'], "ch1", True)
    ch2 = channels_create_v1(u_id['token'], "ch2", True)

    listall = channels_listall_v2(u_id['token'])

    # assert listall returns filled dict
    assert listall['channels'] == [{'channel_id': ch1["channel_id"], 'name': 'ch1'},
                                {'channel_id': ch2["channel_id"], 'name': 'ch2'}]

def test_listall_private_only():
    clear_v1()

    # create user
    u_id = auth_register_v1("e1@gmail.com", "abcdefg123", "James", "Cai")

    # create channels
    ch1 = channels_create_v1(u_id['token'], "ch1", False)
    ch2 = channels_create_v1(u_id['token'], "ch2", False)

    listall = channels_listall_v2(u_id['token'])

    # assert listall returns filled dict
    assert listall['channels'] == [{'channel_id': ch1["channel_id"], 'name': 'ch1'},
                                {'channel_id': ch2["channel_id"], 'name': 'ch2'}]

# test listall func when no channels exist
def test_listall_no_channels():
    clear_v1()

    # create user
    u_id = auth_register_v1("e1@gmail.com", "abcdefg123", "James", "Cai")

    listall = channels_listall_v2(u_id['token'])

    # assert listall returns empty dict
    assert listall == {'channels': []}

# test listall when multiple channels and users
def test_multiple_users_and_channels():
    clear_v1()

    # create user
    u_id1 = auth_register_v1("e1@gmail.com", "abcdefg123", "James", "Cai")
    u_id2 = auth_register_v1("e2@gmail.com", "abcdefg123", "Jam", "Cao")

    # create channels
    ch1 = channels_create_v1(u_id1['token'], "ch1", False)
    ch2 = channels_create_v1(u_id1['token'], "ch2", False)
    ch3 = channels_create_v1(u_id2['token'], "ch3", False)

    listall = channels_listall_v2(u_id1['token'])

    # assert listall returns filled dict
    assert listall['channels'] == [{'channel_id': ch1["channel_id"], 'name': 'ch1'},
                                {'channel_id': ch2["channel_id"], 'name': 'ch2'},
                                {'channel_id': ch3["channel_id"], 'name': 'ch3'}]

# =============================TESTING ERRORS================================

def test_invalid_input_string():
    clear_v1()
    with pytest.raises(AccessError):
        channels_listall_v2('BOBbob')

def test_invalid_input_invalid_user_id():
    clear_v1()
    with pytest.raises(AccessError):
        channels_listall_v2(10)
