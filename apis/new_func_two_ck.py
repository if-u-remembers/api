import json
import requests
import urllib3
from requests.auth import HTTPBasicAuth

from apis import reApi, mysql


class new_func_two:
    def __init__(self, url, user, pwd, modelhost, modelmysqluser, modelpassword, modeldatabase):
        self.sql = mysql.inmysql(modelhost, modelmysqluser, modelpassword, modeldatabase)
        self.intosql = mysql.intomysql(modelhost, modelmysqluser, modelpassword, modeldatabase)
        self.user = user
        self.pwd = pwd
        self.urls = url
        self.table_name = 'cisco_model_data'

    def __get_token(self):
        # 获取token字符串用的
        """
        获取token串
        :return: 一个token串
        """
        url = self.urls + '/dna/system/api/v1/auth/token'
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        # try:
        token = requests.post(url, auth=HTTPBasicAuth(self.user, self.pwd),
                              headers={'content-type': 'application/json'}, verify=False).json()
        if 'error' in token:
            print('用户或者用户密码错误')
            return None
        elif 'Token' in token:
            return token['Token']

    def create_project(self, name):
        # 新建一个项目
        url = self.urls + '/dna/intent/api/v1/template-programmer/project'
        token = self.__get_token()
        headers = {
            'X-Auth-Token': token,
            'Content-Type': "application/json",
            'cache-control': "no-cache"
        }
        if token is None:
            return '400'
        payloadf = {'name': name}
        resp = reApi.reapis(url, self.user, self.pwd).requestapi(headers, payloadf)
        if 200 <= resp.status_code <= 299:
            print('成功创建', payloadf['name'])
            return str(resp.status_code)
        elif resp.status_code == 500:
            print('已经存在', payloadf['name'], '无法创建')
            return str(resp.status_code)

    def get_project_id(self, name):
        # 通过name 获取项目id
        url = self.urls + '/dna/intent/api/v1/template-programmer/project?name=' + name
        token = self.__get_token()
        headers = {
            'X-Auth-Token': token,
            'Content-Type': "application/json",
            'cache-control': "no-cache"
        }
        resp = reApi.reapis(url, self.user, self.pwd).getapi(headers)
        data = json.loads(resp.text.encode('utf8'))
        if 200 <= resp.status_code <= 299 and data:
            return data[0]
        else:
            return None

    def create_model(self, name, model_id):
        # 给项目name创建model
        token = self.__get_token()
        pid = self.get_project_id(name)
        url = self.urls + '/dna/intent/api/v1/template-programmer/project/' + pid['id'] + '/template'
        headers = {
            'X-Auth-Token': token,
            'Content-Type': "application/json",
            'cache-control': "no-cache"
        }
        data = self.redata_id(model_id)
        if data is None:
            return '400'
        PAYLOADF = {
            'templateContent': data['model'],
            'softwareType': 'IOS-XE',
            'deviceTypes': [
                {
                    'productFamily': 'Switches and Hubs'
                },
                {
                    'productFamily': 'Routers'
                }
            ],
            'name': data['modelname']
        }
        resp = requests.request("POST", url, headers=headers, json=PAYLOADF)
        if 200 <= resp.status_code <= 299:
            print('成功创建', PAYLOADF['name'])
            return str(resp.status_code)
        else:
            print('已经存在', PAYLOADF['name'], '无法创建')
            return str(resp.status_code)

    def batch_create_model(self, name, listid):
        relist = []
        for item in listid:
            redict = {'id': item, 'code': self.create_model(name, item)}
            relist.append(redict)
        return json.dumps(relist)

    def get_project_model(self, name):
        # 获取某个项目中的所有模板，数据如下：
        # [{'name': 'OSPF', 'id': 'f87cce87-5d84-425a-80e1-956a0e63e481', 'mid': 1},
        #  {'name': 'ACL', 'id': '00cca6c2-8c7d-4e2e-aa22-1050d2396daa', 'mid': 2}]
        data = self.get_project_id(name)
        if data:
            relist = []
            mid = 1
            # print(data)
            for item in data['templates']:
                # 从数据库查询到该模板名
                sqlname = item['name']
                sql = self.sql.select_for_id('cisco_model_data', 'name', sqlname)
                sql2 = self.sql.select_for_id('cisco_model_data2', 'name', sqlname)
                if sql:
                    model_data = sql[0][1]
                    introduce = sql[0][4]
                elif sql2:
                    # model_data = sql[0][1]
                    # introduce = sql[0][3]
                    model_data = sql2[0][1]
                    introduce = sql2[0][3]
                else:
                    print('data1和2都查不到数据')
                    model_data = None
                    introduce = None
                newdict = {'modelName': item['name'], 'id': item['id'], 'mid': mid, "model": model_data, "introduce": introduce}
                mid += 1
                relist.append(newdict)
            return relist
        else:
            return []

    def del_project_model(self, name, mid):
        # 删除某个项目中的model, mid是模板中的id号
        # 删除后记得重新查询一次新的project
        token = self.__get_token()
        pid = self.get_project_model(name)[mid - 1]['id']
        url = self.urls + '/dna/intent/api/v1/template-programmer/template/' + pid
        headers = {
            'X-Auth-Token': token,
            'Content-Type': "application/json",
            'cache-control': "no-cache"
        }
        resp = requests.request("DELETE", url, headers=headers)
        if 200 <= resp.status_code <= 299:
            print('成功删除')
            return str(resp.status_code)
        else:
            print('无法删除')
            return str(resp.status_code)

    def batch_del_project_model(self, name, listid):
        relist = []
        for item in listid:
            redict = {'id': item, 'code': self.del_project_model(name, item)}
            relist.append(redict)
        return relist

    def updata_project_model_data(self, name, mid, modeldata_data, modeldata_name, introduce):
        # 先查询到数据库中数据是否和其符合
        data1 = self.sql.select_for_id('cisco_model_data', 'name', modeldata_name)
        data2 = self.sql.select_for_id('cisco_model_data2', 'name', modeldata_name)
        data3 = self.sql.select('cisco_model_data2')
        if data1:
            print("查询到数据库存在数据")
        elif len(data2) >= 1:
            # 当data2存在数据
            self.sql.new_func2_updata('cisco_model_data2', modeldata_data, introduce, modeldata_name)
        else:
            val = ((modeldata_data, modeldata_name, introduce),)
            self.intosql.add_data(val, 'cisco_model_data2', ['model', 'name', 'introduce'])
        # 通过项目名查询到模板的id 并对该id所属的模板进行修改配置
        token = self.__get_token()
        pid = self.get_project_model(name)[mid - 1]['id']
        url = self.urls + '/dna/intent/api/v1/template-programmer/template/'
        headers = {
            'X-Auth-Token': token,
            'Content-Type': "application/json",
            'cache-control': "no-cache"
        }
        PAYLOADF = {
            "id": pid,
            "templateContent": modeldata_data,
            "softwareType": "IOS-XE",
            "deviceTypes": [
                {"productFamily": "Switches and Hubs"},
                {"productFamily": "Routers"}
            ],
            "name": modeldata_name
        }
        resp = requests.request("PUT", url, headers=headers, json=PAYLOADF)
        if 200 <= resp.status_code <= 299:
            print('成功修改')
            return str(resp.status_code)
        else:
            print('无法修改')
            return str(resp.status_code)

    ###################
    # 部署设备
    ###################
    def get_device(self):
        # 获取设备ip地址
        token = self.__get_token()
        url = self.urls + '/dna/intent/api/v1/network-device'
        headers = {
            'X-Auth-Token': token,
            'Content-Type': "application/json",
            'cache-control': "no-cache"
        }
        resp = requests.request("GET", url, headers=headers)
        data = resp.json()['response']
        for item in data:
            print(item)
        if 200 <= resp.status_code <= 299:
            print('成功获取ip')
            return str(resp.status_code)
        else:
            print('无法获取ip')
            return str(resp.status_code)

    def deploy_project_model(self, project_name, model_name, tid):
        # 部署某个项目中的模板
        templateid = None
        token = self.__get_token()
        url = self.urls + '/dna/intent/api/v1/template-programmer/template/deploy'
        headers = {
            'X-Auth-Token': token,
            'Content-Type': "application/json",
            'cache-control': "no-cache"
        }
        data = self.get_project_model(project_name)
        # 获取到所有项目数据，进行遍历找出对应的模板数据
        for item in data:
            if item['modelName'] == model_name:
                print(item)
                templateid = item['id']
                break
        if not templateid:
            # 如果没有找到，返回400错误
            print('not temp')
            return '400'
        PAYLOADF = {
            "templateId": templateid,
            "targetInfo": [
                {
                    "id": tid,
                    "type": 'MANAGED_DEVICE_IP'
                }
            ]
        }
        resp = requests.request("POST", url, headers=headers, json=PAYLOADF)
        print(resp.json())
        if 200 <= resp.status_code <= 299:
            print('成功部署')
            return str(resp.status_code)
        else:
            print('无法部署')
            return str(resp.status_code)

    def batch_deploy_project_model(self, model, pname):
        relist = []
        for item in model:
            code = self.deploy_project_model(pname, item['modelname'], item['id'])
            relist.append({'modelname': item['modelname'], 'code': code})
        return relist

    def all_project(self):
        # 获取所有模项目的名称
        url = self.urls + '/dna/intent/api/v1/template-programmer/project'
        token = self.__get_token()
        headers = {
            'X-Auth-Token': token,
            'Content-Type': "application/json",
            'cache-control': "no-cache"
        }
        if token is None:
            return '400'
        resp = requests.request("GET", url, headers=headers)
        data = json.loads(resp.text.encode('utf8'))

        if 200 <= resp.status_code <= 299 and data:
            relist = []
            mid = 0
            for item in data:
                relist.append({'name': item['name'], 'id': mid})
                mid += 1
            return relist
        else:
            return []

    ###################
    # 下列都是数据库操作
    ###################
    @staticmethod
    def __redata_todo(item):
        mid, model, name, logo, introduce, remakes = item[0], item[1], item[2], item[3], item[4], item[5]
        children_dict = {'id': mid, 'modelname': name, 'remakes': remakes, 'introduce': introduce, 'model': model,
                         'logo': logo}
        return children_dict

    def __getdata(self):
        data = self.sql.select(self.table_name)
        list_data = []
        for item in data:
            list_data.append(self.__redata_todo(item))
        return list_data

    def redata(self):
        # 返回用户可见的数据
        data = self.__getdata()
        list_data = []
        for item in data:
            children_dicts = {'id': item['id'], 'modelname': item['modelname'], 'remakes': item['remakes'],
                              'introduce': item['introduce'], 'logo': item['logo']}
            list_data.append(children_dicts)
        return json.dumps(list_data)

    def redata_id(self, ids):
        # ids是一个数字格式的数据
        data = self.sql.select_for_id(self.table_name, 'id', ids)
        if data:
            children_dictss = self.__redata_todo(data[0])
            # 返回字典格式数据
            return children_dictss
        else:
            return None

    def __select(self, data):
        try:
            select = json.loads(data)['id']
            if type(select) == type(1):
                return json.dumps(self.redata_id(select))
            else:
                selist = []
                for item in select:
                    redata_ids = self.redata_id(item)
                    print(redata_ids)
                    if redata_ids not in selist:
                        selist.append(redata_ids)
                return json.dumps(selist)
        except:
            # 异常返回一个空数据
            print('error')
            return json.dumps([])

    def __updata(self, data):
        # 返回数据为： 200， 400
        dicts = json.loads(data)
        mid, model, name, logo, introduce, remakes = dicts['id'], dicts['model'], dicts['modelname'], dicts['logo'], dicts['introduce'], dicts['remakes']
        return self.sql.fun2_updata(self.table_name, mid, name, model, remakes, introduce, logo)

    def __adds(self, data):
        # 返回数据为： 200， 400
        dicts = json.loads(data)
        model, name, logo, introduce, remakes = dicts['model'], dicts['modelname'], dicts['logo'], dicts['introduce'], dicts['remakes']
        return self.sql.fun2_add(self.table_name, model, name, logo, introduce, remakes)

    def __dels(self, data):
        # 返回数据为一个id，error字段的字典嵌套数组
        dist = json.loads(data)['id']
        relist = []
        for item in dist:
            error = self.sql.dels(self.table_name, 'id', item)
            newdist = {'id': item, 'code': error}
            relist.append(newdist)
        return json.dumps(relist)

    def mysqls(self, name, data):
        if name == 'del':
            return self.__dels(data)
        elif name == 'updata':
            return self.__updata(data)
        elif name == 'add':
            return self.__adds(data)
        elif name == 'select':
            # 这里返回多组数据,且保留id及空的情况
            return self.__select(data)