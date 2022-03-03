import pytest
from src.auth import auth_register_v1
from src.data_store import data_store

# This function tests if users field is cleared 
# after calling auth-_register_V1()
def test_clear_valid():
    auth_register_v1(
        "abc@gmail.com",
        "123abc123",
        "Saitama",
        "Kun")
    users_data = data_store.get()
    clear_v1()
    assert users_data['users'] == []
    assert users_data['channels'] == []