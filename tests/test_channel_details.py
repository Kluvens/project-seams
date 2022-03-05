# Jiapeng Yang(Justin) z5339252

from src.auth import auth_register_v1, auth_login_v1
from src.channels import channels_create_v1
from src.channel import channel_invite_v1, channel_details_v1
from src.data_store import data_store
from src.other import clear_v1

from src.error import InputError
from src.error import AccessError

import pytest

'''
the testing function tests when a single user created a channel
'''
def test_channel_details_working_single_member():
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
the testing function tests when one user created a channel and invite others to join
'''
def test_channel_details_working_multiple_members():
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
testing when the users are valid but channel_id is invalid
'''
def test_channel_details_invalid_channel_id():
    clear_v1()

    # register and login for users
    first_auth_user = auth_register_v1("unswisgreat@unsw.edu.au", "unswisgreat123", "Tony", "Stark")
    first_auth_user = auth_login_v1("unswisgreat@unsw.edu.au", "unswisgreat123")
    first_u_id = first_auth_user["auth_user_id"]

    second_auth_user = auth_register_v1("hellounsw@gmail.com", "UNSWisgreat125", "Bruce", "Banner")
    second_auth_user = auth_login_v1("hellounsw@gmail.com", "UNSWisgreat125")
    second_u_id = second_auth_user["auth_user_id"]

    # create the channel and the host is the first user
    # name is the given name
    created_channel_id = channels_create_v1(first_u_id, "Tony_channel", True).get("channel_id")

    # invite other people to join the current channel
    channel_invite_v1(first_u_id,created_channel_id,second_u_id)

    # tests when channel_id is invalid
    with pytest.raises(InputError):
        channel_details_v1(first_u_id, str(created_channel_id) + "unsw")


'''
testing when channel_id is valid but the user who sent the details request is not in the channel
'''
def test_channel_details_invalid_auth_id():
    clear_v1()

    # register and login for users
    first_auth_user = auth_register_v1("unswisgreat@unsw.edu.au", "unswisgreat123", "Tony", "Stark")
    first_auth_user = auth_login_v1("unswisgreat@unsw.edu.au", "unswisgreat123")
    first_u_id = first_auth_user["auth_user_id"]

    second_auth_user = auth_register_v1("hellounsw@gmail.com", "UNSWisgreat125", "Bruce", "Banner")
    second_auth_user = auth_login_v1("hellounsw@gmail.com", "UNSWisgreat125")
    second_u_id = second_auth_user["auth_user_id"]

    # create the channel and the host is the first user
    # name is the given name
    created_channel_id = channels_create_v1(first_u_id, "Tony_channel", True).get("channel_id")

    # invite other people to join the current channel
    channel_invite_v1(first_u_id,created_channel_id,second_u_id)

    # tests when channel_id is invalid
    with pytest.raises(AccessError):
        channel_details_v1(str(first_u_id) + "unsw", created_channel_id)

        