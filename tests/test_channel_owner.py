from src.auth import auth_register_v1, auth_login_v1
from src.channels import channels_create_v1
from src.channel import channel_invite_v1, channel_details_v1, channel_addowner_v1, channel_removeowner_v1, find_user_index, get_user_id
from src.other import clear_v1

from src.error import InputError
from src.error import AccessError

from src.helper import get_user_id
from src.data_store import data_store

import pytest

def test_add_owner_working():
    clear_v1()

    # register and login for users
    first_u_id = get_user_id("unswisgreat@unsw.edu.au", "unswisgreat123", "Tony", "Stark")
    
    second_u_id = get_user_id("hellounsw@gmail.com", "UNSWisgreat125", "Bruce", "Banner")

    # create a channel
    created_channel_id = channels_create_v1(first_u_id, "Tony_channel", True).get("channel_id")

    # invite other people to join the current channel
    channel_invite_v1(first_u_id,created_channel_id,second_u_id)

    channel_addowner_v1(first_u_id, created_channel_id, second_u_id)

    # get channel details
    first_channel_details = channel_details_v1(first_u_id, created_channel_id)
    
    assert first_channel_details["name"] == "Tony_channel"
    assert first_channel_details["is_public"] == True
    assert first_channel_details["owner_members"][0] == {
        "u_id": first_u_id,
        "email": "unswisgreat@unsw.edu.au",
        "name_first": "Tony",
        "name_last": "Stark",
        "handle_str": "tonystark",
    }
    assert first_channel_details["owner_members"][1] == {
        "u_id": second_u_id,
        "email": "hellounsw@gmail.com",
        "name_first": "Bruce",
        "name_last": "Banner",
        "handle_str": "brucebanner",
    }
    assert first_channel_details["all_members"][0] == {
        "u_id": first_u_id,
        "email": "unswisgreat@unsw.edu.au",
        "name_first": "Tony",
        "name_last": "Stark",
        "handle_str": "tonystark",
    }
    assert first_channel_details["all_members"][1] == {
        "u_id": second_u_id,
        "email": "hellounsw@gmail.com",
        "name_first": "Bruce",
        "name_last": "Banner",
        "handle_str": "brucebanner",
    }

def test_add_owner_channel_id_invalid():
    clear_v1()

    # register and login for users
    first_u_id = get_user_id("unswisgreat@unsw.edu.au", "unswisgreat123", "Tony", "Stark")
    
    second_u_id = get_user_id("hellounsw@gmail.com", "UNSWisgreat125", "Bruce", "Banner")

    # create the channel and the host is the first user
    # name is the given name
    created_channel_id = channels_create_v1(first_u_id, "Tony_channel", True).get("channel_id")

    # invite other people to join the current channel
    channel_invite_v1(first_u_id, created_channel_id, second_u_id)

    # tests when channel_id is invalid
    with pytest.raises(InputError):
        channel_addowner_v1(first_u_id, created_channel_id + 1, second_u_id)

def test_add_owner_u_id_invalid():
    clear_v1()

    # register and login for users
    first_u_id = get_user_id("unswisgreat@unsw.edu.au", "unswisgreat123", "Tony", "Stark")
    
    second_u_id = get_user_id("hellounsw@gmail.com", "UNSWisgreat125", "Bruce", "Banner")

    # create the channel and the host is the first user
    # name is the given name
    created_channel_id = channels_create_v1(first_u_id, "Tony_channel", True).get("channel_id")

    # invite other people to join the current channel
    channel_invite_v1(first_u_id, created_channel_id, second_u_id)

    # tests when auth_user_id is invalid
    with pytest.raises(InputError):
        channel_addowner_v1(first_u_id, created_channel_id, second_u_id+1)

def test_add_owner_u_id_not_member():
    clear_v1()

    # register and login for users
    first_u_id = get_user_id("unswisgreat@unsw.edu.au", "unswisgreat123", "Tony", "Stark")
    
    second_u_id = get_user_id("hellounsw@gmail.com", "UNSWisgreat125", "Bruce", "Banner")

    third_u_id = get_user_id("heyhellounsw@gmail.com", "UNSWisgreat1251", "Bruces", "Banners")

    # create the channel and the host is the first user
    # name is the given name
    created_channel_id = channels_create_v1(first_u_id, "Tony_channel", True).get("channel_id")

    # invite other people to join the current channel
    channel_invite_v1(first_u_id, created_channel_id, second_u_id)

    # tests when auth_user_id is invalid
    with pytest.raises(InputError):
        channel_addowner_v1(first_u_id, created_channel_id, third_u_id)

