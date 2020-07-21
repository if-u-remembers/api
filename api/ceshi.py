
import json
import requests
import urllib3


def put_api_ones():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    # api_url = 'https://ios-xe-mgmt-latest.cisco.com:9443/restconf/data/ietf-interfaces:interfaces/interface=GigabitEthernet1'
    payload = {
        'ietf-interfaces:interface':
            {
                'name': "GigabitEthernet5",
                'description': "wudeqiang-interface",
                'type': "iana-if-type:ethernetCsmacd",
                'enabled': True,
                'ietf-ip:ipv4': {
                    'address': [
                        {
                            'ip': "10.10.20.48",
                            'netmask': "255.255.255.0"}
                    ]
                },
                'ietf-ip:ipv6': {}
            }
    }
    basicauth = ("developer", "C1sco12345")
    # headers = {
    #     'Accept': 'application/yang-data+json',
    #     'Content-Type': 'application/yang-data+json',
    #     'Authorization': 'Basic ZGV2ZWxvcGVyOkMxc2NvMTIzNDU='
    # }
    api_url = "https://ios-xe-mgmt-latest.cisco.com:9443/restconf/data/ietf-interfaces:interfaces/"
    headers = {
              "Accept": "application/yang-data+json",
               "Content-type": "application/yang-data+json"
        }


    # 关闭认证
    # resp = requests.post(api_url, json=payload, headers=headers, verify=False)

    resp = requests.post(api_url, json=payload, auth=basicauth, headers=headers, verify=False)
    print(resp)
    response_json = json.dumps(resp.json(), indent=4)

    return response_json
    # return resp


print(put_api_ones())