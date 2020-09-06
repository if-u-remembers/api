from apis import reApi, mysql
import urllib3, requests
from requests.auth import HTTPBasicAuth
import json

url_api = 'https://sandboxdnac2.cisco.com'


def model_into(template_content, name):
    # 其中template_content是模板命令，name是模板名
    payloadf = {
        "templateContent": template_content,
        "softwareType": "IOS-XE",
        "deviceTypes": [
            {
                "productFamily": "Switches and Hubs"
            },
            {
                "productFamily": "Routers"
            }
        ],
        "name": name
    }
    return payloadf


class new_func_two:
    def __init__(self, url, user, pwd, modelhost, modelmysqluser, modelpassword, modeldatabase):
        self.sql = mysql.inmysql(modelhost, modelmysqluser, modelpassword, modeldatabase)
        self.user = user
        self.pwd = pwd
        self.urls = url
        self.table_name = 'cisco_model_data'

    def __get_token(self):
        '''
        获取token串
        :return: 一个token串
        '''
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
            return resp.status_code
        elif resp.status_code == 500:
            print('已经存在', payloadf['name'], '无法创建')
            return resp.status_code
        # print(resp.text.encode('utf8'))

    def get_project_id(self, name):
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
            return data[0]['id']
        else:
            return None

    def put_project(self, name, payloadf):
        # 下发模板，输入id，和
        # 这里查询数据库获取模板信息，然后查询一遍思科id
        pid = self.get_project_id(name)
        url = self.urls + '/dna/intent/api/v1/template-programmer/project/' + str(pid) + '/template'
        # url = self.urls + '/dna/intent/api/v1/template-programmer/project/' + '9386b328-beb9-4046-ab1a-db5860cade20'+ '/template'
        token = self.__get_token()
        headers = {
            'X-Auth-Token': token,
            'Content-Type': "application/json",
            'cache-control': "no-cache"
        }
        resp = requests.request("POST", url, headers=headers, json=payloadf)
        # print(resp.text.encode('utf8'))
        if 200 <= resp.status_code <= 299:
            return resp.status_code
        else:
            return '400'

    def __redata_todo(self, item):
        mid, model, name, logo, introduce, remarks = item[0], item[1], item[2], item[3], item[4], item[5]
        children_dict = {'id': mid, 'modelname': name, 'remakes': remarks, 'introduce': introduce, 'model': model,
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
        global children_dictss
        data = self.sql.select_for_id(self.table_name, 'id', ids)
        for item in data:
            children_dictss = self.__redata_todo(item)
            # 返回字典格式数据
        return children_dictss

    # 删改查部分:
    def __select(self, data):
        try:
            select = json.loads(data)['id']
            if type(select) == type(1):
                return json.dumps(self.redata_id(select))
            else:
                selist = []
                for item in select:
                    selist.append(self.redata_id(item))
                return json.dumps(selist)
        except:
            # 异常返回一个空数据
            print('error')
            return json.dumps([])

    def __updata(self, data):
        # 返回数据为： 200， 400
        dicts = json.loads(data)
        id, modelname, remarks, introduce, url, model, logo = dicts['id'], dicts['modelname'], dicts['remarks'], dicts[
            'introduce'], dicts['url'], dicts['model'], dicts['logo']
        return self.sql.fun2_updata(id, modelname, model, url, remarks, introduce, logo)

    def __adds(self, data):
        # 返回数据为： 200， 400
        dicts = json.loads(data)
        modelname, remarks, introduce, url, model, logo = dicts['modelname'], dicts['remarks'], dicts['introduce'], \
                                                          dicts['url'], dicts['model'], dicts['logo']
        return self.sql.fun2_add(modelname, model, url, remarks, introduce, logo)

    def __dels(self, data):
        # 返回数据为一个id，error字段的字典嵌套数组
        dist = json.loads(data)['id']
        relist = []
        for item in dist:
            error = self.sql.dels(self.table_name, 'id', item)
            newdist = {'id': item, 'error': error}
            relist.append(newdist)
        return json.dumps(relist)

    def mysqls(self, name, data):
        if name == 'del':
            return self.__dels(data)
        elif name == 'modify':
            return self.__updata(data)
        elif name == 'add':
            return self.__adds(data)
        elif name == 'select':
            # 这里返回多组数据,且保留id及空的情况
            return self.__select(data)

    # 还没完工sql.fun2_updata 这里需要修改…^^^^


user = 'admin'
pwd = 'Cisco1234!'
host = 'li-say.top'
mysqluser = 'root'
password = '981002'
database = 'office'

a = new_func_two(url=url_api, user=user, pwd=pwd, modelhost=host, modelmysqluser=mysqluser, modelpassword=password,
                 modeldatabase=database)
print(a.select_model())
