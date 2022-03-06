import pytest
from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.data_store import data_store
from src.channel import channel_messages_v1
from src.other import clear_v1

# This function tests if users field is cleared 
# after calling auth-_register_V1()
def test_clear_valid():
    clear_v1()

    # Creating a new user and new channel
    user_one = auth_register_v1("abc@gmail.com", "123abc123", "Saitama", "Kun")
    new_channel_one = channels_create_v1(user_one['auth_user_id'], "mychannel", True)

    clear_v1()

    user_two = auth_register_v1("ryan117@gmail.com", "Password123", "John", "Howard")
    new_channel_two = channels_create_v1(user_two['auth_user_id'], "my_channel", False)

    assert user_one['auth_user_id'] == user_two['auth_user_id']
    assert new_channel_one['channel_id'] == new_channel_two['channel_id']