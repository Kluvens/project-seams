import pytest

from src.channels import channels_list_v1, channels_listall_v1, channels_create_v1
from src.other import clear_v1
from src.data_store import data_store
from src.error import InputError
from src.auth import auth_register_v1

# =============================TESTING CORRECTNESS============================

# test if listall func displays all channels including public and private
def listall_public_and_private():
    clear_v1()

    # create user
    uid1 = auth_register_v1("e1@gmail.com", "abcdefg123", "James", "Cai")

    # create channels 
    cid1 = channels_create_v1(uid1['auth_user_id'], "ch1", True)
    cid2 = channels_create_v1(uid1['auth_user_id'], "ch2", False)

    listall = channels_listall_v1(uid1['auth_user_id'])

    assert listall['channels'][uid1['auth_user_id']] == [['ch1']]
    assert listall['channels'][uid1['auth_user_id']] == [['ch2']]

# test listall func when no channels exist
    clear_v1()

    # create user
    uid1 = auth_register_v1("e1@gmail.com", "abcdefg123", "James", "Cai")

    # create channels 
    cid1 = channels_create_v1(uid1['auth_user_id'], "ch1", True)
    cid2 = channels_create_v1(uid1['auth_user_id'], "ch2", False)

    listall = channels_listall_v1(uid1['auth_user_id'])

    with pytest.raises(IndexError):
        listall['channels'][uid2['auth_user_id']]
    
# invalid input error testing
def invalid_listall_input():
    clear_v1()
    with pytest.raises(AccessError):
        channels_listall_v1('BOBbob')