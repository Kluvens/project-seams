import pytest

from src.channels import channels_list_v1, channels_listall_v1, channels_create_v1
from src.other import clear_v1
from src.data_store import data_store
from src.error import InputError, AccessError
from src.auth import auth_register_v1

# =============================TESTING CORRECTNESS============================

# test if listall func displays all channels including public and private
def test_listall_public_and_private():
    clear_v1()

    # create user
    uid1 = auth_register_v1("e1@gmail.com", "abcdefg123", "James", "Cai")

    # create channels 
    cid1 = channels_create_v1(uid1['auth_user_id'], "ch1", True)
    cid2 = channels_create_v1(uid1['auth_user_id'], "ch2", False)

    listall = channels_listall_v1(uid1['auth_user_id'])

    assert listall['channels'][uid1['auth_user_id']] == {'channel_id': [[0, 1]], 'name': [['ch1', 'ch2']]}

# test listall func when no channels exist
def test_listall_no_channels():
    clear_v1()

    # create user
    uid1 = auth_register_v1("e1@gmail.com", "abcdefg123", "James", "Cai")

    listall = channels_listall_v1(uid1['auth_user_id'])

    assert listall['channels'][uid1['auth_user_id']] == {'channel_id': [[]], 'name': [[]]}

# =============================TESTING ERRORS================================

def test_invalid_listall_input():
    clear_v1()
    with pytest.raises(AccessError):
        channels_listall_v1('BOBbob')