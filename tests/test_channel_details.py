from src.auth import auth_register_v1, auth_login_v1
from src.channels import channels_create_v1
from src.channel import channel_invite_v1, channel_details_v1
from src.data_store import data_store
from src.other import clear_v1

from src.error import InputError
from src.error import AccessError

import pytest

def test_channel_details_working():
    clear_v1()

    data = data_store.get()

    # first create two users
    first_auth_user = auth_register_v1("unswisgreat@unsw.edu.au", "unswisgreat123", "Tony", "Stark")
    first_u_id = data["users"][-1]["uid"]
    first_auth_user = auth_login_v1("unswisgreat@unsw.edu.au", "unswisgreat123")
    first_auth_user_id = first_auth_user["auth_user_id"]

    second_auth_user = auth_register_v1("hellounsw@gmail.com", "UNSWisgreat125", "Bruce", "Banner")
    second_u_id = data["users"][-1]["uid"]
    second_auth_user = auth_login_v1("hellounsw@gmail.com", "UNSWisgreat125")
    second_auth_user_id = second_auth_user["auth_user_id"]

    # create the channel and the host is the first user
    # name is the given name
    created_channel_id = channels_create_v1(first_auth_user_id, "Tony_channel", True).get("channel_id")

    # invite other people to join the current channel
    channel_invite(first_auth_user_id,created_channel_id,second_u_id)

    # get channel details
    # the results is a dictionary with { name, is_public, owner_members, all_members }
    # owner_members and all_members should be lists of dictionaries
    get_channel_details = channel_details(first_auth_user_id, created_channel_id)

    # check the details
    assert get_channel_details["name"] == "Tony_channel"
    assert get_channel_details["is_public"] == True
    assert get_channel_details["owner_members"] == [
        {
            'uid': first_u_id,
            'email': "unswisgreat@unsw.edu.au",
            'name_first': 'Tony',
            'name_last': 'Stark',
        }
    ]
    assert get_channel_details["all_members"][0] == {
            'uid': first_u_id,
            'email': "unswisgreat@unsw.edu.au",
            'name_first': 'Tony',
            'name_last': 'Stark',
        }
    assert get_channel_details["all_members"][1] == {
            'uid': second_u_id,
            'email': "hellounsw@gmail.com",
            'name_first': 'Bruce',
            'name_last': 'Banner',
        }

def test_channel_details_invalid_channel_id():
    clear_v1()
    # first create two users
    first_auth_user = auth_register_v1("unswisgreat@unsw.edu.au", "unswisgreat123", "Tony", "Stark")
    first_u_id = data["users"][-1]["uid"]
    first_auth_user = auth_login_v1("unswisgreat@unsw.edu.au", "unswisgreat123")
    first_auth_user_id = first_auth_user["auth_user_id"]

    second_auth_user = auth_register_v1("hellounsw@gmail.com", "UNSWisgreat125", "Bruce", "Banner")
    second_u_id = data["users"][-1]["uid"]
    second_auth_user = auth_login_v1("hellounsw@gmail.com", "UNSWisgreat125")
    second_auth_user_id = second_auth_user["auth_user_id"]

    # create the channel and the host is the first user
    # name is the given name
    created_channel_id = channels_create_v1(first_auth_user_id, "Tony_channel", True).get("channel_id")

    # invite other people to join the current channel
    channel_invite(first_auth_user_id,created_channel_id,second_u_id)

    # tests when channel_id is invalid
    with pytest.raises(InputError):
        channel_details(first_auth_user_id, created_channel_id + "unsw")



def test_channel_details_invalid_auth_id():
    clear_v1()
    # first create two users
    first_auth_user = auth_register_v1("unswisgreat@unsw.edu.au", "unswisgreat123", "Tony", "Stark")
    first_u_id = data["users"][-1]["uid"]
    first_auth_user = auth_login_v1("unswisgreat@unsw.edu.au", "unswisgreat123")
    first_auth_user_id = first_auth_user["auth_user_id"]

    second_auth_user = auth_register_v1("hellounsw@gmail.com", "UNSWisgreat125", "Bruce", "Banner")
    second_u_id = data["users"][-1]["uid"]
    second_auth_user = auth_login_v1("hellounsw@gmail.com", "UNSWisgreat125")
    second_auth_user_id = second_auth_user["auth_user_id"]

    # create the channel and the host is the first user
    # name is the given name
    created_channel_id = channels_create_v1(first_auth_user_id, "Tony_channel", True).get("channel_id")

    # invite other people to join the current channel
    channel_invite(first_auth_user_id,created_channel_id,second_u_id)

    # tests when channel_id is invalid
    with pytest.raises(AccessError):
        channel_details(first_auth_user_id + "unsw", created_channel_id)
        