def test_add_owner_u_id_already_owner():
    clear_v1()

    # register and login for users
    first_u_id = get_user_id("unswisgreat@unsw.edu.au", "unswisgreat123", "Tony", "Stark")
    
    second_u_id = get_user_id("hellounsw@gmail.com", "UNSWisgreat125", "Bruce", "Banner")

    # create the channel and the host is the first user
    # name is the given name
    created_channel_id = channels_create_v1(first_u_id, "Tony_channel", True).get("channel_id")

    # invite other people to join the current channel
    channel_invite_v1(first_u_id, created_channel_id, second_u_id)

    channel_addowner_v1(first_u_id, created_channel_id, second_u_id)

    with pytest.raises(InputError):
        channel_addowner_v1(first_u_id, created_channel_id, second_u_id)

def test_add_owner_no_permission():
    pass

def test_add_owner_auth_user_id_invalid():
    '''
    if token to user id is failed, then throw an accesserror
    '''
    pass

def test_remove_owner_working():
    clear_v1()

    # register and login for users
    first_u_id = get_user_id("unswisgreat@unsw.edu.au", "unswisgreat123", "Tony", "Stark")
    
    second_u_id = get_user_id("hellounsw@gmail.com", "UNSWisgreat125", "Bruce", "Banner")

    # create a channel
    created_channel_id = channels_create_v1(first_u_id, "Tony_channel", True).get("channel_id")

    # invite other people to join the current channel
    channel_invite_v1(first_u_id,created_channel_id,second_u_id)

    channel_addowner_v1(first_u_id, created_channel_id, second_u_id)

    channel_removeowner_v1(first_u_id, created_channel_id, second_u_id)

    # get channel details
    first_channel_details = channel_details_v1(first_u_id, created_channel_id)

    assert first_channel_details["name"] == "Tony_channel"
    assert first_channel_details["is_public"] == True
    assert first_channel_details["owner_members"][0] == {
        "u_id": first_u_id,
        "email": "unswisgreat@unsw.edu.au",
        "name_first": "Tony",
        "name_last": "Stark",
        "handle_str": "tonystark",
    }
    assert first_channel_details["all_members"][0] == {
        "u_id": first_u_id,
        "email": "unswisgreat@unsw.edu.au",
        "name_first": "Tony",
        "name_last": "Stark",
        "handle_str": "tonystark",
    }
    assert first_channel_details["all_members"][1] == {
        "u_id": second_u_id,
        "email": "hellounsw@gmail.com",
        "name_first": "Bruce",
        "name_last": "Banner",
        "handle_str": "brucebanner",
    }

def test_remove_owner_channel_id_invalid():
    clear_v1()

    # register and login for users
    first_u_id = get_user_id("unswisgreat@unsw.edu.au", "unswisgreat123", "Tony", "Stark")
    
    second_u_id = get_user_id("hellounsw@gmail.com", "UNSWisgreat125", "Bruce", "Banner")

    # create the channel and the host is the first user
    # name is the given name
    created_channel_id = channels_create_v1(first_u_id, "Tony_channel", True).get("channel_id")

    # invite other people to join the current channel
    channel_invite_v1(first_u_id, created_channel_id, second_u_id)

    channel_addowner_v1(first_u_id, created_channel_id, second_u_id)

    # tests when channel_id is invalid
    with pytest.raises(InputError):
        channel_removeowner_v1(first_u_id, created_channel_id + 1, second_u_id)

def test_remove_owner_u_id_invalid():
    clear_v1()

    # register and login for users
    first_u_id = get_user_id("unswisgreat@unsw.edu.au", "unswisgreat123", "Tony", "Stark")
    
    second_u_id = get_user_id("hellounsw@gmail.com", "UNSWisgreat125", "Bruce", "Banner")

    # create the channel and the host is the first user
    # name is the given name
    created_channel_id = channels_create_v1(first_u_id, "Tony_channel", True).get("channel_id")

    # invite other people to join the current channel
    channel_invite_v1(first_u_id, created_channel_id, second_u_id)

    # tests when auth_user_id is invalid
    with pytest.raises(InputError):
        channel_removeowner_v1(first_u_id, created_channel_id, second_u_id+1)

def test_remove_owner_u_id_not_member():
    clear_v1()

    # register and login for users
    first_u_id = get_user_id("unswisgreat@unsw.edu.au", "unswisgreat123", "Tony", "Stark")
    
    second_u_id = get_user_id("hellounsw@gmail.com", "UNSWisgreat125", "Bruce", "Banner")

    # create the channel and the host is the first user
    # name is the given name
    created_channel_id = channels_create_v1(first_u_id, "Tony_channel", True).get("channel_id")

    # invite other people to join the current channel
    channel_invite_v1(first_u_id, created_channel_id, second_u_id)

def test_remove_owner_u_id_the_only_owner():
    clear_v1()

    # register and login for users
    first_u_id = get_user_id("unswisgreat@unsw.edu.au", "unswisgreat123", "Tony", "Stark")

    created_channel_id = channels_create_v1(first_u_id, "Tony_channel", True).get("channel_id")

    with pytest.raises(InputError):
        channel_removeowner_v1(first_u_id, created_channel_id, first_u_id)

def test_remove_owner_no_permission():
    pass

def test_remove_owner_auth_user_id_invalid():
    pass