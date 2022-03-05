import pytest

from src.auth import auth_register_v1, auth_login_v1
from src.channels import channels_create_v1
from src.channel import channel_messages_v1
from src.other import clear_v1

from src.error import InputError, AccessError

def test_channel_messages_InputError():
    clear_v1()

    uid = auth_register_v1("ryan117@gmail.com", "Password123", "John", "Howard")
    new_channel = channels_create_v1(uid['auth_user_id'], "my_channel", True)
    start_number = 0

    # Input invalid channel
    with pytest.raises(InputError):
        channel_messages_v1(uid['auth_user_id'], new_channel['channel_id'] + 1, start_number)
    # assert error.type == InputError

    # # Input invalid start number
    # with pytest.raises(InputError):
    #     channel_messages_v1(uid['auth_user_id'], "my_channel", 99999999)
    # # assert error.type == InputError

def test_channel_invite_AccessError():
    clear_v1()

    uid_one = auth_register_v1("ryan117@gmail.com", "Password123", "John", "Howard")
    new_channel = channels_create_v1(uid_one['auth_user_id'], "my_channel", False)
    start_number = 0

    uid_two = auth_register_v1("kakarot007@gmail.com", "mypassword1", "Harry", "Potter")

    # uid_two is not a member of the channel
    with pytest.raises(AccessError):
        channel_messages_v1(uid_two['auth_user_id'], "my_channel", start_number)
    # assert error.type == AccessError


def test_channel_messages_working():
    clear_v1()
    
    uid = auth_register_v1("ryan117@gmail.com", "Password123", "John", "Howard")
    new_channel = channels_create_v1(uid['auth_user_id'], "my_channel", True)
    start_number = 0

    messages_output = channel_messages_v1(uid['auth_user_id'], "my_channel", start_number)

    assert messages_output['start'] == start_number
    assert messages_output['messages'] == []
    assert messages_output['end'] == start_number or messages_output['end'] == -1