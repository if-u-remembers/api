

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
    datas = json.loads(get_api_one())
    # print(type(datas))
    # print(len(datas['ietf-interfaces:interfaces']['interface']))
    return datas


def new_dict():
    dicts = jsonTodata()
    lens = len(dicts['ietf-interfaces:interfaces']['interface'])
    i = 0
    NewDicts = {}
    while i < lens:
        ChildrenDict = {}
        ChildrenDict['enabled'] = dicts['ietf-interfaces:interfaces']['interface'][i]['enabled']
        NewDicts[dicts['ietf-interfaces:interfaces']['interface'][i]['name']] = i
        if dicts['ietf-interfaces:interfaces']['interface'][i]['ietf-ip:ipv4']:
            ip = dicts['ietf-interfaces:interfaces']['interface'][i]['ietf-ip:ipv4']['address'][0]['ip']
            netmask = dicts['ietf-interfaces:interfaces']['interface'][i]['ietf-ip:ipv4']['address'][0]['netmask']
            description = dicts['ietf-interfaces:interfaces']['interface'][i]['description']
            ChildrenDict['description'] = description
            ChildrenDict['ip'] = ip
            ChildrenDict['netmask'] = netmask
        else:
            ChildrenDict['ip'] = 'null'
            ChildrenDict['netmask'] = 'null'
        NewDicts[dicts['ietf-interfaces:interfaces']['interface'][i]['name']] = ChildrenDict
        i += 1
    return json.dumps(NewDicts)


# print(jsonTodata())
# print(get_api_one())
print(new_dict())

