from apis import reApi
import json


class ApiFuncOne:
    def __init__(self, url, user, pwd):
        self.url = url
        self.user = user
        self.pwd = pwd

    def getapis(self):
        data = reApi.reapis(self.url, self.user, self.pwd).getapi_to_func_one()
        lens = len(data['ietf-interfaces:interfaces']['interface'])
        # print(lens)
        item = 0
        NewList = []
        while item < lens:
            ChildrenDict = {'name': data['ietf-interfaces:interfaces']['interface'][item]['name'],
                            'enabled': data['ietf-interfaces:interfaces']['interface'][item]['enabled'],
                            'type': data['ietf-interfaces:interfaces']['interface'][item]['type']}
            if data['ietf-interfaces:interfaces']['interface'][item]['ietf-ip:ipv4']:
                ipv4_data = data['ietf-interfaces:interfaces']['interface'][item]['ietf-ip:ipv4']['address']
                ipv4 = []
                # 这里有个bug,不过已经解决了.
                for i in ipv4_data:
                    ipv4.append(i)
            else:
                ipv4 = None
            # 若存在description
            if "description" in data['ietf-interfaces:interfaces']['interface'][item]:
                description = data['ietf-interfaces:interfaces']['interface'][item]['description']
            else:
                description = None
            ChildrenDict['description'], ChildrenDict['ipv4'] = description, ipv4
            NewList.append(ChildrenDict)
            item += 1
        return json.dumps(NewList)

    def putapis(self, newjson):
        # 接受post修改
        list = json.loads(newjson)
        yangConfig = {"ietf-interfaces:interface": {}}
        dict = list[0]
        yangConfig['ietf-interfaces:interface']['name'], yangConfig['ietf-interfaces:interface']['description'] = dict['name'], dict['description']
        yangConfig['ietf-interfaces:interface']['type'], yangConfig['ietf-interfaces:interface']['enabled'] = dict['type'], dict['enabled']
        chil = {'address': dict['ipv4']}
        yangConfig['ietf-interfaces:interface']['ietf-ip:ipv4'] = chil
        # 修正url的尾缀名
        url = self.url + 'interface=' + dict['name']
        return reApi.reapis(url, self.user, self.pwd).putapi(yangConfig)