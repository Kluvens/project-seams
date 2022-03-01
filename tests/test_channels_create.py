from src.auth import auth_register_v1, auth_login_v1
from src.channels import channels_create_v1
from src.channel import channel_invite_v1, channel_details_v1
from src.data_store import data_store
from src.other import clear_v1

from src.error import InputError
from src.error import AccessError

import pytest


def test_channel_create_working():
    clear_v1()

    data = data_store.get()

    first_auth_user = auth_register_v1("unswisgreat@unsw.edu.au", "unswisgreat123", "Tony", "Stark")
    first_u_id = data["users"][-1]["uid"]
    first_auth_user = auth_login_v1("unswisgreat@unsw.edu.au", "unswisgreat123")
    first_auth_user_id = first_auth_user["auth_user_id"]

    created_channel_id = channels_create_v1(first_auth_user_id, "Tony_channel", True).get("channel_id")

    # check the channel id and name stored in data
    # -1 means the newly created channel always located in the last place in data
    check_user = data["users"][first_u_id]
    assert data["channels"][-1]["cid"] == created_channel_id
    assert data["channels"][-1]["name"] == "Tony_channel"
    assert data["channels"][-1]["is_public"] == True
    assert data["channels"][-1]["owner_members"][0] == {
        'uid': check_user["uid"],
        'email': check_user["email"],
        'name_first': check_user["name_first"],
        'name_last': check_user["name_last"],
    }
    assert data["channels"][-1]["all_members"][0] == {
        'uid': check_user["uid"],
        'email': check_user["email"],
        'name_first': check_user["name_first"],
        'name_last': check_user["name_last"],
    }

def test_channel_create_inputError():
    clear_v1()

    first_auth_user = auth_register_v1("unswisgreat@unsw.edu.au", "unswisgreat123", "Tony", "Stark")
    first_u_id = data["users"][-1]["uid"]
    first_auth_user = auth_login_v1("unswisgreat@unsw.edu.au", "unswisgreat123")
    first_auth_user_id = first_auth_user["auth_user_id"]

    # length of name is less than 1
    with pytest.raises(InputError):
        channels_create_v1(first_auth_user_id, "", True)

    # length of name is more than 20
    with pytest.raises(InputError):
        channels_create_v1(first_auth_user_id, "hahahahahaahahahahahamustbemorethantwentyletters", True)