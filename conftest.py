import pytest
from tests.http_helpers import GenerateTestData
from src.config import url
import requests

@pytest.fixture(scope="module")
def reset_call():
    response = requests.delete(url + 'clear/v1')
    return response.status_code

@pytest.fixture(scope="module")
def dummy_data():
    data_instance = GenerateTestData(url)
    return data_instance
