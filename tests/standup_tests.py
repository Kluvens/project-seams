import json
import requests
import pytest
from src.config import url
from tests.http_helpers import GenerateTestData
from src.error import InputError
from src.error import AccessError
from src.helpers import decode_token
from src.standup import standup_start_v1, standup_active_v1, standup_send_v1
from src.channels import channels_create_v2
from src.auth import auth_register_v2
from src.other import clear_v1
from src.data_store import data_store

import time
from datetime import datetime, timedelta

import pytest

def test_standup_active():
    clear_v1()
    user1 = auth_register_v2("1@gmail.com","1231234","james","cai")
    chl = channels_create_v2(user1['token'], "ch1", True)
    std1 = standup_start_v1(user1['token'], chl['channel_id'], 5)
    standup_active = standup_active_v1(user1['token'], chl['channel_id'])
    assert standup_active['is_active'] == True


def test_standup_start():
    clear_v1()
    user1 = auth_register_v2("1@gmail.com","1231234","james","cai")
    chl = channels_create_v2(user1['token'], "sample", True)
    standup = standup_start_v1(user1['token'], chl['channel_id'], 5)
    assert standup['time_finish'] - (datetime.now()+timedelta(seconds = 5)).timestamp() < 1

def test_standup_send():
    clear_v1()
    data = data_store.get()
    user1 = auth_register_v2("1@gmail.com","1231234","james","cai")
    chl = channels_create_v2(user1['token'], "sample", True)
    standup_start_v1(user1['token'], chl['channel_id'], 5)
    assert standup_send_v1(user1['token'], chl['channel_id'], "Hello") == {}
    assert data['channels'][0]['standup']['message'] == 'james: Hello\n'