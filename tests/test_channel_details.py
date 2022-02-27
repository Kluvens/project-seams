from src.auth import auth_register_v1, auth_login_v1
from src.channels import channels_create_v1
from src.channel import channel_invite_v1, channel_details_v1
from src.data_store import data_store
import pytest

'''
stored data strcture

data = {
    'users': [
        {
            'u_id': 1,
            'email': email1,
            'name_first': name_first,
            'name_last': name_last,
            'password': password,
        },
        {
            'u_id': 2,
            'email': email2,
            'name_first': name_first,
            'name_last': name_last,
            'password': password,
        },
    ],
    'channels': [
        {
            'c_id': 1,
            'name' : 'channel1',
            'is_public': True,
            'owner_members': [
                {
                    'u_id': 1,
                    'email': 'example@gmail.com',
                    'name_first': 'Hayden',
                    'name_last': 'Jacobs',
                    'handle_str': 'haydenjacobs',
                }
            ],
            'all_members': [
                {
                    'u_id': 1,
                    'email': 'example@gmail.com',
                    'name_first': 'Hayden',
                    'name_last': 'Jacobs',
                    'handle_str': 'haydenjacobs',
                }
            ]
        },
        {
            'c_id': 2,
            'name' : 'channel2',
            'is_public': True,
        },
    ],
}

'''

'''
register return structure

{
    "auth_user_id": 1
}
'''

'''
the strcture for channel details
{
    'name': 'Hayden',
    'is_public': True,
    'owner_members': [
        {
            'u_id': 1,
            'email': 'example@gmail.com',
            'name_first': 'Hayden',
            'name_last': 'Jacobs',
            'handle_str': 'haydenjacobs',
        }
    ],
    'all_members': [
        {
            'u_id': 1,
            'email': 'example@gmail.com',
            'name_first': 'Hayden',
            'name_last': 'Jacobs',
            'handle_str': 'haydenjacobs',
        }
    ],
}
'''

def test_channel_details_working():
    # first create two users
    first_auth_user_id = auth_register_v1("unswisgreat@unsw.edu.au", "unswisgreat123", "Tony", "Stark")
    first_auth_user_id = auth_login_v1("unswisgreat@unsw.edu.au", "unswisgreat123")
    first_user_id = first_auth_user_id["auth_user_id"]

    second_auth_user_id = auth_register_v1("hellounsw@gmail.com", "UNSWisgreat125", "Bruce", "Banner")
    second_auth_user_id = auth_login_v1("hellounsw@gmail.com", "UNSWisgreat125")
    second_user_id = second_auth_user_id["auth_user_id"]

    # create the channel and the host is the first user
    # name is the given name
    created_channel_id = channels_create_v1(first_user_id, "Tony_channel", True).get("channel_id")

    # invite other people to join the current channel
    channel_invite(first_user_id,created_channel_id,second_user_id)

    # get channel details
    # the results is a dictionary with { name, is_public, owner_members, all_members }
    # owner_members and all_members should be lists of dictionaries
    get_channel_details = channel_details(first_user_id, created_channel_id)

    # check the details
    assert get_channel_details[name] == "Tony_channel"
    assert get_channel_details[is_public] == True
    assert get_channel_details[owner_members] == [
        {
            'u_id': first_user_id,
            'email': "unswisgreat@unsw.edu.au",
            'name_first': 'Tony',
            'name_last': 'Stark',
        }
    ]
    assert get_channel_details[all_members][0] == {
            'u_id': first_user_id,
            'email': "unswisgreat@unsw.edu.au",
            'name_first': 'Tony',
            'name_last': 'Stark',
        }
    assert get_channel_details[all_members][1] == {
            'u_id': second_user_id,
            'email': "hellounsw@gmail.com",
            'name_first': 'Bruce',
            'name_last': 'Banner',
        }

def test_channel_details_invalid_channel_id():
    # first create two users
    first_auth_user_id = auth_register_v1("unswisgreat@unsw.edu.au", "unswisgreat123", "Tony", "Stark")
    first_auth_user_id = auth_login_v1("unswisgreat@unsw.edu.au", "unswisgreat123")
    first_user_id = first_auth_user_id["auth_user_id"]
    second_auth_user_id = auth_register_v1("hellounsw@gmail.com", "UNSWisgreat125", "Bruce", "Banner")
    second_auth_user_id = auth_login_v1("hellounsw@gmail.com", "UNSWisgreat125")
    second_user_id = second_auth_user_id["auth_user_id"]

    # create the channel and the host is the first user
    # name is the given name
    created_channel_id = channels_create_v1(first_user_id, "Tony_channel", True).get("channel_id")

    # invite other people to join the current channel
    channel_invite(first_auth_user_id,created_channel_id,second_user_id)

    # tests when channel_id is invalid
    with pytest.raises(InputError):
        channel_details(first_auth_user_id, channel_id + "unsw")



def test_channel_details_invalid_auth_id():
    # first create two users
    first_auth_user_id = auth_register_v1("unswisgreat@unsw.edu.au", "unswisgreat123", "Tony", "Stark")
    first_auth_user_id = auth_login_v1("unswisgreat@unsw.edu.au", "unswisgreat123")
    first_user_id = first_auth_user_id["auth_user_id"]
    second_auth_user_id = auth_register_v1("hellounsw@gmail.com", "UNSWisgreat125", "Bruce", "Banner")
    second_auth_user_id = auth_login_v1("hellounsw@gmail.com", "UNSWisgreat125")
    second_user_id = second_auth_user_id["auth_user_id"]

    # create the channel and the host is the first user
    # name is the given name
    created_channel_id = channels_create_v1(first_user_id, "Tony_channel", True).get("channel_id")

    # invite other people to join the current channel
    channel_invite(first_auth_user_id,created_channel_id,second_user_id)

    # tests when channel_id is invalid
    with pytest.raises(AccessError):
        channel_details(first_auth_user_id + "unsw", channel_id)