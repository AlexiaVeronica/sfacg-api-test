import requests
import json


class Config:

    def __init__(self, file):
        self.file = file

    def save(self, data):
        with open(self.file, 'w') as outfile:
            json.dump(data, outfile)

    def read(self):
        with open(self.file) as json_file:
            return json.load(json_file)


json_info = Config('api_url.json').read()

headers = {
    'Host': 'api.sfacg.com',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Accept': 'application/vnd.sfacg.api+json;version=1',
    'User-Agent': json_info.get("User-Agent"),
    'Authorization': json_info.get("Authorization")
}


def get(url: str):
    api_url = json_info.get("Host") + url.replace(json_info.get("Host"), '')
    for retry in range(json_info.get("max_retry")):
        try:
            return requests.get(api_url, headers=headers).json()
        except (OSError, TimeoutError, IOError) as error:
            print("Get Error Retry: " + retry)


def post(url: str):
    api_url = json_info.get("Host") + url.replace(json_info.get("Host"), '')
    for retry in range(json_info.get("max_retry")):
        try:
            return requests.post(api_url, headers=headers).json()
        except (OSError, TimeoutError, IOError) as error:
            print("Get Error Retry: " + retry)
