"""
    创建于2020/7/16
    对api进行数据处理并返回数据到app.py
    利用参数对信息进行判断
"""
import json
import requests
import urllib3


def get_api_one():
    """
    调用已经配置好的数据
    :return: 返回参数
    """
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    api_url = "https://ios-xe-mgmt-latest.cisco.com:9443/restconf/data/ietf-interfaces:interfaces/"
    headers = {"Accept": "application/yang-data+json",
               "Content-type":"application/yang-data+json"
        }
    basicauth = ("developer", "C1sco12345")
    resp = requests.get(api_url, auth=basicauth, headers=headers, verify=False)
    response_json = json.dumps(resp.json(), indent=4)
    return response_json


def get_new_api_ones(api_url, headers, basicauth):
    """
    调用未配置好的数据
    :param api_url: api链接
    :param headers: http头数据
    :param basicauth: 请求密码？
    :return: 返回一个get值
    """
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    resp = requests.get(api_url, auth=basicauth, headers=headers, verify=False)
    response_json = json.dumps(resp.json(), indent=4)
    return response_json


# def put_new_api_ones(api_url, headers, basicauth):
#     urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#     resp = requests.put(api_url, auth=basicauth, headers=headers, verify=False)
#     response_json = json.dumps(resp.json(), indent=4)
#     return response_json


def put_api_ones():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    api_url='https://ios-xe-mgmt-latest.cisco.com:9443/restconf/data/ietf-interfaces:interfaces/interface=GigabitEthernet1'
    payload = {
        'ietf-interfaces:interface':
            {
             'name': 'GigabitEthernet1',
             'description': 'wudeqiang-interface',
             'type': 'iana-if-type:ethernetCsmacd',
             'enabled': True,
             'ietf-ip:ipv4': {
                 'address': [
                     {
                         'ip': '10.10.20.48',
                         'netmask': '255.255.255.0'}
                 ]
             },
             'ietf-ip:ipv6': {}
        }
    }
    headers = {
        'Accept': 'application/yang-data+json',
        'Content-Type': 'application/yang-data+json',
        'Authorization': 'Basic ZGV2ZWxvcGVyOkMxc2NvMTIzNDU='
    }
    # basicauth = ("developer", "C1sco12345")
    resp = requests.post(api_url, data=payload, headers=headers)
    # resp = requests.put(url, auth=basicauth, headers=headers, verify=False)
    response_json = json.dumps(resp.json(), indent=4)

    # payload = {'key1': 'value1', 'key2': 'value2'}
    # resp = requests.post("http://httpbin.org/post", data=payload)

    return response_json


# print(put_api_ones())
