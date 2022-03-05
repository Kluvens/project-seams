# Jiapeng Yang(Justin) z5339252

from src.auth import auth_register_v1, auth_login_v1
from src.channels import channels_create_v1
from src.channel import channel_invite_v1, channel_details_v1
from src.other import clear_v1

from src.error import InputError
from src.error import AccessError

import pytest

'''
testing when a single user wants to create a channel and channel_id is valid
'''
def test_channel_create_working_single_user():
    clear_v1()

    # register and login for a user
    first_auth_user = auth_register_v1("unswisgreat@unsw.edu.au", "unswisgreat123", "Tony", "Stark")
    first_auth_user = auth_login_v1("unswisgreat@unsw.edu.au", "unswisgreat123")
    first_u_id = first_auth_user["auth_user_id"]

    created_channel_id = channels_create_v1(first_u_id, "Tony_channel", True).get("channel_id")

    first_channel_details = channel_details_v1(first_u_id, created_channel_id)

    # testing
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

'''
testing when a user created a channel and invite others to join, the channel_id is always valid
'''
def test_channel_create_working_many_user():
    clear_v1()

    # register and login for users
    first_auth_user = auth_register_v1("unswisgreat@unsw.edu.au", "unswisgreat123", "Tony", "Stark")
    first_auth_user = auth_login_v1("unswisgreat@unsw.edu.au", "unswisgreat123")
    first_u_id = first_auth_user["auth_user_id"]

    second_auth_user = auth_register_v1("hellounsw@gmail.com", "UNSWisgreat125", "Bruce", "Banner")
    second_auth_user = auth_login_v1("hellounsw@gmail.com", "UNSWisgreat125")
    second_u_id = second_auth_user["auth_user_id"]

    # create a channel
    created_channel_id = channels_create_v1(first_u_id, "Tony_channel", True).get("channel_id")

    # invite other people to join the current channel
    channel_invite_v1(first_u_id,created_channel_id,second_u_id)

    # get channel details
    first_channel_details = channel_details_v1(first_u_id, created_channel_id)

    # testing
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

'''
we only problems on specification can happen
testing when user_id is valid but channel name is none
'''
def test_channel_create_inputError_less_than_1():
    clear_v1()

    # register and login for a user
    first_auth_user = auth_register_v1("unswisgreat@unsw.edu.au", "unswisgreat123", "Tony", "Stark")
    first_auth_user = auth_login_v1("unswisgreat@unsw.edu.au", "unswisgreat123")
    first_u_id = first_auth_user["auth_user_id"]

    # length of name is less than 1
    with pytest.raises(InputError):
        channels_create_v1(first_u_id, "", True)

'''
testing when user id is valid but channel name is more than 20 characters
'''
def test_channel_create_inputError_more_than_20():
    clear_v1()

    # register and login for a user
    first_auth_user = auth_register_v1("unswisgreat@unsw.edu.au", "unswisgreat123", "Tony", "Stark")
    first_auth_user = auth_login_v1("unswisgreat@unsw.edu.au", "unswisgreat123")
    first_u_id = first_auth_user["auth_user_id"]
    
    # length of name is more than 20
    with pytest.raises(InputError):
        channels_create_v1(first_u_id, "hahahahahaahahahahahamustbemorethantwentyletters", True)
        
