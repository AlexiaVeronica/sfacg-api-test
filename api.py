from rich import print
import requests
import sys

max_retry = 10
headers = {
    'User-Agent': 'boluobao/4.5.52(iOS;14.0)/appStore',
    'Host': 'api.sfacg.com',
    'Authorization': 'Basic YXBpdXNlcjozcyMxLXl0NmUqQWN2QHFlcg=='
}


def get(api_url):
    api_url = 'https://api.sfacg.com/' + api_url.replace('https://api.sfacg.com/', '')
    for i in range(max_retry):
        try:
            return requests.get(api_url, headers=headers).json()
        except (OSError, TimeoutError, IOError) as error:
            print("\nGet Error Retry: " + api_url)


def get_dict_value(date, keys=None, default=None):
    if keys is None:
        print(date)
    else:
        keys_list = keys.split('.')
        if isinstance(date, dict):
            dictionary = dict(date)
            for i in keys_list:
                try:
                    if dictionary.get(i) is not None:
                        dict_values = dictionary.get(i)
                        dictionary = dict_values
                    elif dictionary.get(i) is None:
                        dict_values = dictionary.get(int(i))
                        dictionary = dict_values
                except:
                    return default
            return dictionary
        else:
            try:
                dictionary = dict(eval(date))
                if isinstance(dictionary, dict):
                    for i in keys_list:
                        try:
                            if dictionary.get(i) is not None:
                                dict_values = dictionary.get(i)
                                dictionary = dict_values
                            # 如果键对应的值不为空，返回对应的值
                            elif dictionary.get(i) is None:
                                dict_values = dictionary.get(int(i))
                                dictionary = dict_values
                            # 如果键对应的值为空，将字符串型的键转换为整数型，返回对应的值
                        except:
                            return default
                            # 如果字符串型的键转换整数型错误，返回None
                    return dictionary
            except:
                return default


input_api = sys.argv[1:]
try:
    if len(sys.argv) >= 3:
        print(get_dict_value(get(input_api[0]), input_api[1]))
    else:
        print(get_dict_value(get(input_api[0])))
except IndexError:
    print('python run.py    url     key')
