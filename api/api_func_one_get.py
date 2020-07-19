

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


def jsonTodata():
    """
    获取思科getapi的数据，并转换为基本字典数据。
    :return:
    """
    datas = json.loads(get_api_one())
    # print(type(datas))
    # print(len(datas['ietf-interfaces:interfaces']['interface']))
    return datas


def twoIPdata():
    """
    模拟一个设备两个ip的数据
    :return: 一个字典格式的数据
    """
    datas = {
        "ietf-interfaces:interfaces": {
            "interface": [
                {
                    "name": "GigabitEthernet1",
                    "description": "MANAGEMENT INTERFACE - DON'T TOUCH ME",
                    "type": "iana-if-type:ethernetCsmacd",
                    "enabled": True,
                    "ietf-ip:ipv4": {
                        "address": [
                            {
                                "ip": "10.10.20.48",
                                "netmask": "255.255.255.0"
                            },
                            {
                                "ip": "10.10.20.49",
                                "netmask": "255.255.255.0"
                            },
                            {
                                "ip": "10.10.20.50",
                                "netmask": "255.255.255.0"
                            }
                        ]
                    },
                    "ietf-ip:ipv6": {}
                },
                {
                    "name": "GigabitEthernet2",
                    "description": "MANAGEMENT INTERFACE - DON'T TOUCH ME",
                    "type": "iana-if-type:ethernetCsmacd",
                    "enabled": True,
                    "ietf-ip:ipv4": {
                        "address": [
                            {
                                "ip": "10.10.20.70",
                                "netmask": "255.255.255.2"
                            },
                            {
                                "ip": "10.10.20.80",
                                "netmask": "255.255.255.0"
                            },
                            {
                                "ip": "10.10.20.90",
                                "netmask": "255.255.255.1"
                            }
                        ]
                    },
                    "ietf-ip:ipv6": {}
                }
            ]
        }
    }
    return datas


def new_dict(dicts):
    lens = len(dicts['ietf-interfaces:interfaces']['interface'])
    i = 0
    # 构建一个空字典，作为最外层
    NewList = []
    while i < lens:
        ChildrenDict = {}
        ChildrenDict['name'] = dicts['ietf-interfaces:interfaces']['interface'][i]['name']
        ChildrenDict['enabled'] = dicts['ietf-interfaces:interfaces']['interface'][i]['enabled']
        ChildrenDict['type'] = dicts['ietf-interfaces:interfaces']['interface'][i]['type']
        if dicts['ietf-interfaces:interfaces']['interface'][i]['ietf-ip:ipv4']:
            ipv4_data = dicts['ietf-interfaces:interfaces']['interface'][i]['ietf-ip:ipv4']['address']
            ipv4 = []
            for item in ipv4_data:
                ipv4.append(item)
            description = dicts['ietf-interfaces:interfaces']['interface'][i]['description']
            ChildrenDict['description'] = description
            ChildrenDict['ipv4'] = ipv4
        else:
            ChildrenDict['ip'] = 'null'
            ChildrenDict['netmask'] = 'null'
        NewList.append(ChildrenDict)
        i += 1
    return json.dumps(NewList)


# print(new_dict(twoIPdata()))
# print(new_dict(jsonTodata()))
# print(jsonTodata())
# print(get_api_one())
