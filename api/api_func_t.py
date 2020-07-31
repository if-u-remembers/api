from netmiko import ConnectHandler
import json
import requests


def acl():
    # create a variable object that represents the ssh cli session
    sshCli = ConnectHandler(
            device_type='cisco_ios',
            host='www.li-say.top',
            port=6002,
            username='cisco',
            password='cisco123!'
    )
    # send some simple "exec" commands and display the returned output
    print("configure ACL to interface.")
    config_commands = [
        'int Loopback1',
        'ip access-group 101 in'
    ]
    # print("Sending the config commands.")
    output = sshCli.send_config_set(config_commands)
    return output
    # print("Config output from the device:\n{}\n".format(output))


def down(name):
    requests.packages.urllib3.disable_warnings()
    api_url = "https://ios-xe-mgmt-latest.cisco.com:9443/restconf/data/ietf-interfaces:interfaces/interface=GigabitEthernet2"
    headers = { "Accept": "application/yang-data+json",
                "Content-type": "application/yang-data+json"
        }
    basicauth = ("developer", "C1sco12345")
    yangConfig = {"ietf-interfaces:interface": {
        "name": "GigabitEthernet2",
        "description": "Network Interface",
        "type": "iana-if-type:ethernetCsmacd",
        "enabled": False,
        "ietf-ip:ipv4": {},
        "ietf-ip:ipv6": {}
    }}
    yangConfig['ietf-interfaces:interface']['name'] = name
    resp = requests.put(api_url, data=json.dumps(yangConfig), auth=basicauth, headers=headers, verify=False)
    return 0
