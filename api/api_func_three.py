from api import three_mysql_and_func_def
from api import api_func_one_get
import time
from time import perf_counter
import json


def GetDdosData():
    # api = 'https://ios-xe-mgmt-latest.cisco.com:9443/restconf/data/Cisco-IOS-XE-interfaces-oper:interfaces/'
    api = 'https://li-say.top:6002/restconf/data/Cisco-IOS-XE-interfaces-oper:interfaces/'
    headers = {"Accept": "application/yang-data+json",
               "Content-type": "application/yang-data+json"
        }
    # basicauth = ("developer", "C1sco12345")
    basicauth = ("cisco", "cisco123!")

    try:
        datas = api_func_one_get.get_new_api_ones(api, headers, basicauth)
        data = json.loads(datas)
        # data = api_func_one_get.get_new_api_ones(api, headers, basicauth)
        listtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(listtime)
        # print(data)
        # 查到每个设备的参数
        list = data['Cisco-IOS-XE-interfaces-oper:interfaces']['interface']
        # intlist = []
        for item in list:
            children = {}
            # 循环每个设备
            acl = item['input-security-acl']
            if (acl == '101' or item['if-index'] == 1) and item['v4-protocol-stats']['in-pkts'] != '':
                children['id'], children['name'], children['pkts'], children['time'], children['acl'] = item['if-index'], item['name'], item['v4-protocol-stats']['in-pkts'], listtime, item['input-security-acl']
                three_mysql_and_func_def.Add_ddos(children)
            else:
                pass
        for i in three_mysql_and_func_def.select_ddos():
            print(i)
        return ''
    except:
        return 'error'


print(GetDdosData())
