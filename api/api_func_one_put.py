import json
import requests
from api import api_put

def put_api_one():
    requests.packages.urllib3.disable_warnings()
    # api_url = "https://ios-xe-mgmt-latest.cisco.com:9443/restconf/data/ietf-interfaces:interfaces/interface=GigabitEthernet1"
    api_url = 'https://li-say.top:6002/restconf/data/ietf-interfaces:interfaces/'
    headers = {"Accept": "application/yang-data+json",
               "Content-type": "application/yang-data+json"
               }
    basicauth = ("cisco", "cisco123!")
    # basicauth = ("developer", "C1sco12345")
    yangConfig = {
        "ietf-interfaces:interface": {
            "name": "GigabitEthernet2",
            "description": "aaaaa",
            "type": "iana-if-type:ethernetCsmacd",
            "enabled": True,
            "ietf-ip:ipv4": {
                "address": [
                    {
                        "ip": "10.10.20.52",
                        "netmask": "255.255.255.0"
                    }
                ]
            },
            "ietf-ip:ipv6": {}
        }
    }
    resp = requests.put(api_url, data=json.dumps(yangConfig), auth=basicauth, headers=headers, verify=False)

    if (resp.status_code >= 200 and resp.status_code <= 299):
        return '{}'.format(resp.status_code)
    else:
        return '{}'.format(resp.status_code)


# print(put_api_one())


def put_api_ones(newjson):
    """
    输入修改参数进行数据的修正
    :return:
    """
    list = json.loads(newjson)
    yangConfig = {"ietf-interfaces:interface": {}}
    dict = list[0]
    yangConfig['ietf-interfaces:interface']['name'] = dict['name']
    yangConfig['ietf-interfaces:interface']['description'] = dict['description']
    yangConfig['ietf-interfaces:interface']['type'] = dict['type']
    yangConfig['ietf-interfaces:interface']['enabled'] = dict['enabled']
    chil = {}
    chil['address'] = dict['ipv4']
    yangConfig['ietf-interfaces:interface']['ietf-ip:ipv4'] = chil
    # return yangConfig
    requests.packages.urllib3.disable_warnings()
    # api_url = "https://ios-xe-mgmt-latest.cisco.com:9443/restconf/data/ietf-interfaces:interfaces/interface=GigabitEthernet1"
    api_url = 'https://li-say.top:6002/restconf/data/ietf-interfaces:interfaces/'
    return api_put.put_api(api_url, yangConfig)
