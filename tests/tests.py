from bot import WOMApi, handlers
from config import secret
import os


def test_build_url():
    base_url = 'https://www.google.com/'

    endpoint = 'test_endpoint_one/'
    assert WOMApi.__build_url(base_url, endpoint) == 'https://www.google.com/test_endpoint_one/'

    endpoint = 'test_endpoint/{}/'
    args = ['two']
    assert WOMApi.__build_url(base_url, endpoint, args) == 'https://www.google.com/test_endpoint/two/'

    endpoint = 'test_endpoint/{}/{}/'
    args = ['three', 'four']
    assert WOMApi.__build_url(base_url, endpoint, args) == 'https://www.google.com/test_endpoint/three/four/'


def test_sotw_file():
    test_json_name = 'test_sotw.json'

    handlers.save_sotw(1, file_name=test_json_name)
    assert os.path.exists(secret.SOTW_PATH + test_json_name)

    os.remove(secret.SOTW_PATH + test_json_name)