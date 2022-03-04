import pytest

from src.channels import channels_list_v1, channels_listall_v1, channels_create_v1
from src.other import clear_v1
from src.error import AccessError
from src.auth import auth_register_v1

# =============================TESTING CORRECTNESS============================

# test if list func doesn't return dict when inputting user_id with
# non-existant channel public and private
def test_no_channels_joined_public():
    clear_v1()

    # create two users
    u_id1 = auth_register_v1("e1@gmail.com", "abcdefg123", "James", "Cai")
    u_id2 = auth_register_v1("e2@gmail.com", "abcdefg123", "Jam", "Cao")

    # create private channel for user 1
    channels_create_v1(u_id1['auth_user_id'], "ch1", False)

    # return channels for user 2 (non-existant)
    listv1 = channels_list_v1(u_id2['auth_user_id'])

    # pass if trying to access non-existant channel
    with pytest.raises(IndexError):
        listv1['channels'][u_id2['auth_user_id']]

def test_no_channels_joined_private():
    clear_v1()

    # create two users
    u_id1 = auth_register_v1("e1@gmail.com", "abcdefg123", "James", "Cai")
    u_id2 = auth_register_v1("e2@gmail.com", "abcdefg123", "Jam", "Cao")

    # create public channel for user 1
    channels_create_v1(u_id1['auth_user_id'], "ch1", True)

    # return channels for user 2 (non-existant)
    listv1 = channels_list_v1(u_id2['auth_user_id'])

    # pass if trying to access non-existant channel 
    with pytest.raises(IndexError):
        listv1['channels'][u_id2['auth_user_id']]

# test func output when user has joined all channels public and private
def test_user_join_all_channels_public():
    clear_v1()

    # create user
    u_id1 = auth_register_v1("james@gmail.com", "abcdefg123", "James", "Cai")
    u_id2 = auth_register_v1("james2@gmail.com", "abcdefg123", "Jam", "Cao")

    # create channels
    channels_create_v1(u_id1['auth_user_id'], "ch1", False)
    channels_create_v1(u_id1['auth_user_id'], "ch2", False)

    listv1 = channels_list_v1(u_id1['auth_user_id'])

    # assert user 1 is part of all channels
    assert listv1['channels'][u_id1['auth_user_id']] == {'channel_id': '0, 1', 'name': 'ch1, ch2'}

def test_user_join_all_channels_private():
    clear_v1()

    # create user
    u_id1 = auth_register_v1("james@gmail.com", "abcdefg123", "James", "Cai")
    u_id2 = auth_register_v1("james2@gmail.com", "abcdefg123", "Jam", "Cao")

    # create channels
    channels_create_v1(u_id1['auth_user_id'], "ch1", True)
    channels_create_v1(u_id1['auth_user_id'], "ch2", True)

    listv1 = channels_list_v1(u_id1['auth_user_id'])

    # assert user 1 is part of all channels
    assert listv1['channels'][u_id1['auth_user_id']] == {'channel_id': '0, 1', 'name': 'ch1, ch2'}

# test func output when user has joined some channels public and private
def test_user_join_some_channels_public():
    clear_v1()

    # create users
    u_id1 = auth_register_v1("e1@gmail.com", "abcdefg123", "James", "Cai")
    u_id2 = auth_register_v1("e2@gmail.com", "abcdefg1234", "Jam", "Cao")

    # create channels with u_id1 as owner of ch1 and ch2 and not a member
    # of ch3
    channels_create_v1(u_id1['auth_user_id'], "ch1", False)
    channels_create_v1(u_id1['auth_user_id'], "ch2", False)
    channels_create_v1(u_id2['auth_user_id'], "ch3", False)

    listv1 = channels_list_v1(u_id1['auth_user_id'])

    # assert user 1 is part of ch1 and ch2
    assert listv1['channels'][u_id1['auth_user_id']] == {'channel_id': '0, 1', 'name': 'ch1, ch2'}

def test_user_join_some_channels_private():
    clear_v1()

    # create users
    u_id1 = auth_register_v1("e1@gmail.com", "abcdefg123", "James", "Cai")
    u_id2 = auth_register_v1("e2@gmail.com", "abcdefg1234", "Jam", "Cao")

    # create channels with u_id1 as owner of ch1 and ch2 and not a member
    # of ch3
    channels_create_v1(u_id1['auth_user_id'], "ch1", True)
    channels_create_v1(u_id1['auth_user_id'], "ch2", True)
    channels_create_v1(u_id2['auth_user_id'], "ch3", True)

    listv1 = channels_list_v1(u_id1['auth_user_id'])

    # assert user 1 is part of ch1 and ch2
    assert listv1['channels'][u_id1['auth_user_id']] == {'channel_id': '0, 1', 'name': 'ch1, ch2'}

# =============================TESTING ERRORS================================

def test_invalid_list_input():
    clear_v1()
    with pytest.raises(AccessError):
        channels_list_v1('BOBbob')