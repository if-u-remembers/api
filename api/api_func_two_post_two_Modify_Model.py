from api import MysqlApi
import json

# id = 1
# name = 'LoopBack244445'
# model = '''{"ietf-interfaces:interface": {"name": "Loopback6", "description": "WHATEVER6", "type": "iana-if-type:softwareLoopback","enabled": True,"ietf-ip:ipv4": {"address": [{"ip": "6.6.6.6","netmask": "255.255.255.0"}]},"ietf-ip:ipv6": {}}}'''
# url = '''https://ios-xe-mgmt-latest.cisco.com:9443/restconf/data/ietf-interfaces:interfaces/interface=Loopback6'''
# remark = '创汇还'
# introduce = '回环'
#
# print(MysqlApi.updataData(id, name, model, url, remark, introduce))


def ModifyModelJsonData(data):
    return json.loads(data)


def ModifyModel(datas):
    dict = ModifyModelJsonData(datas)
    id, modelname, remarks, introduce, url, model, logo = dict['id'], dict['modelname'], dict['remarks'], dict['introduce'], dict['url'], dict['model'], dict['logo']
    return MysqlApi.updataData(id, modelname, model, url, remarks, introduce, logo)


def AddModel(datas):
    dict = ModifyModelJsonData(datas)
    modelname, remarks, introduce, url, model, logo = dict['modelname'], dict['remarks'], dict['introduce'], dict['url'], dict['model'], dict['logo']
    # print(model)
    # return '0'
    return MysqlApi.AddData(modelname, model, url, remarks, introduce, logo)


def DelModel(id_list):
    dist = json.loads(id_list)
    list = dist['id']
    relist = []
    for item in list:
        dist = {}
        error = MysqlApi.DelData(item)
        dist['id'], dist['code'] = item, error
        relist.append(dist)
    return json.dumps(relist)

# print(MysqlApi.selectData())